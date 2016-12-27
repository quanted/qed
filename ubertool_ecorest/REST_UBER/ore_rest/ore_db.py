import logging
import os
import sqlite3


file_path = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(file_path, 'sqliteDB', 'ore.s3db')
# Connecting to the database file
conn = sqlite3.connect(db)
c = conn.cursor()


def loadChoices(query):
    choices = []

    if query == 'crop':
        # TODO: I don't think this is used anymore
        choices = cropQuery()
    elif query == 'oreDb':
        choices = oreDbQuery()
    # print choices

    # choices = c.fetchone()
    # print choices.keys()

    # print choices['Crop']
    return choices


def cropQuery():
    # TODO: This is not currently used...
    c.execute('SELECT DISTINCT CCA FROM CCA')

    return c.fetchall()


# , GrpName, SubGrpNo, SubGrpName
def oreDbQuery():
    """
    SQLite query returning all of the available data needed to populate the "Crop-Target Category Lookup" tab
    :return: SQLite cursor
    """
    # TODO: Change TABLE name to the Crop Slection table that has not yet been Created :-(
    # TODO: Currently using the old DB for Crop Lookup table

    c.execute('SELECT DISTINCT Crop, GrpNo, GrpName, SubGrpNo, SubGrpName, Category FROM CCA')

    return c.fetchall()


def generateSQLFilter(sql_filter, es_type, category):
    """
    Generates the SQLite query to populate the Exposure Scenario tab.
    (e.g. "Category=? AND AppEquip IN (?, ?, ?, ?)") resulting in:
    SELECT DISTINCT Activity, AppType, AppEquip, Formulation FROM OccHandlerNC WHERE Category=? AND AppEquip IN (?, ?, ?, ?)

    :param sql_filter:
    :param es_type: string
    :param category: string
    :return: (SQLite query string, list of insertion values)
    """
    query_string = "Category = ? AND ("
    insertion_list = [category]

    i = 0
    while i < len(sql_filter):
        insertion_list.append(sql_filter[i])  # append values to be inserted into SQL statement (? substitution)
        if (i + 1) != 1:  # NOT first loop
            query_string += " OR "
        query_string += es_type + " = ?"
        i += 1

    query_string += ")"
    # print query_string
    # print insertion_list

    return query_string, insertion_list


def oreWorkerActivities(query):
    """
    SQL query of to populate the exposure scenario tab
    """
    category = query['crop_category']
    _query_root = 'SELECT DISTINCT Activity, AppType, AppEquip, Formulation FROM OccHandlerNC WHERE '

    if 'es_type' in query:  # Exposure Scenario filtering (e.g. has 'es_type' key in request)
        sql_filter = query['es_type_filter']
        es_type = query['es_type']

        # TODO: Handle "Spray(all starting formulations)" logic
        """
        Spray = [L, SC, EC], DF, WDG, WP, or WSP
        Spray + Flagger = above + "Broadcast" AppType
        """

        query_string = generateSQLFilter(sql_filter, es_type, category)
        print _query_root + query_string[0] + ', ' + str(query_string[1])

        crop_category = tuple(query_string[1])
        c.execute(_query_root + query_string[0],
                  crop_category)
    else:  # Crop-Target query (Crop-Target Category Lookup Tab)
        """
        SQL query example (Target Category == "Field crop, high-acreage"):

        SELECT DISTINCT Activity, AppType, AppEquip, Formulation FROM OccHandlerNC WHERE
             (Category="Field crop, high-acreage"
             AND Formulation NOT IN (SELECT Formulation FROM OccHandlerNC WHERE Formulation LIKE 'Spray%'));
        """
        crop_category = (category,)  # Must be a tuple
        print _query_root + "(Category=? AND Formulation NOT IN "\
                            "(SELECT Formulation FROM OccHandlerNC WHERE Formulation LIKE 'Spray%'))"
        c.execute(_query_root +
                  "(Category=? AND Formulation NOT IN "
                  "(SELECT Formulation FROM OccHandlerNC WHERE Formulation LIKE 'Spray%'))",
                  crop_category)

    query = c.fetchall()

    formulation = []
    appequip = []
    apptype = []
    activity = []

    # print query

    for result in query:

        if result[0] not in activity:
            activity.append(result[0])
        if result[1] not in apptype:
            apptype.append(result[1])
        if result[2] not in appequip:
            appequip.append(result[2])
        if result[3] not in formulation:
            formulation.append(result[3])

    # print activity
    # print apptype
    # print appequip
    # print formulation

    return {'Activity': activity,
            'AppType': apptype,
            'AppEquip': appequip,
            'Formulation': formulation}


def oreOutputQuery(inputs):
    """
    SELECT * FROM OccHandlerNC WHERE Crop = 'Corn, field' AND (Activity = 'M/L' OR Activity = 'Applicator' OR Activity = 'Fla
    gger') AND AppEquip = 'Aerial' AND AppType = 'Broadcast' AND (Formulation = 'L/SC/EC' OR Formulation = 'Spray (all start
    ing formulations)');
    """

    # TODO: This is set up to work with only ONE crop/target category; it must be changed to allow for multiple...

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    category = inputs['exp_category']
    activities = inputs['exp_scenario']['Activity']
    app_eqips = inputs['exp_scenario']['AppEquip']
    app_types = inputs['exp_scenario']['AppType']
    formulations = inputs['exp_scenario']['Formulation']

    params = [category]

    def query_generator(exp_scenario, exp_scenario_list):

        query_string = exp_scenario + " = ?"  # E.g. "Activity = ?"
        i = 0
        while i < len(exp_scenario_list):
            params.append(exp_scenario_list[i])  # append item to params[] to pass to SQL statement
            if i > 0:  # skip 1st list item bc it is handle by default in the 'query_string' string definition
                query_string += " OR " + exp_scenario + " = ?"  # E.g. "Activity = ? OR Activity = ? OR Activity = ?"
            i += 1
        return query_string

    sql_query = 'SELECT * FROM OccHandlerNC WHERE Category = ? ' \
                'AND (' + query_generator('Activity', activities) + ') ' \
                'AND (' + query_generator('AppEquip', app_eqips) + ') ' \
                'AND (' + query_generator('AppType', app_types) + ') ' \
                'AND (' + query_generator('Formulation', formulations) +')'

    # TreatedVal, TreatedUnit, DUESLNoG, DUESLG, DUEDLG, DUESLGCRH, DUEDLGCRH, IUENoR, IUEPF5R, IUEPF10R, IUEEC
    print sql_query
    print params

    c.execute(sql_query, tuple(params))

    query = c.fetchall()
    conn.close()  # Close 'row_factory' connection

    return query
