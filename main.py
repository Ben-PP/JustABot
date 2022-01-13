import discord
from decouple import config

import help
from roles import Roles
from messages import Messages

client = discord.Client()
BOT_TOKEN = config('BOT_TOKEN')

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))

#Listens on events on the server
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!help"):
        await help.help(message)
    
    if message.content.startswith("!roles"):
        await Roles.roles(message, client)
    
    if message.content.startswith("!embed"):
        await Messages.embed(message)
    
client.run(BOT_TOKEN)