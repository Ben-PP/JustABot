import requests
from bs4 import BeautifulSoup
import discord
import sqlite3

import commands.help

rss_urls = {
    "taide":"https://www.foodandco.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=0301&language=fi",
    "piato":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1408&language=fi",
    "maija":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1402&language=fi",
    "lozzi":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1401&language=fi",
    "tilia":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1413&language=fi",
    "syke":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1405&language=fi",
    "belvedere":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1404&language=fi",
    "uno":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1414&language=fi",
    "ylistö":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1403&language=fi",
    "rentukka":"https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1416&language=fi"
}


#TODO: Test on friday and sunday.
async def menu(message):
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await commands.help.help_menu(message)
        return
    elif message_splitted[1].lower() == "favorites":
        await favorites(message, message_splitted)
        return
    elif message_splitted[1].lower() == "list":
        await list_restaurants(message)
        return
    elif len(message_splitted) == 2:
        await send_menu(message, message_splitted[1].lower())
        return

async def favorites(message, message_splitted):
    #Check if command has arguments.
    if len(message_splitted) >= 3:
        command = message_splitted[2].lower()
        #Lists all the favorite restaurants of the user.
        if command == "list":
            if len(message_splitted) != 3:
                await message.channel.send("Please don't give any arguments with **list**")
                return
            dbname = "databases/"+str(message.guild.id)+".db"
            db = sqlite3.connect(dbname)
            cursor = db.cursor()

            cursor.execute("SELECT restaurant_name FROM favorite_restaurants WHERE user_id="+str(message.author.id))
            keys = cursor.fetchall()
            content = []
            content.append("**Your favorites are:**")
            for key in keys:
                content.append("\n-\t"+key[0])
            msg = "".join(content)
            await message.channel.send(msg)

            db.commit()
            db.close()
            return

        #Adds restaurant to favorites.
        if command == "add":
            if len(message_splitted) != 4:
                await message.channel.send("Incorrect ammount of arguments.")
                return
            dbname = "databases/"+str(message.guild.id)+".db"
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            key = message_splitted[3].lower()
            try:
                url = rss_urls[key]
            except:
                await message.channel.send("Restaurant not found. Check spelling or contact developer for adding the restaurant!")
                return
            cursor.execute("""INSERT OR REPLACE INTO favorite_restaurants (
                user_id,
                restaurant_name) VALUES (
                    """+str(message.author.id)+""",
                    '"""+key+"""'
                )""")
            await message.channel.send(message_splitted[3]+" added to your favourites!")
            db.commit()
            db.close()
            return

        #Removes restaurant from favorites.
        if command == "remove":
            if len(message_splitted) != 4:
                await message.channel.send("Incorrect ammount of arguments.")
                return
            dbname = "databases/"+str(message.guild.id)+".db"
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            key = message_splitted[3].lower()
            try:
                url = rss_urls[key]
            except:
                await message.channel.send("Restaurant not found. Check spelling.")
                return
            cursor.execute("""DELETE FROM favorite_restaurants WHERE
                user_id="""+str(message.author.id)+""" AND
                restaurant_name='"""+key+"""'
                """)
            await message.channel.send(message_splitted[3]+" removed from your favorites.")

            db.commit()
            db.close()
            return
        await message.channel.send("Incorrect argument.")
        return
    
    #Sends menu from all the favorite restaurants of the user.
    dbname = "databases/"+str(message.guild.id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("SELECT restaurant_name FROM favorite_restaurants WHERE user_id="+str(message.author.id))
    keys = cursor.fetchall()
    for key in keys:
        await send_menu(message, key[0])

    db.commit()
    db.close()

async def send_menu(message, key):
    try:
        rss_url = rss_urls[key]
    except:
        await message.channel.send("Incorrect argument.")
        return
    url = requests.get(rss_url)
    soup = BeautifulSoup(url.text, "xml")
    title = soup.find("title")
    item = soup.find("item")
    date = soup.find("item").find("title")
    description = item.find("description")

    menu = description.text.split("<br>")
    fields = list()
    for menu_item in menu:
        data = menu_item.split(":")
        if len(data) >= 2:
            fields.append({"name":data[0],"value":data[1],"inline":False})
    
    content = {
        "title":title.text,
        "description":date.string+"\n",
        "fields":fields
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

async def list_restaurants(message):
    content = {
        "title":"Restaurants",
        "description":"Menu is available for following restaurants:",
        "fields":[
            {
                "name":"Yläkaupunki",
                "value":"-\tTaide",
                "inline":False
            },
            {
                "name":"Mattilanniemi",
                "value":"-\tPiato\n-\tMaija",
                "inline":False
            },
            {
                "name":"Seminaarinmäki",
                "value":"-\tLozzi\n-\tTilia\n-\tSyke\n-\tBelvedere",
                "inline":False
            },
            {
                "name":"Ruusupuisto",
                "value":"-\tUno",
                "inline":False
            },
            {
                "name":"Ylistönmäki",
                "value":"-\tYlistö",
                "inline":False
            },
            {
                "name":"Kortepohja",
                "value":"-\tRentukka",
                "inline":False
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)