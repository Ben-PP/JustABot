import sqlite3
import discord
from decouple import config

import help
from roles import Roles
from messages import Messages

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))
    #TODO: Do clean up for all the databases.
    #Check for any guilds that do not exist anymore.
    #Check for any messages that do not exist anymore.

#Listens on events on the server.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!help"):
        await help.help(message)
        return

    if message.content.startswith("!roles"):
        await Roles.roles(message)
        return

    if message.content.startswith("!embed"):
        await Messages.embed(message)
        return
    if message.content.startswith("!print"):
        db = sqlite3.connect("databases/"+str(message.guild.id)+".db")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(tables)
        print("======================================")
        for table in tables:
            print(str(table))
            cursor.execute("SELECT * FROM '"+table[0]+"'")
            print(cursor.fetchall())
            print("________________________________")
        db.close()

@client.event
async def on_raw_reaction_add(payload):
    bot_id = client.user.id
    if bot_id == payload.user_id:
        return
    await Roles.set_role(payload, client)

@client.event
async def on_raw_reaction_remove(payload):
    bot_id = client.user.id
    if bot_id == payload.user_id:
        return
    await Roles.remove_role(payload, client)
    
client.run(BOT_TOKEN)