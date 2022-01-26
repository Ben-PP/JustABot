import sqlite3
import os
from timeit import default_timer as timer

import database.remove_channel as remove_channel

def checkdb(client, is_experimental):
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
        clean_up(guild, is_experimental)
        end = timer()
        print("Elapsed time: "+str(end-start))

def check_db_folder():
    if not(os.path.isdir("./databases")):
        os.mkdir("./databases")

#Checks for needed tables and creates them if needed.
def check_tables(guild):
    print("Checking tables of guild: "+str(guild.id))
    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS active_messages (
        name text PRIMARY KEY,
        active_channel_id integer,
        active_message_id integer
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS reaction_role_messages (
        message_id integer NOT NULL PRIMARY KEY,
        channel_id integer
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS embedded_messages (
        embed_message_id integer NOT NULL PRIMARY KEY,
        embed_channel_id integer,
        sent_message_id integer,
        sent_channel_id integer
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS access_level (
        role_id integer NOT NULL PRIMARY KEY,
        is_admin text,
        is_trusted text
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS used_messages (
        message_id integer NOT NULL PRIMARY KEY,
        channel_id integer
    )""")
    print("Tables ok!")
    db.commit()
    db.close()


def clean_up(guild, is_experimental):
    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    print("Clean up started...")

    #Put here all time consuming clean ups that will be run in the production version.
    #These are not needed on when coding
    if True:
        #Clean up for deleted channels
        print("Checking channels...")
        cursor.execute("SELECT DISTINCT channel_id FROM used_messages")
        channel_ids = cursor.fetchall()
        for channel_id in channel_ids:
            channel = guild.get_channel(channel_id[0])
            if channel == None:
                print("Deleted channel found. Removing...")
                remove_channel.remove_channel(guild.id, channel_id[0])
        print("Channels ok.")

        #Clean up for deleted roles
        #FIXME: Delete all reaction roles connected
        cursor.execute("SELECT role_id FROM access_level")
        access_roles = cursor.fetchall()
        guild_roles = guild.roles
        
        for access_role in access_roles:
            is_found = False
            for guild_role in guild_roles:
                if access_role[0] == guild_role.id:
                    is_found = True
                    break
            print(str(is_found))
            if not(is_found):
                print("Deleted role found! Role deleted from access level table.")
                cursor.execute("DELETE FROM access_level WHERE role_id='"+str(access_role[0])+"'")

        db.commit()
        db.close()
        return

        #FIXME: What if message is deleted when bot is offline?
        cursor.execute("SELECT * FROM reaction_role_messages")
        messages = cursor.fetchall()

        #FIXME: Clean up for embedded_messages
        cursor.execute("SELECT * FROM embedded_messages")
        embedded_messages = cursor.fetchall()
        for embedded_message in embedded_messages:
            embed_is_found = False
            sent_is_found = False

            for guild_channel in guild.channels:
                if embedded_message[1] == guild_channel.id:
                    embed_is_found = True
                if embedded_message[3] == guild_channel.id:
                    sent_is_found = True
                if embed_is_found and sent_is_found:
                    break
            if not(embed_is_found) and not(sent_is_found):
                print("Deleted channel found")

    print("Clean up done!")
    db.commit()
    db.close()