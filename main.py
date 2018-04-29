#!/usr/bin/env python3
import discord

import Control
import secret


#discord.Client().session.close()
try:
    Control.client.run(secret.bot_token)
except KeyboardInterrupt:
    pass
finally:
    Control.client.close()
