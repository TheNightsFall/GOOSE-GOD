#for basic functionality
import discord
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound
import os
from os import listdir
from os.path import isfile, join
import random
from pretty_help import PrettyHelp, Navigation
import math #oh god oh no
import pymongo
import dns
import datetime
from datetime import timedelta
import pytz
from keep_alive import keep_alive

commandInt = {
  "reactions": 2,
  "parodies": 3,
  "battle": 5,
  "quests": 7,
  "honkresponse": 11,
}

cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]
servercom = cluster["disc0"]["servercom"]
han = servercom = cluster["disc0"]["dailyreminder"]
#levelling.update_many({}, {"$set": {"inventory": []}})

intents = discord.Intents.default()
intents.members = True
#change this back to $ later.
bot = commands.Bot(command_prefix="h!", case_insensitive=True, intents=intents)

nav = Navigation("🔼", "🔽")
color = discord.Color.blue()
bot.help_command = PrettyHelp(navigation = nav, color=color, active_time=40)

@bot.event 
async def on_ready(): #When bot goes online.
  testing = 0
  print('Bot logged in as {0.user}'.format(bot))
  smolHan.start(bot)
  if testing == 0:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move."))
  else:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="debugging, donut use."))
  
@bot.event
async def on_message(message):
  if message.author == bot.user:
    pass
  elif not message.guild:
    await message.channel.send("GET OUT OF DMS. HONK.")
  else:
    stats = servercom.find_one({"id": message.guild.id})
    if stats is None:
      newguild = {"id": message.guild.id, "commandint": 2310,}
      servercom.insert_one(newguild)
    if "honk" in message.content.lower():
      stats = servercom.find_one({"id": message.guild.id})
      if stats["commandint"]%11 == 0:
          honkQuotes = ['honk.','hOOOONK','honk?','HONK','HONK','HONK HONK','HoNK hoNKK. HOOOOONK~','HOnk hONK','HONK BONK','HONK HONK HONK','HONKERS','HOOOONK. HOOOONK','HOONk hoNK','HONKITY FONKITY','hOnK hOnk', 'hoNK hONk', 'honk', 'honk.']
          response = random.choice(honkQuotes)
          await message.channel.send(response)
      #Adding a honk to the user's dict.
      stats = levelling.find_one({"id": message.author.id})
      if stats is None:
          newuser = {"id": message.author.id, "honks": 1, "balance": 0, "coins": 0, "quest": 0,}
          levelling.insert_one(newuser)
      else:
          honks = stats["honks"] + 1
          levelling.update_one({"id":message.author.id}, {"$set":{"honks":honks}})
    if message.content == '🍞':
      await message.channel.send('is for me? <:goosebread:802019887542960148>')
    if 'bread' in message.content.lower():
      await message.add_reaction('🍞')
    stats = servercom.find_one({"id": message.guild.id})
    if stats["commandint"]%2 == 0:
      if "eye" in message.content.lower():
        await message.add_reaction('👀')
      if "solar" in message.content.lower():
        await message.add_reaction('🐧')
      if "coffee" in message.content.lower():
        await message.add_reaction('☕')
      if "whack" in message.content.lower():
        await message.add_reaction('💔')
  await bot.process_commands(message)
  
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    seconds = math.floor(error.retry_after)
    if seconds > 3600:
      hours = str(math.floor(seconds/3600))
      minutes = str(math.floor((int(seconds) - int(hours)*3600)/60))
      await ctx.send("<:goosealert:802019887663939654> Command on cooldown. Try again in "+hours+" hours and "+minutes+" minutes.")
    elif seconds < 60:
      await ctx.send("<:goosealert:802019887663939654> Command on cooldown. Try again in "+seconds+" seconds.")
    else:
      minutes = str(math.floor(seconds/60))
      await ctx.send("<:goosealert:802019887663939654> Command on cooldown. Try again in " + minutes + " minutes.")
  elif isinstance(error, CommandNotFound):
    await ctx.send("Command doesn't exist. HONK.")
  else:
    raise error

#Daily reminder.
@tasks.loop(seconds = 15)
async def smolHan(bot):
  while True:
    channel = bot.get_channel(755050908491972689)
    timeTime = han.find_one({"id": 755050908491972689})
    timeE = timeTime["date"]
    utcNow = pytz.utc.localize(datetime.datetime.utcnow())
    checkCooldown = timeE + timedelta(days=1)
    checkCooldown = checkCooldown.replace(tzinfo=None)
    d = utcNow.replace(tzinfo=None)
    if checkCooldown > d:
      return
    else:
      await channel.send("Daily reminder that smol han.")
      han.update_one({"id":755050908491972689}, {"$set":{"date":utcNow}})

if __name__ == "__main__":
  for extension in [f.replace('.py', '') for f in listdir("cogs") if isfile(join("cogs", f))]:
    try:
      bot.load_extension("cogs" + "." + extension)
      print(f"Cog {extension} successfully loaded.")
    except:
      print(f"Failed to load extension {extension}. If you do surgery like you load cog, patient already dead.")
  keep_alive()
  bot.run(os.getenv('ELMOISOURMOM'))
else:
  print("Something went wrong.")
