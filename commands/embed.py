from pyexpat.errors import messages
import sqlite3
import discord
import ast

from authorization import authorize
import commands.help as help

#Sends an embedded message from user sent message.
async def embed(message):
    
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await help.help_embed(message)
        return
    elif message_splitted[1] == "onetime":
        if authorize(message, "trusted"):
            await send_embed(message, message_splitted, False)
        return
    elif message_splitted[1] == "save":
        if authorize(message,"admin"):
            await send_embed(message, message_splitted, True)
        return
    elif message_splitted[1] == "list":
        if authorize(message, "trusted"):
            await list_messages(message)
        return
    elif message_splitted[1] == "syntax":
        await help.help_embed_syntax(message)
        return

#Lists all the embedded messages that are saved and can be modified.
async def list_messages(message):
    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM embedded_messages")
    messages = cursor.fetchall()
    if len(messages) < 1:
        await message.channel.send("No embedded messages saved.")
        db.commit()
        db.close()
        return
    urls = []
    await message.channel.send("Here are all the embedded messages that you can edit: \n")
    i = 1
    for msg in messages:
        url = "**Embedded message "+str(i)+".** https://discord.com/channels/"+str(message.guild.id)+"/"+str(msg[1])+"/"+str(msg[0])
        urls.append(url)
        url = "can be edited by editing this message: "+"https://discord.com/channels/"+str(message.guild.id)+"/"+str(msg[3])+"/"+str(msg[2])
        urls.append(url)
        i += 1
    if len(messages) < 5:
        await message.channel.send("\n".join(urls))
    else:
        chunks = [urls[x:x+8] for x in range(0, len(urls), 8)]
        for chunk in chunks:
            await message.channel.send(str("\n".join(chunk)))
    db.commit()
    db.close()

#Sends embedded message to specific channel.
# If is_saved is True, both command message and embedded message are saved
# So they can be edited. If False, no information is saved and editing the
# embedded message is not possible.
async def send_embed(message, message_splitted, is_saved):
    #Checks
    if len(message_splitted) <= 4:
        await message.channel.send("Incorrect ammount of arguments. For help '**!embed help**'")
        return
    channels = message.channel_mentions
    if len(channels) < 1:
        await message.channel.send("No channel mentioned. Remember to **#mention** the channel.")
        return

    channel = channels[0]
    cut_letters = len(message_splitted[0]) + len(message_splitted[1]) + len(message_splitted[2]) + 3
    message_no_command = message.content[-(len(message.content)-cut_letters):]
    sent_message = await send(message_no_command, channel)
    if sent_message == None:
        await message.channel.send("Failed to send embed. Check syntax.")
    else:
        if message.channel != sent_message.channel:
            await message.channel.send("Embed sent! "+sent_message.jump_url)
    #Saves both the command message and sent embedded message so that the
    #embed can be modified later by editing the original command message.
    if is_saved:
        dbname = "databases/"+str(message.guild.id)+".db"
        db = sqlite3.connect(dbname)
        db.execute("PRAGMA foreign_keys=ON")
        cursor = db.cursor()

        cursor.execute("""INSERT INTO embedded_messages (
            embed_message_id,
             embed_channel_id,
              sent_message_id,
              sent_channel_id
              )VALUES(
                  """+str(sent_message.id)+""",
                  """+str(sent_message.channel.id)+""",
                  """+str(message.id)+""",
                  """+str(message.channel.id)+"""
              )""")

        db.commit()
        db.close()

#Sends the embedded message to correct channel.
#Returns Message that was sent or if message can't be sent,
#returns None
async def send(content, channel):
    try:
        content_out = ast.literal_eval(content)
    except:
        return None
    embed = discord.Embed.from_dict(content_out)
    try:
        return await channel.send(embed=embed)
    except:
        #FIXME: Different prints for errors
        return None

#Allows to edit embedded message that bot has sent by editing the original message
#from where the command was given.
async def edit_embed(payload, client):
    dbname = "databases/"+str(payload.guild_id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM embedded_messages WHERE sent_message_id='"+str(payload.message_id)+"'")
    saved_embed = cursor.fetchone()
    if saved_embed == None:
        db.commit()
        db.close()
        return
    guild = client.get_guild(payload.guild_id)
    ch = guild.get_channel(payload.channel_id)
    try:
        edited_message = await ch.fetch_message(payload.message_id)
    except:
        print("Message could not be found.")
    message_splitted = edited_message.content.split(" ")
    cut_letters = len(message_splitted[0]) + len(message_splitted[1]) + len(message_splitted[2]) + 3
    message_no_command = edited_message.content[-(len(edited_message.content)-cut_letters):]
    try:
        print(str(message_no_command))
        content = ast.literal_eval(message_no_command)
    except:
        print("Could not read the content. Syntax error.")
        db.commit()
        db.close()
        return
    embed = discord.Embed.from_dict(content)
    embed_channel = guild.get_channel(saved_embed[1])
    embed_message = await embed_channel.fetch_message(saved_embed[0])
    try:
        await embed_message.edit(embed=embed)
    except:
        print("Could not edit the embed.")

    db.commit()
    db.close()