import sqlite3

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