import discord
import os
import requests
import json
import random
import asyncio
from datetime import date
from replit import db

today = date.today()

firstReminderDays = [[1, 25], [2, 22], [3, 25], [4, 24], [5, 25], [6, 24], [7, 25], [8, 25], [9, 24], [10, 25], [11, 24], [12, 25]]
secondReminderDays = [[1, 30], [2, 27], [3, 30], [4, 29], [5, 30], [6, 29], [7, 30], [8, 30], [9, 29], [10, 30], [11, 29], [12, 30]]
final_check = [[1, 31], [2, 28], [3, 31], [4, 30], [5, 31], [6, 30], [7, 31], [8, 31], [9, 30], [10, 31], [11, 30], [12, 31]]
sent_reminder = False

bot = discord.Client()

@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send("Hello!")

  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"] 
  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New response added lel")
  
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ", 1))
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('$rent'):
    rent_info = str(firstReminderDays) + "\n" + str(secondReminderDays) + "\n" + str(final_check)
    await message.channel.send("I will remind you on the following days:\n" + rent_info)

  if msg.startswith('$code'):
    await message.channel.send("My code is at: https://replit.com/@AntonioMac/Rose-Bot#main.py")
  
  if msg.startswith('$STFU'):
    await message.channel.send("yoooo my bad, joe mama asked tho")

@bot.event
async def rent_reminder():
  while True:
    month_day_year = today.strftime("%m/%d/%y").split("/")
    for (i,v) in enumerate(month_day_year):
      month_day_year[i] = int(v)
    
    await bot.wait_until_ready()
    curr_date = [month_day_year[0], month_day_year[1]]
    
    # testing  
    # if True:
    #  channel = discord.utils.get(bot.guilds[0].channels, name = 'rose-bot-reminders')
    #  await channel.send("joe mama @everyone " + "rent is due!")
    #  await asyncio.sleep(1)


    # Remind a week before
    if curr_date in firstReminderDays:
      reminder = ""
      for member in bot.get_all_members():
        if member.id == bot.user.id:
          continue
        else:
          reminder = reminder + "@" + "member"
      channel = discord.utils.get(bot.guilds[0].channels, name = 'rose-bot-reminders')
      await channel.send(reminder + "rent is due!")
      await asyncio.sleep(86400)
      continue
    
    # Remind a few days before
    if curr_date in secondReminderDays:
      reminder = ""
      for member in bot.get_all_members():
        if member.id == bot.user.id:
          continue
        else:
          reminder = reminder + "@" + "member"
      channel = discord.utils.get(bot.guilds[0].channels, name = 'rose-bot-reminders')
      await channel.send(reminder + "rent is due!")
      await asyncio.sleep(86400)
      continue

    # Remind the last day of the month
    if curr_date in final_check:
      channel = discord.utils.get(bot.guilds[0].channels, name = 'rose-bot-reminders')
      await channel.send("final reminder - rent is due!")
      await asyncio.sleep(86400)
      continue
    
      
          


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = ["Obama", "herro it be aight", "u got this, ez dub 😎"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "\"" + json_data[0]['q'] + "\" \n  - " + json_data[0]['a']
  return quote

def update_encouragements(encouraging_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_msg]

def delete_encouragement(index):
  encouragements = db["encouragements"] 
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

my_secret = os.environ['TOKEN']
bot.loop.create_task(rent_reminder())
bot.run(my_secret)