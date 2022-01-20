import discord
import ast
import sqlite3

import help

#FIXME: Make the messages sent modifiable
#Things to make the bot send messages

#Sends an embedded message from user sent message
#FIXME: Enable sending embedded message to another channel
async def embed(message):
        
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await help.help_embed(message)
        return

    message_no_command = message.content[-(len(message.content)-7):]
    print(message_no_command)
    content = ast.literal_eval(message_no_command)
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

#Called when message is deleted
def message_deleted(payload):
    dbname = "databases/"+str(payload.guild_id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    #Check and remove any reaction role related data on the message
    cursor.execute("SELECT * FROM reaction_role_messages WHERE message_id='"+str(payload.message_id)+"'")
    message = cursor.fetchone()    
    if message != None:
        cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(payload.message_id)+"'")
        cursor.execute("DROP TABLE '"+str(payload.message_id)+"'")

    db.commit()
    db.close()