import requests
from bs4 import BeautifulSoup

import commands.help

#TODO Add to help.
async def menu(message):
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await commands.help.help_menu(message)
        return
    elif message_splitted[1] == "taide":
        await taide(message)
        return

async def taide(message):
    url = requests.get("https://www.foodandco.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=0301&language=fi")
    soup = BeautifulSoup(url.text, "html.parser")
    item = soup.find("item")
    title = item.find("title")
    await message.channel.send("**Taide**\n"+title.string)
    #FIXME: Continue when there is menu for the day