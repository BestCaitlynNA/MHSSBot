import datetime

import Database

def convert_string_to_date(date_string):
    return datetime.datetime.strptime(date_string, "%d%m%Y").date()

def get_mh_requirement(start_date_string, end_date_string):
    start_date = convert_string_to_date(start_date_string)
    end_date = convert_string_to_date(end_date_string)
    return ((end_date - start_date).days+1) * 3

def convert_to_db_date(date_string):
    return date_string[4:] + "-" + date_string[2:4] + "-" + date_string[:2]

def get_failed_mh_users(cnx, start_date_string, end_date_string):
    mh_requirement = get_mh_requirement(start_date_string, end_date_string)
    start_date = convert_to_db_date(start_date_string)
    end_date = convert_to_db_date(end_date_string)
    rows = Database.check_user_requirements(cnx, start_date, end_date)
    #print(rows)
    failed = []
    failed = [row for row in rows if row[1] < mh_requirement]
    return failed
    # for row in rows:
    #     if row[1] < mh_requirement:
    #         failed.append(row)
