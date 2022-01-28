import sqlite3
import commands.help as help

async def access(message):
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1:
        await help.help_access(message)
    elif message_splitted[1] == "help":
        await help.help_access(message)
    elif message_splitted[1] == "add":
        await add(message, message_splitted)
    elif message_splitted[1] == "remove":
        await remove(message, message_splitted)
    elif message_splitted[1] == "list":
        await list_roles(message)
    else:
        await message.channel.send("Unknown command '**"+message_splitted[1]+"**'.\nType '**!roles help**' for more commands.")

#Adds roles to access levels.
async def add(message, message_splitted):

    #Checks
    if len(message_splitted) != 4:
        await message.channel.send("Incorrect ammount of arguments!")

    if message_splitted[3] != "admin" and message_splitted[3] != "trusted":
        await message.channel.send("Please, give a valid access level. Levels are typed all lower case. For all the levels, check **!access help**")
        return

    role_id = None
    try:
        role_id = int(message_splitted[2][3:(len(message_splitted[2])-1)])
    except:
        await message.channel.send("Role is not valid!1")
        return
    role = message.guild.get_role(role_id)
    if role == None:
        await message.channel.send("Role is not valid!2")
        return

    #Adding to database
    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()
    
    if message_splitted[3] == "admin":
        cursor.execute("""INSERT OR REPLACE INTO access_level (
            role_id,
            is_admin,
            is_trusted) VALUES(
                """+str(role_id)+""",
                'True',
                'True'
            )
        """)
        await message.channel.send("<@&"+str(role_id)+"> started a power trip as **admin**!")
    elif message_splitted[3] == "trusted":
        cursor.execute("""INSERT OR REPLACE INTO access_level (
            role_id,
            is_admin,
            is_trusted) VALUES(
                """+str(role_id)+""",
                'False',
                'True'
            )
        """)
        await message.channel.send("<@&"+str(role_id)+"> is now **trusted** definately not sus...")
    db.commit()
    db.close()

#Removes roles from access levels.
async def remove(message, message_splitted):

    #Checks
    if len(message_splitted) != 3:
        return
    role_id = None
    try:
        role_id = int(message_splitted[2][3:(len(message_splitted[2])-1)])
    except:
        await message.channel.send("Role is not valid!")
    role = message.guild.get_role(role_id)
    if role == None:
        await message.channel.send("Role is not valid!")

    #Removing from database
    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM access_level WHERE role_id='"+str(role_id)+"'")
    role = cursor.fetchone()
    if role == None:
        await message.channel.send("This role does not have any access levels!")
    
    cursor.execute("DELETE FROM access_level WHERE role_id='"+str(role_id)+"'")

    #Respond according to what type of access level the role had.
    if role[1] == "True":
        await message.channel.send("<@&"+str(role_id)+"> Went on a trip too far and no more has **admin** access.")
    else:
        await message.channel.send("<@&"+str(role_id)+"> Was not worthy and got their **trusted** access revoked.")

    db.commit()
    db.close()

#Lists all the access levels and what roles are connected to them.
async def list_roles(message):
    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM access_level")
    high_level_roles = cursor.fetchall()
    admins = list()
    admins.append("**admin roles are:**\n")
    trusted = list()
    trusted.append("**trusted roles are:**\n")
    for role in high_level_roles:
        if role[1] == "True":
            admins.append("<@&"+str(role[0])+">\n")
        else:
            trusted.append("<@&"+str(role[0])+">\n")
    content = "".join(admins)
    await message.channel.send(content)
    content = "".join(trusted)
    await message.channel.send(content)
    db.commit()
    db.close()