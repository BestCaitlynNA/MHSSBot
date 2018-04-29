#!/usr/bin/env python3
import asyncio
import discord
import multiprocessing
import errno
import os
import sys

import secret
import ScreenshotProcessing

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith("$ss"):
        # print("received message")
        # print(message.content)
        # if (len(message.embeds) > 0):
        #     print("This message has an embed")
        # if (len(message.attachments) > 0):
        #     print("This message has an attachement")
        #     print("The url is :" + str(message.attachments[0].get('url')))
        msg = ScreenshotProcessing.receive(message)
        await client.send_message(message.channel, msg)
