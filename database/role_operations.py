import sqlite3

def remove_role(role):
    dbname = "databases/"+str(role.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    cursor.execute("DELETE FROM guild_roles WHERE role_id='"+str(role.id)+"'")

    db.commit()
    db.close()

def add_role(role):
    dbname = "databases/"+str(role.guild.id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()

    cursor.execute("INSERT INTO guild_roles (role_id) VALUES ('"+str(role.id)+"')")

    db.commit()
    db.close()