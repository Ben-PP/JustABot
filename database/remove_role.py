import sqlite3

def remove_role(role):
    dbname = "databases/"+str(role.guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("DELETE FROM access_level WHERE role_id='"+str(role.id)+"'")

    db.commit()
    db.close()