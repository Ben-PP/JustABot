from multiprocessing import cpu_count
import sqlite3
import os
from timeit import default_timer as timer

from on_delete import guild_deleted

def checkdb(client, is_experimental):
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
        message_id integer NOT NULL PRIMARY KEY,
        embed_channel_id integer,
        sent_message_id integer,
        sent_channel_id integer
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS access_level (
        role_id integer NOT NULL PRIMARY KEY,
        is_admin text,
        is_trusted text
    )""")
    print("Tables ok!")
    db.commit()
    db.close()


def clean_up(guild, is_experimental):
    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    print("Clean up started...")

    #Clean up for reaction_role_messages
    cursor.execute("SELECT * FROM reaction_role_messages")
    messages = cursor.fetchall()
    for message in messages:
        #If channel has been deleted
        ch = guild.get_channel(message[1])
        if ch == None:
            cursor.execute("DELETE FROM reaction_role_messages WHERE channel_id='"+str(message[1])+"'")
            cursor.execute("DROP TABLE '"+str(message[0])+"'")
            print("No channel found, all messages removed from this channel.")
    #Put here all time consuming clean ups that will be run in the production version.
    #These are not needed on when coding
    if True:
        #FIXME: What if message is deleted when bot is offline?
        cursor.execute("SELECT * FROM reaction_role_messages")
        messages = cursor.fetchall()

        #Checks if all the roles with access level are still on the server
        #TODO: Delete all reaction roles connected
        cursor.execute("SELECT role_id FROM access_level")
        access_roles = cursor.fetchall()
        guild_roles = guild.roles
        is_found = False
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

        #FIXME: Clean up for embedded_messages
    print("Clean up done!")
    db.commit()
    db.close()