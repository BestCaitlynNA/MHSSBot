#!/usr/bin/env python3
import MySQLdb
import secret
import argparse

import Database

def create_database(cnx):
    try:
        command = "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET=UTF8;".format(secret.db_name)
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed creating database: {}".format(err))
        cnx.close()

def create_tables(cnx):
    try:
        command = "CREATE TABLE IF NOT EXISTS " + Database.tables[0] +" ("    \
            + "User_id VARCHAR(20) NOT NULL,"                                \
            + "MonsterHuntHash VARCHAR(64) NOT NULL UNIQUE PRIMARY KEY,"     \
            + "KillTime DATE NOT NULL"                               \
        + ");"
        cnx.cursor().execute(command)
        command = "CREATE TABLE IF NOT EXISTS " + Database.tables[1] + " (   \
            User_id VARCHAR(20) NOT NULL UNIQUE PRIMARY KEY,             \
            Audit BOOLEAN                                           \
        );"
        cnx.cursor().execute(command)
        command = "CREATE TABLE IF NOT EXISTS " + Database.tables[2] + " (   \
            User_id VARCHAR(20) UNIQUE PRIMARY KEY,                      \
            User VARCHAR(36)                                       \
        );"
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed creating tables: {}".format(err))
        cnx.close()

def delete_tables(cnx):
    try:
        for table in Database.tables:
            command = "DROP TABLE IF EXISTS " + table + ";"
            cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed to delete table: {}".format(err))
        cnx.close()

def delete_database(cnx):
    try:
        command = 'DROP DATABASE IF EXISTS ' + secret.db_name + ';'
        cnx.cursor().execute(command)
    except MySQLdb.Error as err:
        print("Failed to delete database: {}".format(err))
        cnx.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up database.')
    parser.add_argument('--create', '-c', action='store_true')
    parser.add_argument('--delete', '-d', action='store_true')
    args = parser.parse_args()
    cnx = Database.connect_to_server()
    if args.create:
        create_database(cnx)
        command = 'USE ' + secret.db_name + ';'
        cnx.cursor().execute(command)
        create_tables(cnx)
    if args.delete:
        delete_database(cnx)
    Database.finalize(cnx)
    exit(1)
