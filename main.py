from ast import Global
import access
from pyexpat.errors import messages
import sqlite3
import discord
from decouple import config

import help
from roles import Roles
import messages
import checkdb
import authorization

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
BOT_TOKEN = config('BOT_TOKEN')
is_experimental = False

command_key = "!"           #What the bot uses to recognize commands

checkdb.check_db_folder()

@client.event
async def on_ready():
    #checks if the bot is experimental version.
    print("Checking for experimental...")
    if client.user.id == 932540671988998234: #Replace this with bot id that is the experimental bot
        global is_experimental
        is_experimental = True
        global command_key
        command_key = "?"
        print("Experimental bot. Command key is '"+command_key+"'")
    else:
        print("Normal bot. Command key is '"+command_key+"'")
    print("=========================================================")
    
    #Check and set up the databases
    print("Checking databases...")
    for guild in client.guilds:
        print("----------------------------------------")
        checkdb.check_tables(guild)
        await checkdb.clean_up(guild, is_experimental)

    print("All databases ok!")
    print("=========================================================")

    

    print('we have logged in as {0.user}'.format(client))
    #Check for any guilds that do not exist anymore.
    #Check for any messages that do not exist anymore.

#Listens on events on the server.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_key+"help"):
        await help.help(message)
        return

    if message.content.startswith(command_key+"roles"):
        if authorization.authorize(message, "trusted"):
            await Roles.roles(message)
        return

    if message.content.startswith(command_key+"embed"):
        await messages.embed(message)
        return
    if message.content.startswith(command_key+"access"):
        if authorization.authorize(message, "owner"):
            await access.access(message)
        return
    if message.content.startswith(command_key+"trusted"):
        if authorization.authorize(message, "trusted"):
            print("Is trusted")
        else:
            print("Is not trusted")
    if is_experimental and message.content.startswith(command_key+"print"):
        db = sqlite3.connect("databases/"+str(message.guild.id)+".db")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Tables in the database")
        print("======================================")
        print(str(tables))
        print("======================================")
        for table in tables:
            print(str(table[0]))
            cursor.execute("SELECT * FROM '"+table[0]+"'")
            print(cursor.fetchall())
            print("________________________________")
        db.close()

@client.event
async def on_raw_message_delete(payload):
    messages.message_deleted(payload)

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