import requests
from tabulate import tabulate


def build_table(list1, list2):
    # function builds a two column table containing url's and status codes
    report = [""] * len(list1)
    for idx, item in enumerate(list1):
        report[idx] = [list1[idx], list2[idx]]
    return report

def write_report(test_name, assert_error, col1, col2):
    if assert_error:
        print test_name + "Test failed for one or more instances"
        report = build_table(col1, col2)
        headers = ["expected", "actual"]
        print tabulate(report, headers, tablefmt='grid')
    else:
        print test_name + "Test completed successfully"
        report = build_table(col1, col2)
        headers = ["expected", "actual url or status"]
        print tabulate(report, headers, tablefmt='grid')
    return