import sqlite3

def remove_role(role):
    dbname = "databases/"+str(role.guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("DELETE FROM access_level WHERE role_id='"+str(role.id)+"'")
    cursor.execute("SELECT * FROM reaction_role_messages")
    messages = cursor.fetchall()
    if len(messages) > 0:
        for message in messages:
            cursor.execute("DELETE FROM '"+str(message[0])+"' WHERE role_id='"+str(role.id)+"'")
            cursor.execute("SELECT * FROM '"+str(message[0])+"'")
            if len(cursor.fetchall()) < 1:
                cursor.execute("DROP TABLE '"+str(message[0])+"'")
                cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(message[0])+"'")
                cursor.execute("SELECT * FROM embedded_messages WHERE embed_message_id='"+str(message[0])+"' or sent_message_id='"+str(message[0])+"'")
                if len(cursor.fetchall()) < 1:
                    cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(message[0])+"'")

    db.commit()
    db.close()