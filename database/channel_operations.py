import sqlite3
import discord

def remove_channel(channel):
    dbname = "databases/"+str(channel.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    #Removes text channel from database
    if channel.type == discord.ChannelType.text:
        cursor.execute("DELETE FROM guild_channels WHERE channel_id='"+str(channel.id)+"'")

    db.commit()
    db.close()

def add_channel(channel):
    dbname = "databases/"+str(channel.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    #Adds text channel to database
    if channel.type == discord.ChannelType.text:
        cursor.execute("INSERT INTO guild_channels (channel_id) VALUES ('"+str(channel.id)+"')")

    db.commit()
    db.close()