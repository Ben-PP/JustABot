import discord
import sqlite3
import os
from timeit import default_timer as timer

import database.channel_operations as channel_operations

async def checkdb(client):
    #Check for deleted guilds
    print("Checking for deleted guilds...")
    files = os.listdir("databases/")
    guilds = client.guilds
    for file in files:
        file_exists = False
        for guild in guilds:
            if str(guild.id)+".db" == file:
                file_exists = True
                break
        if not(file_exists):
            print("Non existing server found and removed.")
            os.remove("databases/"+file)
    print("Deleted guilds ok!")

    for guild in client.guilds:
        print("----------------------------------------")
        start = timer()
        check_tables(guild)
        await clean_up(guild)
        end = timer()
        print("Elapsed time: "+str(end-start))

def check_db_folder():
    if not(os.path.isdir("./databases")):
        os.mkdir("./databases")

#Checks for needed tables and creates them if needed.
def check_tables(guild):
    print("Checking tables of guild: "+str(guild.id))
    start = timer()

    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS active_messages (
        name text PRIMARY KEY,
        active_channel_id integer,
        active_message_id integer
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS guild_roles (
        role_id integer NOT NULL PRIMARY KEY
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS guild_channels (
        channel_id integer NOT NULL PRIMARY KEY
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS reaction_role_messages (
        message_id integer NOT NULL,
        emoji text NOT NULL,
        channel_id integer,
        role_id integer,
        PRIMARY KEY(message_id, emoji),
        FOREIGN KEY(channel_id) REFERENCES guild_channels(channel_id) ON DELETE CASCADE,
        FOREIGN KEY(role_id) REFERENCES guild_roles(role_id) ON DELETE CASCADE
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS embedded_messages (
        embed_message_id integer NOT NULL PRIMARY KEY,
        embed_channel_id integer,
        sent_message_id integer,
        sent_channel_id integer,
        FOREIGN KEY(embed_channel_id) REFERENCES guild_channels(channel_id) ON DELETE CASCADE,
        FOREIGN KEY(sent_channel_id) REFERENCES guild_channels(channel_id) ON DELETE CASCADE
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS access_level (
        role_id integer NOT NULL PRIMARY KEY,
        is_admin text,
        is_trusted text,
        FOREIGN KEY(role_id) REFERENCES guild_roles(role_id) ON DELETE CASCADE
    )""")

    print("Updating tables...")

    #Check guild_roles.
    cursor.execute("SELECT * FROM guild_roles")
    saved_role_ids = cursor.fetchall()
    current_roles = guild.roles
    if len(saved_role_ids) < 1:
        for role in guild.roles:
            cursor.execute("INSERT INTO guild_roles (role_id) VALUES('"+str(role.id)+"')")
            cursor.execute("SELECT * FROM guild_roles")
            saved_role_ids = cursor.fetchall()
    #Check for any deleted roles.
    for saved_role_id in saved_role_ids:
        if guild.get_role(saved_role_id[0]) == None:
            cursor.execute("DELETE FROM guild_roles WHERE role_id='"+str(saved_role_id[0])+"'")
        else:
            current_roles.remove(guild.get_role(saved_role_id[0]))
    #Add any new roles.
    if len(current_roles) > 0:
        for role in current_roles:
            cursor.execute("INSERT INTO guild_roles (role_id) VALUES ("+str(role.id)+")")

    #Check guild_channels.
    cursor.execute("SELECT * FROM guild_channels")
    saved_channel_ids = cursor.fetchall()
    current_channels = guild.text_channels
    if len(saved_channel_ids) < 1:
        for channel in guild.text_channels:
            cursor.execute("INSERT INTO guild_channels (channel_id) VALUES ("+str(channel.id)+")")
            cursor.execute("SELECT * FROM guild_channels")
            saved_channel_ids = cursor.fetchall()
    #Check for any deleted channels.
    for saved_channel_id in saved_channel_ids:
        if guild.get_channel(saved_channel_id[0]) == None:
            cursor.execute("DELETE FROM guild_channels WHERE channel_id="+str(saved_channel_id[0])+"")
        else:
            current_channels.remove(guild.get_channel(saved_channel_id[0]))
    #Add any new channels.
    if len(current_channels) > 0:
        for channel in current_channels:
            cursor.execute("INSERT INTO guild_channels (channel_id) VALUES ("+str(channel.id)+")")

    end = timer()
    print("Tables ok!")
    print("Elapsed time: "+str(end-start))
    db.commit()
    db.close()


async def clean_up(guild):
    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    print("Clean up started...")

    print("Cleaning messages...")
    start = timer()

    #reaction_role_messages
    cursor.execute("SELECT DISTINCT message_id,channel_id FROM reaction_role_messages")
    messages = cursor.fetchall()
    for message in messages:
        print("Checking reaction_role_messages...")
        ch = guild.get_channel(message[1])
        if ch == None:
            print("No channel found")
        else:
            try:
                msg = await ch.fetch_message(message[0])
            except discord.NotFound:
                cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(message[0])+"'")
                print("Message not found. Message deleted from database.")
            except discord.HTTPException:
                print("HTTP exception. Could not retrieve the message or messages.")
            except:
                pass

    #embedded_messages
    cursor.execute("SELECT * FROM embedded_messages")
    messages = cursor.fetchall()
    for message in messages:
        print("Checking embedded_messages...")
        ch = guild.get_channel(message[1])
        if ch == None:
            print("No channel found")
        else:
            try:
                msg = await ch.fetch_message(message[0])
            except discord.NotFound:
                cursor.execute("DELETE FROM embedded_messages WHERE embed_message_id='"+str(message[0])+"'")
                print("Message not found. Message deleted from database.")
            except discord.HTTPException:
                print("HTTP exception. Could not retrieve the message or messages.")
            except:
                pass

        ch = guild.get_channel(message[3])
        if ch == None:
            print("No channel found")
        else:
            try:
                msg = await ch.fetch_message(message[2])
            except discord.NotFound:
                cursor.execute("DELETE FROM embedded_messages WHERE sent_message_id='"+str(message[2])+"'")
                print("Message not found. Message deleted from database.")
            except discord.HTTPException:
                print("HTTP exception. Could not retrieve the message or messages.")
            except:
                pass
            

    end = timer()
    print("Time used to clean messages: "+str(end-start))

    print("Clean up done!")
    db.commit()
    db.close()