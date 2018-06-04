import datetime

import Database
import Roles
import secret

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
    print("Requirement is", mh_requirement)
    rows = Database.check_user_requirements(cnx, start_date, end_date)
    print(rows)
    rows = [row if (row[1] is not None) else (row[0], 0) for row in rows]
    failed = [row for row in rows if row[1] < mh_requirement]
    print(failed)
    return failed
    # for row in rows:
    #     if row[1] < mh_requirement:
    #         failed.append(row)

def check_overlapping_sets(set1, set2):
    return not set(set1).isdisjoint(set2)

def validate_dates(start_date_string, end_date_string):
    return (get_mh_requirement(start_date_string, end_date_string) > 0)

def accept_command(message):
    if (type(message.author.roles[0]) != str):
        message.author.roles = [role.name for role in message.author.roles]
    return check_overlapping_sets(message.author.roles, Roles.valid_roles)

def accept_admin_command(message):
    if (message.author.id == secret.tester_id):
        return True
    return False
