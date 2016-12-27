import sqlite3
import argparse
import sys
import os
import csv

_CURR_PATH = os.path.abspath(os.path.dirname(__file__))
con = sqlite3.connect(os.path.join(_CURR_PATH, "sqliteDB", "ore.s3db"))
cur = con.cursor()
try:
    cur.execute("DROP TABLE OccHandlerNC")
except sqlite3.OperationalError:
    pass
finally:
    cur.execute("CREATE TABLE OccHandlerNC ('Activity', 'Formulation', 'AppEquip', 'AppType', 'Category', "
                "'AppRateUnit', 'TreatedVal', 'TreatedUnit', 'DUESLNoG', 'DUESLG', 'DUEDLG',	'DUESLGCRH', "
                "'DUEDLGCRH', 'DUEEC', 'IUENoR', 'IUEPF5R', 'IUEPF10R', 'IUEEC', 'SourceCategory', 'SourceMRID', "
                "'SourceDescription', 'SourceDER');")

_LOOKUP_TAB_CATEGORIES = ["Orchard/Vineyard", "Field crop, typical", "Field crop, high acreage", "Greenhouse",
                          "Forestry", "Golf course", "Nursery", "Sod"]


# TODO: The LookUpHandler table has less specific "categories" than the OccHandler table; therefore, when the user
# TODO: looks up the category it needs to be related to the more specific category (e.g. using LIKE %<category>%)

# TODO: Create "LookUpHandler" table from the crop-target lookup tab


def main(csv_name):
    the_csv = csv_name + ".csv"

    with open(the_csv, 'rb') as f:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(f)  # comma is default delimiter
        to_db = []
        for i in dr:
            if i['TreatedVal'] != "":  # Only use rows with an "Amount Handled/Area Treated" value given
                to_db.append((i["Activity"], i["Formulation"], i["AppEquip"], i["AppType"], i["Category"],
                              i['AppRateUnit'], i['TreatedVal'], i['TreatedUnit'], i['DUESLNoG'], i['DUESLG'],
                              i['DUEDLG'], i['DUESLGCRH'], i['DUEDLGCRH'], i['DUEEC'], i['IUENoR'], i['IUEPF5R'],
                              i['IUEPF10R'], i['IUEEC'], i['SourceCategory'], i['SourceMRID'], i['SourceDescription'],
                              i['SourceDER'])
                             )

    cur.executemany(
            "INSERT INTO OccHandlerNC VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            to_db)
    con.commit()


if __name__ == '__main__':
    # sys.argv[1]
    main("csv_occhandler_tab")
