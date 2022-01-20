import sqlite3

import help

async def access(message):
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1:
        await help.help_access(message)
        return
    elif message_splitted[1] == "help":
        await help.help_access(message)
        return
    elif message_splitted[1] == "add":
        await add(message, message_splitted)
        return
    elif message_splitted[1] == "remove":
        await remove(message, message_splitted)
        return
    elif message_splitted[1] == "list":
        await list_roles(message)
        return
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
        await message.channel.send("<@&"+str(role_id)+"> is now **trusted**!")
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
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM access_level WHERE role_id='"+str(role_id)+"'")
    role = cursor.fetchone()
    if role == None:
        await message.channel.send("This role does not have any access levels!")
    
    cursor.execute("DELETE FROM access_level WHERE role_id='"+str(role_id)+"'")

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
    print(str(high_level_roles))
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
    
#Returns True if user is authorized to access the command, else returns False
def authorize(message, required_level):
    if message.author.id == message.guild.owner.id:
        print("Is owner")
        return True
    
    has_access = False

    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    user_roles = message.author.roles
    
    #Checks if the role has trusted or higher access level
    if required_level == "trusted":
        cursor.execute("SELECT role_id FROM access_level WHERE is_trusted='True'")
        trusted_roles = cursor.fetchall()
        if trusted_roles != None:
            if __is_trusted(user_roles, trusted_roles):
                has_access = True
            else:
                cursor.execute("SELECT role_id FROM access_level WHERE is_admin='True'")
                admin_roles = cursor.fetchall()
                has_access = __is_admin(user_roles, admin_roles)
    #Checks if the role has admin access level
    elif required_level == "admin":
        cursor.execute("SELECT role_id FROM access_level WHERE is_admin='True'")
        admin_roles = cursor.fetchall()
        if admin_roles != None:
            has_access =  __is_admin(user_roles, admin_roles)
    elif required_level != "owner":
        print("Error: Incorrect access level! Choose either 'owner', 'admin' or 'trusted'")
        db.commit()
        db.close()
        return False

    db.commit()
    db.close()
    if has_access == False:
        print("Unauthorized user.")
    else:
        print("Authorized user.")
    return has_access

#Checks if the role has trusted access level
def __is_trusted(user_roles, trusted_roles):
    for trusted_role_id in trusted_roles:
        for user_role in user_roles:
            if trusted_role_id[0] == user_role.id:
                return True
    return False

#Checks if the role has admin access level
def __is_admin(user_roles, admin_roles):
    for admin_role in admin_roles:
        for user_role in user_roles:
            if user_role.id == admin_role[0]:
                return True
    return False