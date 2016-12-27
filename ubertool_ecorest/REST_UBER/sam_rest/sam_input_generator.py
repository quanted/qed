# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""

import copy
from datetime import date, datetime, timedelta


def convert_date_to_days_since_date2(date, date2):
    """
        date: Python Date object; end date in date range
        date2: Python Date object; start date in date range

        returns: int; number of days between the two dates, including the last day
    """

    no_of_days = (date - date2) + timedelta(days=1)

    return no_of_days.days


def sim_date_index_list(start_date_since_1900, end_date_since_1900, start_datetime_object):
    """
        start_date_since_1900: int; Number of days from Jan 1, 1900 to simulation start date
        end_date_since_1900: int; Number of days from Jan 1, 1900 to simulation end date
        start_datetime_object: Python DateTime object; Simulation start DateTime object

        returns: tuple (list, list)
            tuple[0] = list of number of days in simulation from 1900.
            tuple[1] = list of each day in simulation (m/d/yyyy HH:MM:SS AM/PM)
    """

    day_list = []
    date_list = []

    curr_datetime = start_datetime_object

    while (start_date_since_1900 < end_date_since_1900 + 1):
        # Append days since 1900 to list
        day_list.append(start_date_since_1900)

        # Append Date to list
        date_list.append(curr_datetime.strftime("%m/%d/%Y %H:%M:%S %p"))
        curr_datetime = curr_datetime + timedelta(days=1)

        start_date_since_1900 += 1

    return day_list, date_list


def app_num_record(args):
    """
        Produces 4 Python lists, corresponding to 4 lines of the SAM.inp file. The lists are, if order:
            1) Application record number
            2) Application day since 1900
            3) Application rate
            4) Application method

        The lists generated are dependant on the Application Rifement choosen
        (e.g. Uniform, Uniform with Step, Triangular).  Each refinement has its own method to produce the lists.
    """

    firstapp_datetime_object = datetime.strptime(args['sim_date_1stapp'], "%m/%d/%Y")
    firstapp_date_since1900 = convert_date_to_days_since_date2(firstapp_datetime_object.date(), date(1900, 1,
                                                                                                     1))  # Equivalent to 'appcount' in VB code (SAMBeta.vb)

    no_of_apps = int(args['apps_per_year']) * int(
        args['sim_no_of_years'])  # Number of applications each year X number of years in simulation

    tspan = (args['sim_date_end_since1900'] - args[
        'sim_date_start_since1900']) + 1  # Time span, number of simulation days
    appfreq = tspan / no_of_apps  # 'appfreq' is an 'int' type

    application_method = args['application_method']

    refinement = args['refine']

    if refinement == 'uniform':
        return app_refine_uniform(
            firstapp_date_since1900,
            no_of_apps,
            args['application_rate'],
            args['application_method'],
            appfreq,
            args['refine_time_window1'],
        )
    elif refinement == 'uniform_step':
        return app_refine_uniform_with_step(
            firstapp_date_since1900,
            no_of_apps,
            args['application_rate'],
            args['application_method'],
            appfreq, args['refine_time_window1'],
            args['refine_percent_applied1'],
            args['refine_time_window2'],
            args['refine_percent_applied2']
        )
    elif refinement == 'triangular':
        return app_refine_triangular(
            firstapp_date_since1900,
            no_of_apps,
            args['application_rate'],
            args['application_method'],
            appfreq,
            args['refine_time_window1'],
        )
    else:
        # Default to 'Uniform with Step'
        return app_refine_uniform_with_step(
            firstapp_date_since1900,
            no_of_apps,
            args['application_rate'],
            args['application_method'],
            appfreq, args['refine_time_window1'],
            args['refine_percent_applied1'],
            args['refine_time_window2'],
            args['refine_percent_applied2']
        )


def app_refine_uniform(appcount, no_of_apps, application_rate, application_method, appfreq, time_window_1):
    """
        Application Refinement: Uniform over Window

        returns: Tuple including the 4 Python lists for app_num_record() method and the total number of applications:
            tuple[0]: app_num_record_list
            tuple[1]: app_record_day_since_1900_list
            tuple[2]: app_rate_list
            tuple[3]: app_method_list
            tuple[4]: total_no_of_apps
    """

    application_rate = float(application_rate) / float(time_window_1)

    jdate_i = convert_date_to_days_since_date2(date(1984, 1, 1), date(1900, 1, 1))

    app_num_record_list = []
    app_record_day_since_1900_list = []
    app_rate_list = []
    app_method_list = []

    # Counter for outer-most loop
    i = 0
    while (i < no_of_apps):

        # List 1: Application record number
        app_record_no = appcount - jdate_i
        app_num_record_list.append(app_record_no)

        # List 2: Application day since 1900
        app_record_day_since_1900 = appcount
        app_record_day_since_1900_list.append(app_record_day_since_1900)

        # List 3: Application rate
        app_rate = application_rate
        app_rate_list.append(app_rate)

        # List 4: Application method
        app_method = application_method + " "
        app_method_list.append(app_method)

        # Counter for time_window_1 loop
        j = 1
        while (j < int(time_window_1)):
            # List 1: Application record number
            app_record_no = appcount - jdate_i + j
            app_num_record_list.append(app_record_no)

            # List 2: Application day since 1900
            app_record_day_since_1900 = appcount + j
            app_record_day_since_1900_list.append(app_record_day_since_1900)

            # List 3: Application rate
            app_rate = application_rate
            app_rate_list.append(app_rate)

            # List 4: Application method
            app_method = application_method + " "
            app_method_list.append(app_method)

            j += 1

        appcount = appcount + appfreq  # This should be an 'int'

        i += 1

    total_no_of_apps = no_of_apps * int(time_window_1)

    return app_num_record_list, app_record_day_since_1900_list, app_rate_list, app_method_list, total_no_of_apps


def app_refine_uniform_with_step(appcount, no_of_apps, application_rate, application_method, appfreq,
                                 time_window_1, percent_applied_1, time_window_2, percent_applied_2):
    """
        Application Refinement: Uniform Step over Window

        returns: Tuple including the 4 Python lists for app_num_record() method and the total number of applications:
            tuple[0]: app_num_record_list
            tuple[1]: app_record_day_since_1900_list
            tuple[2]: app_rate_list
            tuple[3]: app_method_list
            tuple[4]: total_no_of_apps
    """

    application_rate_1 = float(application_rate) * float(percent_applied_1) / 100. / float(time_window_1)
    application_rate_2 = float(application_rate) * float(percent_applied_2) / 100. / float(time_window_2)

    jdate_i = convert_date_to_days_since_date2(date(1984, 1, 1), date(1900, 1, 1))

    app_num_record_list = []
    app_record_day_since_1900_list = []
    app_rate_list = []
    app_method_list = []

    # Counter for outer-most loop
    i = 0
    while (i < no_of_apps):

        # List 1: Application record number
        app_record_no = appcount - jdate_i
        app_num_record_list.append(app_record_no)

        # List 2: Application day since 1900
        app_record_day_since_1900 = appcount
        app_record_day_since_1900_list.append(app_record_day_since_1900)

        # List 3: Application rate
        app_rate = application_rate_1
        app_rate_list.append(app_rate)

        # List 4: Application method
        app_method = application_method + " "
        app_method_list.append(app_method)

        # Counter for time_window_1 loop
        j = 0
        # Application number tracker for inner loop
        appcount2 = 0
        while (j < int(time_window_1)):
            appcount2 += 1

            # List 1: Application record number
            app_record_no = appcount - jdate_i + appcount2
            app_num_record_list.append(app_record_no)

            # List 2: Application day since 1900
            app_record_day_since_1900 = appcount + appcount2
            app_record_day_since_1900_list.append(app_record_day_since_1900)

            # List 3: Application rate
            app_rate = application_rate_1
            app_rate_list.append(app_rate)

            # List 4: Application method
            app_method = application_method + " "
            app_method_list.append(app_method)

            j += 1

        # Counter for time_window_2 loop
        k = 1
        while (k < int(time_window_2)):
            # List 1: Application record number
            app_record_no = appcount - jdate_i + appcount2 + k
            app_num_record_list.append(app_record_no)

            # List 2: Application day since 1900
            app_record_day_since_1900 = appcount + appcount2 + k
            app_record_day_since_1900_list.append(app_record_day_since_1900)

            # List 3: Application rate
            app_rate = application_rate_2
            app_rate_list.append(app_rate)

            # List 4: Application method
            app_method = application_method + " "
            app_method_list.append(app_method)

            k += 1

        appcount = appcount + appfreq  # This should be an 'int'

        i += 1

    total_no_of_apps = no_of_apps * (int(time_window_1) + int(time_window_2))

    return app_num_record_list, app_record_day_since_1900_list, app_rate_list, app_method_list, total_no_of_apps


def app_refine_triangular(appcount, no_of_apps, application_rate, application_method, appfreq, time_window_1):
    """
        Application Refinement: Triangular over Window

        returns: Tuple including the 4 Python lists for app_num_record() method and the total number of applications:
            tuple[0]: app_num_record_list
            tuple[1]: app_record_day_since_1900_list
            tuple[2]: app_rate_list
            tuple[3]: app_method_list
            tuple[4]: total_no_of_apps
    """

    appm = float(application_rate)
    thalf = int(time_window_1) / 2

    jdate_i = convert_date_to_days_since_date2(date(1984, 1, 1), date(1900, 1, 1))

    app_num_record_list = []
    app_record_day_since_1900_list = []
    app_rate_list = []
    app_method_list = []

    # Counter for outer-most loop
    i = 0
    while (i < no_of_apps):

        # List 1: Application record number
        app_record_no = appcount - jdate_i
        app_num_record_list.append(app_record_no)

        # List 2: Application day since 1900
        app_record_day_since_1900 = appcount
        app_record_day_since_1900_list.append(app_record_day_since_1900)

        # List 3: Application rate
        app_rate = 0.5 * 1 * ((2 * appm) / float(time_window_1)) / float(thalf)
        app_rate_list.append(app_rate)

        # List 4: Application method
        app_method = application_method + " "
        app_method_list.append(app_method)

        # Counter 'j' loop
        j = 1
        # Application number tracker for inner loop
        appcount2 = 0
        while (j < int(thalf)):
            appcount2 += 1

            # List 1: Application record number
            app_record_no = appcount - jdate_i + appcount2
            app_num_record_list.append(app_record_no)

            # List 2: Application day since 1900
            app_record_day_since_1900 = appcount + appcount2
            app_record_day_since_1900_list.append(app_record_day_since_1900)

            # List 3: Application rate
            app_rate = (appm / float(time_window_1) / float(thalf)) * ((j + 1) ** 2 - (j ** 2))
            app_rate_list.append(app_rate)

            # List 4: Application method
            app_method = application_method + " "
            app_method_list.append(app_method)

            j += 1

        # Counter 'k' loop
        k = 1
        while (k < int(thalf)):
            # List 1: Application record number
            app_record_no = appcount - jdate_i + appcount2 + k
            app_num_record_list.append(app_record_no)

            # List 2: Application day since 1900
            app_record_day_since_1900 = appcount + appcount2 + k
            app_record_day_since_1900_list.append(app_record_day_since_1900)

            # List 3: Application rate
            app_rate = (appm / float(time_window_1) / float(thalf)) * (
            ((float(thalf) - k) ** 2) - ((float(thalf) - k - 1) ** 2))
            app_rate_list.append(app_rate)

            # List 4: Application method
            app_method = application_method + " "
            app_method_list.append(app_method)

            k += 1

        appcount = appcount + appfreq  # This should be an 'int'

        i += 1

    total_no_of_apps = no_of_apps * int(time_window_1)

    return app_num_record_list, app_record_day_since_1900_list, app_rate_list, app_method_list, total_no_of_apps


def output_time_avg_options(output_time_avg_option):
    if output_time_avg_option == '1':
        """
            FIX THIS PART
        """
        options = "test"
    else:
        options = '0'

    return options


def inputs_preprocessing(inputs):
    start_datetime_object = datetime.strptime(inputs['sim_date_start'], "%m/%d/%Y")
    end_datetime_object = datetime.strptime(inputs['sim_date_end'], "%m/%d/%Y")

    inputs['sim_date_start_index'] = convert_date_to_days_since_date2(start_datetime_object.date(), date(1984, 1, 1))
    inputs['sim_date_start_since1900'] = convert_date_to_days_since_date2(start_datetime_object.date(),
                                                                          date(1900, 1, 1))
    inputs['sim_date_end_since1900'] = convert_date_to_days_since_date2(end_datetime_object.date(), date(1900, 1, 1))
    inputs['sim_date_1st_year'] = start_datetime_object.year
    inputs['sim_date_1st_month'] = start_datetime_object.month
    inputs['sim_date_1st_day'] = start_datetime_object.day
    inputs['sim_date_last_year'] = end_datetime_object.year
    inputs['sim_no_of_years'] = inputs['sim_date_last_year'] - inputs['sim_date_1st_year'] + 1
    inputs['sim_no_of_days'] = inputs['sim_date_end_since1900'] - inputs['sim_date_start_since1900'] + 1
    inputs['sim_day_index_list'], inputs['sim_day_date_list'] = sim_date_index_list(
        inputs['sim_date_start_since1900'], inputs['sim_date_end_since1900'],
        start_datetime_object)
    inputs['crop_list_no'] = inputs['crop_list_no'].split(',')
    inputs['app_num_record'], inputs['app_record_day_since_1900'], \
    inputs['app_rate'], inputs['app_method'], inputs['total_no_of_apps'] = app_num_record(inputs)
    inputs['output_time_avg_conc'] = output_time_avg_options(inputs['output_time_avg_option'])

    return inputs


def generate_sam_input_file(args, sam_input_file_path):
    """
        Callable to generate 'SAM.inp' input file for 'SuperPRZMpesticide.exe'

        args: JSON string; SAM inputs in JSON format.

        returns: nothing
    """

    inputs = inputs_preprocessing(
        copy.deepcopy(args))  # Create a new copy of args dict to not mess with the original POSTed 'args'

    ####################Start writing input file###################

    myfile = open(sam_input_file_path, 'w')

    try:
        myfile.write(inputs['sim_type'] + "\n")
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Simulation Start Day Index \n" % inputs['sim_date_start_index'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Start Julian Day \n" % inputs['sim_date_start_since1900'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !End Julian Day \n" % inputs['sim_date_end_since1900'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !First year \n" % inputs['sim_date_1st_year'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !First mth \n" % inputs['sim_date_1st_month'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !First day \n" % inputs['sim_date_1st_day'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Last yr \n" % inputs['sim_date_last_year'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !num years \n" % inputs['sim_no_of_years'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Total Number of Simulation Days \n" % inputs['sim_no_of_days'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s \n" % ' '.join(map(str, inputs[
            'sim_day_index_list'])))  # Map the list items to strings and join them together with " " (space); this prints list of strings without quotes around each list item
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s \n" % ' '.join(map(str, inputs[
            'sim_day_date_list'])))  # Map the list items to strings and join them together with " " (space); this prints list of strings without quotes around each list item
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Chemical \n" % inputs['chemical_name'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Number of Crops \n" % inputs['crop_number'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Crop IDs \n" % ' '.join(map(str, inputs['crop_list_no'])))
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s. !Koc or Kd \n" % inputs['koc'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !1=Koc,2=Kd \n" % inputs['coefficient'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s. !Soil Half Life \n" % inputs['soil_metabolism_hl'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Total Number of Apps \n" % inputs['total_no_of_apps'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')

    try:
        myfile.write("%s !Application num_record \n" % ' '.join(map(str, inputs['app_num_record'])))
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Application Julian dates \n" % ' '.join(map(str, inputs['app_record_day_since_1900'])))
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !App mass kg/ha \n" % ' '.join(map(str, inputs['app_rate'])))
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !App Method \n" % ' '.join(map(str, inputs['app_method'])))
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')

    try:
        myfile.write("%s !Output type (1=Daily,2=TimeAvg) \n" % inputs['output_type'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Averaging period (days) \n" % inputs['output_avg_days'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Time-Avg Output Type (1=AvgConcs, 2=ToxExceed) \n" % inputs['output_time_avg_option'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Time-Avg Conc Options Selected \n" % inputs['output_time_avg_conc'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Threshold(ug/L) \n" % inputs['output_tox_value'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write("%s !Threshold Options Selected \n" % inputs['output_tox_thres_exceed'])
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')
    try:
        myfile.write(
            "1 !Output format (1=table,2=map,3=plot/histogram) \n")  # inputs['output_format'] This needs to be fixed to handle all combinations
    except Exception, e:
        print str(e)
        myfile.write(' ---ERROR--- \n')

    myfile.close()

    return inputs[
        'sim_day_index_list']  # , sam_input_file_path  NOT NEEDED; COULD BE USED TO REMOVE HARD CODED STRINGS FROM FORTRAN AND BE PASSED IN AS COMMAND LINE ARH INSTEAD
