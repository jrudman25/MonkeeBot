import discord
import os
import requests
import json
import random
import time
from replit import db
from keep_running import keep_running
import re

client = discord.Client()

monkey_words = ["oo oo", "ooh ooh", "ah ah", "ahh ahh", "ooh ah", "oo ah", "ah oo", "ah ooh", "monkey", "monke", "monkee"]

monkey_response = [
  "ooh ooh ah ah",
  "oo oo",
  "who in the blazes wrote this article?",
  "ahh ahh ahh",
  "b a n a n a",
  "monke",
  "RIP Harambe :(",
  "momnkeee"
]

banned_words = [
  "jew",
  "kys",
  "kill",
  "retard",
  "holocaust",
  "rape",
  "murder",
  "suicide",
  "whore",
  "pussy",
  "homo",
  "faggot",
  "dyke",
  "bussy",
  "cunt",
  "queer",
  "dussy",
  "shoot",
  "gun",
  "knife",
  "hurt",
  "injure",
  "racis",
  "@",
  "kkk",
  "stab",
  "shoot"
]

# Setup and rich presence settings
@client.event
async def on_ready():
  print('Successfully logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="$help to get started!"))

if "active" not in db.keys():
  db["active"] = True

# API Functions
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

# Quoting Functions
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

def check_banned(quote):
  if any(word in quote for word in banned_words):
    return True
  testQuote = quote.lower().replace(" ", "")
  testQuote = re.sub('[^A-Za-z0-9 ]+', '', testQuote)
  print(testQuote)
  if any(word in testQuote for word in banned_words):
    return True
  else:
    return False

# Client Events
@client.event
async def on_message(message):

  # Creates msg variable for ease of access
  msg = message.content

  # Ignore messages from self
  if message.author == client.user:
    return

  # Beginner hello function
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  # Toggles monkey word detection on and off
  if msg.startswith('$toggle'):
    print('{0} tried to toggle monkey detection'.format(message.author))
    value = msg.split("$toggle ", 1)[1]
    if value.lower() == "true":
      db["active"] = True
      await message.channel.send("Monkey detection is active")
    elif value.lower() == "false":
      db["active"] = False
      await message.channel.send("Monkey detection is inactive")
    else:
      await message.channel.send("I don't recognize that request")

  # Create a new quote
  if msg.startswith('$new'):
    print('{0} tried to add a new quote'.format(message.author))
    quote = msg.split("$new ", 1)[1]
    if check_banned(quote) == True:
      await message.channel.send("Please be nice, use only alphanumeric characters, and don't @ people!")
    else:
      if len(quote) > 150:
        await message.channel.send("That quote is too long...")
      else:
        update_quotes(quote)
        await message.channel.send("New quote added!")

  # Delete a quote
  if msg.startswith('$del'):
    if "quotes" in db.keys():
      index = msg.split("$del", 1)[1]
      
      try:
        val = int(index)
      except ValueError:
        await message.channel.send("That is not a valid index...")
      print('{0} deleted a quote'.format(message.author))
      delete_quote(val)
      await message.channel.send(', '.join(str(x) for x in db["quotes"]))

  # Pull a random quote
  if msg.startswith('$quote'):
    if db["quotes"] == []:
      await message.channel.send("No quotes in database!")
    else:
      await message.channel.send(random.choice(db["quotes"]))

  # List all quotes
  if msg.startswith('$list'):
    if db["quotes"] == []:
      await message.channel.send("No quotes in database!")
    elif "quotes" in db.keys():
      await message.channel.send(', '.join(str(x) for x in db["quotes"]))
    
  # Hidden clear function
  if msg.startswith('$clear'):
    db["quotes"] = []
    print('{0} cleared the database'.format(message.author))

  # Check future updates
  if msg.startswith('$updates'):
    await message.channel.send('Coming soon: $joke, $kanye, $elon, more images, and more!')

  # Get a monkey picture
  if msg.startswith('$monke'):
    await message.channel.send(file=discord.File('monkey.png'))
    
  # Diplay all usable commands
  if msg.startswith('$help'):
    await message.channel.send('Supported commands: $help, $hello, $updates, $monke, $quote, $new, $del, $list, $toggle; append an h to the beginning of a command to get help with it (ex: $hnew for help with the $new command)')

  # Quote APIs
  """
  if msg.startswith('$kanye'):
    quote = get_kanye_quote
    await message.channel.send(quote)

  if msg.startswith('$elon'):
    quote = get_elon_quote
    await message.channel.send(quote)
  """

  # Monkey word detection
  if db["active"]:
    if any(word in msg for word in monkey_words):
      await message.channel.send(random.choice(monkey_response))
    if msg.startswith('banana'):
      await message.channel.send('Where?!')

  #Help functions
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
    await message.channel.send('$toggle is used to toggle plain-text monkey word detection (use true to toggle on and false to toggle off, $ commands cannot be toggled)')

  if msg.startswith('$hupdates'):
    await message.channel.send('$updates is used to display planned additions to the bot')

# Links code to bot and keeps it running (Token stored as environment variable for security)
keep_running()
client.run(os.environ.get('TOKEN'))
