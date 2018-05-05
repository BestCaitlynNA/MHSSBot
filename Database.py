import MySQLdb

import secret

config = {                      \
  'user': secret.db_user,       \
  'password': secret.db_pass,   \
  'host': secret.db_host,       \
  'database': secret.db_name    \
}

tables = [          \
    'monster_hunt',   \
    'audit',          \
    'user_id'         \
]

def connect_to_server():
    try:
        cnx = MySQLdb.connect(**config)
        return cnx
    except MySQLdb.Error as err:
        if err.errno == errcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)

def finalize(cnx):
    cnx.close()

"""
Pull all users in db
"""
def check_user_requirements(cnx, start_date, end_date):
    try:
        command = "SELECT user_id.User, monster_hunt_count.Tally JOIN((SELECT monster_hunt.User_id as User_id, count(monster_hunt.MonsterHuntHash) as 'Tally' WHERE KillTime BETWEEN(start_date, end_date)) as monster_hunt_count) FULL OUTER JOIN user_id ON monster_hunt_count.User_id=user_id.User_id;"
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed to check user requirements: {}".format(err))

def import_users(cnx, id_list, user_list):
    try:
        command = "INSERT INTO " + user_id + " VALUES "
        for i in range(len(id_list)):
            command += "(" + id_list[i] + ", " + user_list[i] + ")"
        command += ";"
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed to import users: {}".format(err))
        cnx.close()

def insert_monsterhunt(cnx, id_str, monster_hunt_hash_list):
    try:
        command = "INSERT INTO " + tables[0] + " VALUES "
        for monster_hunt_hash in monster_hunt_hash_list:
            command += "(" + id_str + ", " + monster_hunt_hash + ")"
        command += ";"
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed to insert monster hunt entry for id: {} : {}".format(id_str, err))
        cnx.close()

def update_user(cnx, id_str, username):
    try:
        command = "UPDATE " + tables[2]  \
        + "SET User = " + user \
        + "WHERE Id = " + id_str;
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Updating id: {} to username: {} failed {}".format(id_str, username, err))
        cnx.close()
