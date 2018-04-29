#!/usr/bin/env python3
import asyncio
import discord
import multiprocessing
import errno
import os
import sys

import secret

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
