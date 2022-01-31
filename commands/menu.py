import requests
from bs4 import BeautifulSoup
import discord

import commands.help

#TODO: Test on friday and sunday.
async def menu(message):
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await commands.help.help_menu(message)
        return
    elif message_splitted[1].lower() == "taide":
        await send_menu(message, "https://www.foodandco.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=0301&language=fi")
        return
    elif message_splitted[1].lower() == "piato":
        await send_menu(message, "https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1408&language=fi")
        return
    elif message_splitted[1].lower() == "maija":
        await send_menu(message, "https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1402&language=fi")
        return
    elif message_splitted[1].lower() == "lozzi":
        await send_menu(message, "https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1401&language=fi")
        return
    elif message_splitted[1].lower() == "tilia":
        await send_menu(message, "https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1413&language=fi")
        return
    elif message_splitted[1].lower() == "syke":
        await send_menu(message, "https://www.semma.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1405&language=fi")
        return
    elif message_splitted[1].lower() == "list":
        await list_restaurants(message)
        return

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
                "value":"-\tLozzi\n-\tTilia\n-\tSyke",
                "inline":False
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

async def send_menu(message, url):
    url = requests.get(url)
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