import discord
import os
import requests
import json
import random
import time
from replit import db
from keep_running import keep_running

client = discord.Client()

monkey_words = ["oo oo", "ooh ooh", "ah ah", "ahh ahh", "ooh ah", "oo ah", "ah oo", "ah ooh", "monkey", "monke"]

monkey_response = [
  "ooh ooh ah ah",
  "oo oo",
  "who wrote this article?",
  "ahh ahh ahh",
  "b a n a n a",
  "monke",
  "RIP Harambe :(",
  "momnkeee"
]

banned_words = [
  "jew",
  "kys",
  "kill yourself",
  "retard"
]

if "active" not in db.keys():
  db["active"] = True

@client.event
async def on_ready():
  print('Successfully logged in as {0.user}'.format(client))

"""
def get_kanye_quote():
  response = requests.get("https://api.kanye.rest")
  json_data = json.loads(response.text)
  return(json_data)

def get_elon_quote():
  response = requests.get("randomElon.peterthaleikis.com")
  json_data = json.loads(response.text)
  return(json_data)
"""

def update_quotes(quote):
  if "quotes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote]

def delete_quote(index):
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
    db["quotes"] = quotes
  
@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$updates'):
    await message.channel.send('Coming soon: $joke, $kanye, $elon, more images, and more!')

  if msg.startswith('$help'):
    await message.channel.send('Supported commands: $help, $hello, $updates, $monke, $quote, $new, $del, $list; append an h to the beginning of a command to get help with it (ex: $hnew for help with the $new command)')

  if msg.startswith('$monke'):
    await message.channel.send(file=discord.File('monkey.png'))

  """
  if msg.startswith('$kanye'):
    quote = get_kanye_quote
    await message.channel.send(quote)

  if msg.startswith('$elon'):
    quote = get_elon_quote
    await message.channel.send(quote)
  """

  if msg.startswith('$quote'):
    if db["quotes"] == []:
      await message.channel.send("No quotes!")
    else:
      await message.channel.send(random.choice(db["quotes"]))

  if msg.startswith('$new'):
    if any(word in msg for word in banned_words):
      await message.channel.send("That quote doesn't seem so nice...")
    else:
      quote = msg.split("$new ", 1)[1]
      update_quotes(quote)
      await message.channel.send("New quote added!")

  if msg.startswith('$del'):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_quote(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)

  if msg.startswith('$list'):
    quotes = []
    if "quotes" in db.keys():
      quotes = db["quotes"]
    await message.channel.send(quotes)

  if msg.startswith('$toggle'):
    value = msg.split("$toggle ", 1)[1]
    if value.lower() == "true":
      db["active"] = True
      await message.channel.send("Monkey detection is active")
    else:
      db["active"] = False
      await message.channel.send("Monkey detection is inactive")
  
  if db["active"]:
    if any(word in msg for word in monkey_words):
      await message.channel.send(random.choice(monkey_response))
    if msg.startswith('banana'):
      await message.channel.send('Where?!')

  if msg.startswith('$hhello'):
    await message.channel.send('$hello is used to print out a simple greeting')

  if msg.startswith('$hhelp'):
    await message.channel.send('$help is used to see a list of available commands')

  if msg.startswith('$hmonke'):
    await message.channel.send('$monke is used to show a picture of a monkey')
 
  if msg.startswith('$hkanye'):
    await message.channel.send('$kanye is used to get a random Kanye West quote')

  if msg.startswith('$helon'):
    await message.channel.send('$elon is used to get a random Elon Musk quote')
 
  if msg.startswith('$hjoke'):
    await message.channel.send('$joke is used to tell a random joke')

  if msg.startswith('$hquote'):
    await message.channel.send('$quote is used to get a random quote from the database')

  if msg.startswith('$hnew'):
    await message.channel.send('$new is used to add a new quote (invoked $new insertQuote)')

  if msg.startswith('$hdel'):
    await message.channel.send('$del is used to delete an existing quote (invoked $del insertIndexOfQuote)- Use $list to find index, starts at 0')

  if msg.startswith('$hlist'):
    await message.channel.send('$list is used to list all the quotes in the database')

  if msg.startswith('$htoggle'):
    await message.channel.send('$toggle is used to toggle plain-text detection (using $ commands will always work, use true to toggle on and anything else to toggle off')

  if msg.startswith('$hupdates'):
    await message.channel.send('$updates is used to display planned additions to the bot')

keep_running()
client.run(os.environ.get('TOKEN'))
