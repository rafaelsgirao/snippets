#!/usr/bin/python3
from discord import Embed, PermissionOverwrite, Intents
from discord.ext import commands
from discord.utils import get
import os
import json
from asyncio import sleep

#Taken from IST Discord Bot v1
# https://github.com/ist-bot-team/ist-discord-bot

intents = Intents.default()
intents.typing = False
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
# Events

@bot.event
async def on_ready():
    print('Bot iniciado com o utilizador {0.user}'.format(bot))
    global guild
    guild = bot.guilds[0]
    global channels

@bot.event
async def on_voice_state_update(user,vc_before,vc_after):
   global guild
   #remove permissions from previous channel first
   if vc_before.channel != None:
        #Skip non join/leave/switch vc channel events
        if vc_before.channel == vc_after.channel:
            return
        vc_txt_before = vc_before.channel.name.lower()
        vc_txt_before = vc_txt_before.replace(" ", "-") + "-vc"
        vc_txt_before = vc_txt_before.replace("+", "plus")
        channel = get(vc_before.channel.category.text_channels, name=vc_txt_before)
        #Txt Channel might not exist the first few times
        if channel != None:
            if len(vc_before.channel.members) == 0:
                await channel.delete()
            else:
                await channel.set_permissions(user, read_messages=False)

   if vc_after.channel != None:
        vc_txt_after = vc_after.channel.name.lower()
        vc_txt_after = vc_txt_after.replace(" ", "-") + "-vc"

        #VC rooms with non valid chars for txt rooms will still fail and create
        #multiple txt channels for each user join
        #Nevertheless, fix VC rooms with a '+' in their name
        vc_txt_after = vc_txt_after.replace("+", "plus")

        channel = get(vc_after.channel.category.text_channels, name=vc_txt_after)
        if channel == None:
            overwrites = {
                guild.default_role: PermissionOverwrite(read_messages=False),
                user: PermissionOverwrite(read_messages=True)
            }
            channel = await vc_after.channel.category.create_text_channel(
                name=vc_txt_after, overwrites=overwrites)
        else:
            await channel.set_permissions(user, read_messages=True)

bot.run(os.environ["ALFARROBA_TOKEN"])
