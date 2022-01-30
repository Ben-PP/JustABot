import commands.access as access
import sqlite3
import discord
from decouple import config
from timeit import default_timer as timer
import os

import checkdb
import authorization

import commands.help
from commands.roles import Roles
import commands.embed as embed
import commands.access as access
import commands.menu as menu

import database.message_operations as message_operations
import database.channel_operations as channel_operations
import database.role_operations as role_operations

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
BOT_TOKEN = config('BOT_TOKEN')
is_experimental = False

command_key = "!"           #What the bot uses to recognize commands

checkdb.check_db_folder()

@client.event
async def on_ready():
    global is_experimental
    #checks if the bot is experimental version.
    print("Checking for experimental...")
    if client.user.id == 932540671988998234: #Replace this with bot id that is the experimental bot
        is_experimental = True
        global command_key
        command_key = "?"
        print("Experimental bot. Command key is '"+command_key+"'")
    else:
        print("Normal bot. Command key is '"+command_key+"'")
    print("=========================================================")
    
    #Check and set up the databases
    print("Checking databases...")
    start = timer()
    await checkdb.checkdb(client)
    end = timer()
    print("=========================================================")
    print("All databases ok!")
    print("Total elapsed time: "+str(end-start))
    print("=========================================================")

    

    print('Logged in as {0.user}'.format(client))

#Listens on events on the server.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_key+"help"):
        await commands.help.help(message)
        return

    if message.content.startswith(command_key+"roles"):
        if authorization.authorize(message, "trusted"):
            await Roles.roles(message)
        return

    if message.content.startswith(command_key+"embed"):
        await embed.embed(message)
        return
    if message.content.startswith(command_key+"access"):
        if authorization.authorize(message, "owner"):
            await access.access(message)
        return
    if message.content.startswith(command_key+"menu"):
        await menu.menu(message)

    if message.content.startswith(command_key+"print"):
        if authorization.authorize(message, "admin"):
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
async def on_guild_remove(guild):
    if os.path.exists("databases/"+guild.id+".db"):
        os.remove("databases/"+guild.id+".db")

#When channel is created or deleted.
@client.event
async def on_guild_channel_delete(channel):
    channel_operations.remove_channel(channel)
@client.event
async def on_guild_channel_create(channel):
    channel_operations.add_channel(channel)

#When message is deleted or edited.
@client.event
async def on_raw_message_delete(payload):
    message_operations.remove_message(payload)
@client.event
async def on_raw_message_edit(payload):
    await embed.edit_embed(payload, client)

#When role is created or deleted.
@client.event
async def on_guild_role_delete(role):
    role_operations.remove_role(role)
@client.event
async def on_guild_role_create(role):
    role_operations.add_role(role)

#When reaction is added or removed.
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