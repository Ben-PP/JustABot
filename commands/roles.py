import sqlite3
import commands.help as help

#Everything related to role creating with the bot.

class Roles:
    db = None
    cursor = None


    #TODO: When Python 3.10 available, replace message_splitted with match-case and make arguments into class attributes
    #Default method called when user writes message that starts with '!roles'.
    #Here the message is also split and searched for further commands.
    async def roles(message):
        #Checks if the db is used by another command and waits for it to finnish
        dbname = "databases/"+str(+message.guild.id)+".db"
        Roles.db = sqlite3.connect(dbname)
        Roles.cursor = Roles.db.cursor()

        message_splitted = message.content.split(" ")
        if len(message_splitted) <= 1 or message_splitted[1] == "help":
            await help.help_roles(message)
        elif message_splitted[1] == "add":
            await Roles.add_reactionrole(message, message_splitted)
        elif message_splitted[1] == "remove":
            await Roles.remove_reactionrole(message, message_splitted)
        elif message_splitted[1] == "set":
            await Roles.set_channel_message(message, message_splitted)
        elif message_splitted[1] == "list":
            await Roles.show_messages(message)
        else:
            await message.channel.send("Unknown command '**"+message_splitted[1]+"**'.\nType '**!roles help**' for more commands.")

        Roles.db.commit()
        Roles.db.close() 

        #Sends a list of all the messages containing at least 1 reaction role
    async def show_messages(message):

        Roles.cursor.execute("SELECT * FROM reaction_role_messages")
        messages = Roles.cursor.fetchall()
        if len(messages) < 1:
            await message.channel.send("No messages with reaction roles.")
            return
        urls = []
        urls.append("Messages that have a reaction role/roles are:\n")
        ch = None
        i = 1
        for msg in messages:
            ch = message.guild.get_channel(msg[1])
            url = str(i)+". https://discord.com/channels/"+str(message.guild.id)+"/"+str(ch.id)+"/"+str(msg[0])
            urls.append(url)
            i += 1
        if len(messages) < 9:
            await message.channel.send("\n".join(urls))
        else:
            chunks = [urls[x:x+8] for x in range(0, len(urls), 8)]
            for chunk in chunks:
                await message.channel.send(str("\n".join(chunk)))

    #Adds reaction to specified message and connects a role to it.
    async def add_reactionrole(message, message_splitted):

        active_message = None
        active_channel = None
        actives = None
        #Loads actives.
        try:
            Roles.cursor.execute("""
                SELECT * FROM active_messages WHERE name='roles'
            """)
            actives = Roles.cursor.fetchone()
        except:
            await message.channel.send("No message or channel is set active!")
            return
        #Loads active_channel.
        try:
            active_channel = message.guild.get_channel(int(actives[1]))
        except:
            await message.channel.send("No active channel found!")
            return
        #Loads active_message.
        try:
            active_message = await active_channel.fetch_message(actives[2])
        except:
            await message.channel.send("No active message found.")
            return

        #checks
        if len(message_splitted) < 4:
            await message.channel.send("Not enough arguments on the message!\nYou must firs provide an emoji, and after that provide the role!")
            return

        used_emoji = message_splitted[2]
        try:
            await active_message.add_reaction(used_emoji)
        except:
            await message.channel.send("'"+used_emoji+"' emoji not valid.")
            return

        role_id= None
        try:
            role_id = int(message_splitted[3][3:(len(message_splitted[3])-1)])
        except:
            await message.channel.send("Role is not valid!")
            await active_message.clear_reaction(used_emoji)
            return
        role = message.guild.get_role(role_id)
        if role == None:
            await message.channel.send("Role is not valid!")
            await active_message.clear_reaction(used_emoji)
            return

        message_id = str(active_message.id)

        #Adds the role to this reaction on this message if the emoji is not on the message allready.
        Roles.cursor.execute("CREATE TABLE IF NOT EXISTS '"+ message_id +"' (emoji text, role_id integer, channel_id integer)")

        #Checks if the emoji is allready connected to a role in this message.
        Roles.cursor.execute("SELECT * FROM '"+message_id+"' WHERE emoji = '"+used_emoji+"'")
        items = Roles.cursor.fetchall()
        if len(items) >= 1:
            await message.channel.send("This reaction allready has a role attached to it. Please choose another reaction or delete the old one.")
            return

        Roles.cursor.execute("INSERT INTO '"+message_id+"' VALUES ('"+used_emoji+"',"+str(role_id)+","+str(active_message.id)+")")
        Roles.cursor.execute("""INSERT OR REPLACE INTO reaction_role_messages (
            message_id,
            channel_id)VALUES(
                """+message_id+""",
                """+str(active_channel.id)+"""
            )
        """)
        #Adds the message, channel and other info to table for dbcheck.
        Roles.cursor.execute("""INSERT OR REPLACE INTO used_messages (
            message_id,
            channel_id)VALUES(
                """+message_id+""",
                """+str(active_channel.id)+"""
            )""")
        try:
            await message.channel.send("Succesfully added "+used_emoji+" with role <@&"+str(role_id)+"> to message: "+message_id, reference=active_message)
        except:
            await message.channel.send("Succesfully added "+used_emoji+" with role <@&"+str(role_id)+"> to message: "+ active_message.jump_url)

    #Deletes reaction from message and removes the connection to a role.
    async def remove_reactionrole(message, message_splitted):
        active_message = None
        active_channel = None
        actives = None
        #Loads actives.
        try:
            Roles.cursor.execute("""
                SELECT * FROM active_messages WHERE name='roles'
            """)
            actives = Roles.cursor.fetchone()
        except:
            await message.channel.send("No message or channel is set active!")
            return
        #Loads active_channel.
        try:
            active_channel = message.guild.get_channel(int(actives[1]))
        except:
            await message.channel.send("No active channel found!")
            return
        #Loads active_message.
        try:
            active_message = await active_channel.fetch_message(actives[2])
        except:
            await message.channel.send("No active message found.")
            return

        #checks
        if len(message_splitted) != 3:
            await message.channel.send("Incorrect ammount of arguments\nCheck **!roles help** for usage.")
            return

        used_emoji = str(message_splitted[2])
        try:
            await active_message.clear_reaction(used_emoji)
        except:
            await message.channel.send("'"+used_emoji+"' emoji not valid.")
            return

        message_id = str(active_message.id)
        Roles.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+str(message_id)+"'")
        table = Roles.cursor.fetchone()
        if table == None:
            try:
                await message.channel.send("No reaction roles has been set to the message: "+message_id, reference=active_message)
            except:
                await message.channel.send("No reaction roles has been set to the message: "+ active_message.jump_url)
            return
        #Removes reaction from the database.
        Roles.cursor.execute("DELETE FROM '"+message_id+"' WHERE emoji='"+used_emoji+"'")
        Roles.cursor.execute("SELECT * FROM '"+message_id+"'")
        #If last reaction from the message is removed, drop the table for that message.
        messages = Roles.cursor.fetchall()
        if len(messages) < 1:
            Roles.cursor.execute("DROP TABLE '"+message_id+"'")
            Roles.cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+message_id+"'")
            Roles.cursor.execute("SELECT * FROM embedded_messages WHERE embed_message_id='"+str(message_id)+"' or sent_message_id='"+str(message_id)+"'")
            if len(Roles.cursor.fetchall()) < 1:
                Roles.cursor.execute("DELETE FROM used_messages WHERE message_id='"+message_id+"'")

    #Sets the active channel and message for !roles commands to the database.
    async def set_channel_message(message, message_splitted):
        ch = message.channel_mentions

        #Checks if channel mention is found on the message
        if len(ch) < 1:
            await message.channel.send("No channel mentioned on the message!\n Check **!roles help** for more info.")
            return
        #Checks the number of arguments.
        if len(message_splitted) != 4:
            await message.channel.send("Incorrect ammount of arguments!\n Check **!roles help** for more info.")
            return
        try:
            message_id = int(message_splitted[3])
        except:
            await message.channel.send("Message id was not valid!")
            return
        active_message = None
        #Tries to fetch the message from the channel.
        try:
            active_message = await ch[0].fetch_message(message_id)
        except:
            await message.channel.send("No such message found from <#"+str(ch[0].id)+">\n Make sure that your message is from this channel.")
            return

        Roles.cursor.execute("""INSERT OR REPLACE INTO active_messages (name, active_channel_id,active_message_id)
                                VALUES(
                                    'roles',
                                    """+str(ch[0].id)+""",
                                    """+str(active_message.id)+"""
                                )
                                """)
        if message.channel.id == ch[0].id:
            await message.channel.send("Channel has been set to: <#"+str(ch[0].id)+">\nMessage has been set to: "+str(message_id), reference=active_message)
        else:
            await message.channel.send("Channel has been set to: <#"+str(ch[0].id)+">\nMessage has been set to: "+str(message_id)+": "+active_message.jump_url)

    #Sets correct role for user according to with what he reacted.
    async def set_role(payload,client):
        dbname = "databases/"+str(payload.guild_id)+".db"
        db = sqlite3.connect(dbname)
        cursor = db.cursor()

        message_id = str(payload.message_id)
        used_emoji = str(payload.emoji)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+message_id+"'")
        if len(cursor.fetchall()) < 1:
            db.commit()
            db.close()
            return
        cursor.execute("SELECT * FROM '"+message_id+"' WHERE emoji='"+used_emoji+"'")
        items = cursor.fetchone()
        if items == None or len(items) < 1:
            db.commit()
            db.close()
            return

        role_id = items[1]

        guild = client.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        if role != None:
            await user.add_roles(role)
        else:
            #Deletes the reaction role from database if the role does not exist.
            cursor.execute("DELETE FROM '"+str(payload.message_id)+"' WHERE emoji='"+str(payload.emoji)+"'")
            cursor.execute("SELECT * FROM '"+str(payload.message_id)+"'")
            messages = cursor.fetchall()
            if len(messages) < 1:
                #If its the last reaction in the message
                cursor.execute("DROP TABLE '"+str(payload.message_id)+"'")
                cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(payload.message_id)+"'")
                cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(payload.message_id)+"'")
            print("---------------------------------------")
            print("Role does not exist anymore. Reaction role deleted from the message.")
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.clear_reaction(used_emoji)

        db.commit()
        db.close()

    #Removes correct role from the user according to with what he reacted.
    async def remove_role(payload, client):
        dbname = "databases/"+str(payload.guild_id)+".db"
        db = sqlite3.connect(dbname)
        cursor = db.cursor()

        message_id = str(payload.message_id)
        used_emoji = str(payload.emoji)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+message_id+"'")
        if len(cursor.fetchall()) < 1:
            db.commit()
            db.close()
            return
        cursor.execute("SELECT * FROM '"+message_id+"' WHERE emoji='"+used_emoji+"'")
        items = cursor.fetchone()
        if items == None or len(items) < 1:
            db.commit()
            db.close()
            return

        role_id = items[1]

        guild = client.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        if role != None:
            await user.remove_roles(role)
        else:
            #If the role does not exist anymore, this removes it from the database
            cursor.execute("DELETE FROM '"+str(payload.message_id)+"'WHERE emoji='"+str(payload.emoji)+"'")
            cursor.execute("SELECT * FROM '"+str(payload.message_id)+"'")
            messages = cursor.fetchall()
            if len(messages) < 1:
                #If its the last reaction in the message
                cursor.execute("DROP TABLE '"+str(payload.message_id)+"'")
                cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(payload.message_id)+"'")
                cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(payload.message_id)+"'")

            print("-----------------------------------")
            print("Role does not exist anymore. Reaction role deleted from the message.")
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.clear_reaction(used_emoji)

        db.commit()
        db.close()