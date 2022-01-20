import sqlite3
import os

def check_db_folder():
    if not(os.path.isdir("./databases")):
        os.mkdir("./databases")

def check_tables(guild):
    print("Checking tables of guild: "+str(guild.id))
    dbname = "databases/"+str(guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS active_messages (
        name text NOT NULL PRIMARY KEY,
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

async def clean_up(guild, is_experimental):
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
    if not(is_experimental):
        pass #FIXME: What if message is deleted when bot is offline?
    #FIXME: clean up for access levels. When role is removed.
    #FIXME: Clean up for embedded_messages
    #FIXME: Clean up for guilds that have been deleted while offline
    print("Clean up done!")
    db.commit()
    db.close()