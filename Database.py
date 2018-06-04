import MySQLdb

import secret

config = {                      \
  'user': secret.db_user,       \
  'password': secret.db_pass,   \
  'host': secret.db_host,       \
  #'database': secret.db_name    \
  'charset': 'utf8'             \
}

# config_db = {                   \
#   'user': secret.db_user,       \
#   'password': secret.db_pass,   \
#   'host': secret.db_host,       \
#   'database': secret.db_name    \
#   'charset': 'utf8'             \
# }

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
        print(err)

def connect_to_server_with_db():
    try:
        #cnx = MySQLdb.connect(**config_db)
        cnx = MySQLdb.connect(user='root', password='root', host='127.0.0.1', database='monsterhunt', charset='utf8')
        return cnx
    except MySQLdb.Error as err:
        print(err)

def finalize(cnx):
    cnx.close()

"""
Pull all users in db
"""
def check_user_requirements(cnx, start_date, end_date):
    try:
        command = "SELECT user_id.User, monster_hunt_count.Tally FROM        (SELECT monster_hunt.User_id as User_id, count(monster_hunt.MonsterHuntHash) as Tally FROM monster_hunt WHERE KillTime BETWEEN '" + start_date + "' and '" + end_date + "' GROUP BY monster_hunt.User_id) as monster_hunt_count RIGHT JOIN user_id ON monster_hunt_count.User_id = user_id.User_id;"
        print(command)
        cursor = cnx.cursor()
        cursor.execute(command)
        return cursor.fetchall()
    except MySQLdb.Error as err:
        print("Failed to check user requirements: {}".format(err))

"""
SELECT user_id.User, monster_hunt_count.Tally FROM
(SELECT monster_hunt.User_id as User_id, count(monster_hunt.MonsterHuntHash) as Tally FROM monster_hunt WHERE KillTime BETWEEN '" + start_date + "' and '" + end_date + "' GROUP BY monster_hunt.User_id) as monster_hunt_count
INNER JOIN user_id ON monster_hunt_count.User_id = user_id.User_id;

SELECT user_id.User, monster_hunt_count.Tally FROM
(SELECT monster_hunt.User_id as User_id, count(monster_hunt.MonsterHuntHash) as Tally FROM monster_hunt WHERE KillTime BETWEEN '2018-05-01' and '2018-05-05' GROUP BY monster_hunt.User_id) as monster_hunt_count
RIGHT JOIN user_id ON monster_hunt_count.User_id = user_id.User_id;
"""

def import_users(cnx, id_list, user_list):
    try:
        command = "REPLACE INTO " + tables[2] + " VALUES "
        for i in range(len(id_list)):
            command += "('" + id_list[i] + "', '" + user_list[i] + "')"
            if i != len(id_list)-1:
                command += ","
        command += ";"
        print(command)
        cnx.cursor().execute(command)
        cnx.commit()
    except MySQLdb.Error as err:
        print("Failed to import users: {}".format(err))
        cnx.close()

def insert_monsterhunt(cnx, id_str, monster_hunt_hash_list, dates):
    try:
        command = "INSERT IGNORE INTO " + tables[0] + " VALUES "
        for i in range(len(monster_hunt_hash_list)):
            command += "('" + id_str + "', '" + monster_hunt_hash_list[i] + "', '" + dates[i] + "')"
            if i != len(monster_hunt_hash_list)-1:
                command += ","
        command += ";"
        print(command)
        cnx.cursor().execute(command)
        cnx.commit()
    except MySQLdb.Error as err:
        print("Failed to insert monster hunt entry for id: {} : {}".format(id_str, err))
        cnx.close()

def update_user(cnx, id_str, username):
    try:
        command = "INSERT INTO " + tables[2] + " VALUES ('" + id_str + ", " + username + "') ON DUPLICATE KEY UPDATE User_id='" + id_str + "' User='" + username + "';"
        cnx.cursor().execute(command)
        cnx.commit()
    except MySQLdb.Error as err:
        print("Updating id: {} to username: {} failed {}".format(id_str, username, err))
        cnx.close()
