#!/usr/bin/env python3
import asyncio
import discord
import multiprocessing
import errno
import os
import sys
import textwrap

import secret
import ScreenshotProcessing
import Database
import Roles
import Utility

client = discord.Client()
cnx = Database.connect_to_server_with_db()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    print('Connected to following servers:')
    for server in client.servers:
        print('Name: ', server.name, ' ID: ', server.id)
        for role in server.roles:
            pass
            #print(role)
        if server.id == secret.server_id:
            for member in server.members:
                pass
                # print('Name: ', member.name, member.discriminator, 'ID: ', member.id)
    if cnx is None:
        print('Bot could not connect to database')
        exit(1)
    print('Bot ready')

def get_all_users():
    users = []
    for server in client.servers:
        if server.id == secret.server_id:
            for member in server.members:
                if (type(member.roles) != str):
                    member.roles = [role.name for role in member.roles]
                if not set(member.roles).isdisjoint(Roles.valid_roles):
                    users.append((str(member.name) + '#' + str(member.discriminator), member.id))
    usernames = [user[0] for user in users]
    user_ids = [user[1] for user in users]
    Database.import_users(cnx, user_ids, usernames)

def insert_monster_hunt_into_db(user_id, monster_hunt_list):
    monster_hunt_hashes = []
    dates = []
    # TODO: Refactor this
    for monster_hunt in monster_hunt_list:
        date = monster_hunt.date
        date_string = "20" + date[6:] + "-" + date[0:2] + "-" + date[3:5]
        if monster_hunt.level == '1':
            continue
        if monster_hunt.level == '2':
            monster_hunt_hashes.append(str(hash(monster_hunt)))
            dates.append(date_string)
        if monster_hunt.level == '3':
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(2**(3-2))]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range (2**(3-2))]
            dates += dates2
        if monster_hunt.level == '4':
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(2**(4-2))]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range (2**(4-2))]
            dates += dates2
        if monster_hunt.level == '5':
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(2**(5-2))]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range (2**(5-2))]
            dates += dates2
    #print(monster_hunt_hashes)
    Database.insert_monsterhunt(cnx, user_id, monster_hunt_hashes, dates)

@client.event
async def on_message(message):
    user_id = message.author.id

    # for testing only
    #print(user_id, secret.tester_id)
    if user_id != secret.tester_id:
        return

    # Don't reply to own messages
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$ss"):
        img_url = ScreenshotProcessing.receive(message)
        filename = ScreenshotProcessing.download_image(img_url)
        ocr_text = ScreenshotProcessing.ocr(filename)
        valid_hunts = ScreenshotProcessing.parse_ocr(ocr_text)
        insert_monster_hunt_into_db(user_id, valid_hunts)
        #Database.update_user(cnx, str(message.author.id), str(message.author))
        msg = "Image received".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$update_users"):
        get_all_users()

    if message.content.startswith("$check_mh"):
        command_length = len("$check_mh")
        #print(start_date)
        #print(end_date)
        # print(len(message.content))
        if len(message.content) != 27:
            msg = "Usage is $check_mh ddmmyyyy(start) ddmmyyyy(end)"
            await client.send_message(message.channel, msg)
            return
        start_date = message.content[command_length+1:command_length + 9]
        end_date = message.content[command_length+10: command_length+18]
        failed_users =  Utility.get_failed_mh_users(cnx, start_date, end_date)
        failed_users_list = textwrap.wrap(str(failed_users), 1000)
        for failed_user in failed_users_list:
            msg = failed_user.format(message)
            await client.send_message(message.channel, msg)

def validate_dates():
    pass
