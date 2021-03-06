#!/usr/bin/env python3
import asyncio
import discord
import multiprocessing
import errno
import os
import sys
import textwrap
import random

import secret
import ScreenshotProcessing
import Database
import Roles
import Utility
import MHSSException

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
    discord_game = discord.game.Game(name="Keeping track of shekels ($help)", type=0)
    await client.change_presence(game=discord_game,status="Keeping track of shekels ($help)")
    print('Bot ready')

def get_all_users():
    users = []
    for server in client.servers:
        if server.id == secret.server_id:
            for member in server.members:
                if (type(member.roles[0]) != str):
                    member.roles = [role.name for role in member.roles]
                if Utility.check_overlapping_sets(member.roles, Roles.valid_roles):
                    users.append((str(member.name) + '#' + str(member.discriminator), member.id))
    usernames = [user[0] for user in users]
    user_ids = [user[1] for user in users]
    print(len(usernames))
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
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(secret.level_3_conversion)]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range(secret.level_3_conversion)]
            dates += dates2
        if monster_hunt.level == '4':
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(secret.level_4_conversion)]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range (secret.level_4_conversion)]
            dates += dates2
        if monster_hunt.level == '5':
            monster_hunt_hashes2 = [str(hash(monster_hunt)) + str(i) for i in range(secret.level_5_conversion)]
            monster_hunt_hashes += monster_hunt_hashes2
            dates2 = [date_string for _ in range (secret.level_5_conversion)]
            dates += dates2
    #print(monster_hunt_hashes)
    Database.insert_monsterhunt(cnx, user_id, monster_hunt_hashes, dates)

@client.event
async def on_message(message):
    user_id = message.author.id

    # for testing only
    #print(user_id, secret.tester_id)
    # if user_id != secret.tester_id:
    #     return

    # Don't reply to own messages
    if message.author == client.user:
        return
    print("From:", message.author.id, message.content)
    if message.content.startswith("$help"):
        if not Utility.accept_command(message):
            return
        msg = '$help - Display this help message.\n'
        msg += '$ss - Submit a screenshot. Only accepts full screen screenshots as attachment for now.\n'
        msg += '$update_users(DG1_R4 only) - Pull full user list into database.\n'
        msg += "$check_mh (start date)ddmmyyyy (end date)ddmmyyy (DG1_R4 only)- Get list of users that haven't met the requirement in the time period.\n"
        msg = msg.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$hello"):
        if not Utility.accept_command(message):
            return
        roll = random.uniform(0,1)
        print(message.content)
        msg = 'Hello {0.author.mention}'
        autistiny = "<:AUTISTINY:422539124642414592>"
        if (autistiny + " /") in message.content:
            msg = msg + ' \\ ' + autistiny + ' /'
        elif ("<" in message.content and ">" in message.content):
            if roll > 0.5:
                 msg = msg + " " +  message.content[message.content.find("<"):message.content.find(">")+1] + ' /'
        msg = msg.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$kys"):
        if not Utility.accept_admin_command(message):
            print("failed check admin")
            return
        feelsbadman = "<:FeelsBadMan:389698707022544908> 🔫"
        msg = ('Goodbye @everyone ' + feelsbadman).format(message)
        await client.send_message(message.channel, msg)
        print("killing")
        sys.exit()

    if message.content.startswith("$ss"):
        if not Utility.accept_command(message):
            return
        img_url = ScreenshotProcessing.receive(message)
        if img_url is None:
            msg = "No image detected.".format(message)
            await client.send_message(message.channel, msg)
        #download image
        filename = ScreenshotProcessing.download_image(img_url)
        #get the OCR text
        ocr_text = ScreenshotProcessing.ocr(filename)
        valid_hunts = []
        try:
            #parse the ocr text
            valid_hunts, invalid_hunts = ScreenshotProcessing.parse_ocr(ocr_text)
            if len(valid_hunts) > 0:
                insert_monster_hunt_into_db(user_id, valid_hunts)
            if len(invalid_hunts) > 0:
                msg = ("Invalid hunts (0-indexed): " + str(invalid_hunts)).format(message)
                await client.send_message(message.channel, msg)
        except MHSSException.MHSSException as err:
            msg = err.message.format(message)
            await client.send_message(message.channel, msg)
        #Database.update_user(cnx, str(message.author.id), str(message.author))
        msg = "Image received".format(message)
        await client.send_message(message.channel, msg)
        msg = "Number of valid hunts detected: {}".format(len(valid_hunts))
        msg = msg.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$update_users"):
        if not Utility.check_overlapping_sets(message.author.roles, Roles.admin_roles) and not Utility.accept_admin_command(message):
            return
        get_all_users()
        msg = 'Updated users'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$check_mh"):
        command_length = len("$check_mh")
        if (type(message.author.roles[0]) != str):
            message.author.roles = [str(role) for role in message.author.roles]
        if not Utility.check_overlapping_sets(message.author.roles, Roles.admin_roles) and not Utility.accept_admin_command(message):
            # print("User:", message.author, "is not part of dg1_r4, roles are:")
            # for role in message.author.roles:
            #     print(role)
            return
        if len(message.content) != 27:
            msg = "Usage is $check_mh ddmmyyyy(start) ddmmyyyy(end)"
            await client.send_message(message.channel, msg)
            return
        start_date = message.content[command_length+1:command_length + 9]
        end_date = message.content[command_length+10: command_length+18]
        if not Utility.validate_dates(start_date, end_date):
            msg = 'End date must occur after start date'.format(message)
            await client.send_message(message.channel, msg)
        print("Attempting to check mh requirements")
        failed_users =  Utility.get_failed_mh_users(cnx, start_date, end_date)
        failed_users_list = textwrap.wrap(str(failed_users), 1000)
        for failed_user in failed_users_list:
            msg = failed_user.format(message)
            await client.send_message(message.channel, msg)
