#for basic functionality
import discord
from discord.ext import commands
import os #for env
import requests
import json
import random
import asyncio
import math
#for image manipulation
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
#for databases, will work out later
import pymongo
import dns
#to keep it running
from keep_alive import keep_alive

#Gotta implement error detectiong and responding, particularly to cooldowns, and have it convert from seconds to hours and minutes.

#Sets up the database. Not sure why I called it 'disc0'.
cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]

#Sets up the bot.
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", case_insensitive=True, intents=intents)
bot.remove_command("help")

#Basically @bot.event or @client.event, but now in cogs.
class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener() 
  async def on_ready(self): #Basically when bot goes online. Prints in console, sets a status.
    testing = 0
    print('Bot logged in as {0.user}'.format(bot))
    if testing == 0:
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move."))
    else:
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="debugging, donut use."))
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == bot.user:
      pass
    else:
      if "honk" in message.content.lower():
        honkQuotes = ['honk.','hOOOONK','honk?','HONK','HONK','HONK HONK','HoNK hoNKK. HOOOOONK~','HOnk hONK','HONK BONK','HONK HONK HONK','HONKERS','HOOOONK. HOOOONK','HOONk hoNK','HONKITY FONKITY','hOnK hOnk', 'hoNK hONk', 'honk', 'honk.']
        response = random.choice(honkQuotes)
        await message.channel.send(response)
        
        #Here the reworking begins
        stats = levelling.find_one({"id": message.author.id})
        if stats is None:
            newuser = {"id": message.author.id, "honks": 1, "balance": 0, "coins": 0}
            levelling.insert_one(newuser)
        else:
            honks = stats["honks"] + 1
            levelling.update_one({"id":message.author.id}, {"$set":{"honks":honks}})
      if message.content.startswith('imagine'):
        await message.channel.send("couldn't be me.")
      #Reacts to bread emoji. But not flat bread or french bread. I hate those.
      if message.content == '🍞':
        await message.channel.send('is for me? <:goosebread:802019887542960148>')
      if 'bread' in message.content.lower():
        await message.add_reaction('🍞')
      #To sista *winks with olives*
      if "eye" in message.content.lower():
        await message.add_reaction('👀')
      if "solar" in message.content.lower(): #Tribute to the one who inspired it. Idk why she asked for a penguin, but she did.
        await message.add_reaction('🐧')
      if "coffee" in message.content.lower():
        await message.add_reaction('☕')
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      seconds = math.floor(error.retry_after)
      if seconds > 3600:
        hours = str(math.floor(seconds/3600))
        minutes = str(math.ceil((int(seconds) - int(hours)*3600)/60))
      await ctx.send("Command on cooldown. Try again in "+hours+" hours and "+minutes+" minutes.")
    elif isinstance(error, commands.BadArgument):
      pass
    else:
      raise error
class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #Grabs a random quote.
  def get_quote(self):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = '"'+json_data[0]['q']+'"\n\t - ' + json_data[0]['a']
    return(quote)

  @commands.command(aliases = ["q","da","discountatlas"])
  async def quote(self, ctx):
    quote = self.get_quote()
    await ctx.send(quote)

  @commands.command()
  async def chased(self,ctx, user:discord.Member = None):
    if user == None:
      user = ctx.author
    chasing = Image.open("imagemanipulation/chasing.jpg")
    asset = user.avatar_url_as(size=64)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((171,171))
    chasing.paste(pfp, (1523,514))
    chasing.save("imagemanipulation/chasingp.jpg") 
    await ctx.send(content = f"{user.display_name} gets chased!",file = discord.File("imagemanipulation/chasingp.jpg"))
  
  @commands.command()
  async def interesting(self, ctx, user:discord.Member = None):
    if user == None:
      user = ctx.author
    interest = Image.open("imagemanipulation/eddyinteresting.jpg")
    font = ImageFont.truetype("times-ro.ttf", 80)
    draw = ImageDraw.Draw(interest)
    draw.text((101,510),f"{user.display_name} is",(255,255,255), font=font)
    interest.save("imagemanipulation/eddyinterestingp.jpg")
    await ctx.send(content = f"{user.display_name} is iNteReSTiNG", file=discord.File("imagemanipulation/eddyinterestingp.jpg"))
  
  @commands.command(aliases = ["hp","honk"])
  async def honkplebe(self, ctx, user: discord.User=None):
    if user == None:
      await ctx.send("You can't honk at yourself, silly!")
    else:
      await ctx.send(f"{ctx.author.display_name} honked at {user.mention}!")
  
  @commands.command()
  async def ping(self, ctx):
      if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds! What a gamer! HONK!!", color=0x44ff44)
      elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds! Still decent. honk.", color=0xffd000)
      elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds! honk?", color=0xff6600)
      else:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds! Get that internet checked. hon-- *lags out*", color=0x990000)
      await ctx.send(embed=embed)
class Honk(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(aliases = ["hc"])
  async def hcount(self, ctx): 
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
        honkNumber = 0
    else:
        honkNumber = stats["honks"]
    name = ctx.message.author.display_name
    await ctx.send(f"User '{name}' has said 'honk' {honkNumber} times.")

  @commands.command(aliases = ["lb"])
  async def leaderboard(self, ctx, pplShown = None):
      if pplShown == None:
          pplShown = 5
      
      rankings = levelling.find().sort("honks",-1)
      i = 1
      emptychance = 0
      em = discord.Embed(title = f"Top {pplShown} Honkiest Honkers", color = discord.Color.blue())
      em.set_thumbnail(url=ctx.guild.icon_url)
      for x in rankings:
          try:
            temp = ctx.guild.get_member(x["id"])
            temphonks = x["honks"]
            em.add_field(name=f"{i}: {temp.name}", value=f"Honks: {temphonks}", inline=False)
            i += 1
          except:
            emptychance += 1
          if i == int(pplShown)+1:
            break
      if emptychance == int(pplShown):
        em.add_field(name="No one has honked. Shame.", value="Type 'honk' to get this leaderboard started.")
      em.set_footer(text="Making Goose God proud since never.")
      await ctx.send(embed = em)
class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  @commands.cooldown(1, 43200, commands.BucketType.user)
  async def daily(self, ctx):
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 200, "coins": 0,}
      levelling.insert_one(newuser)
    else:
      bal = stats["balance"] + 200
      levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
    await ctx.send("You've gained 200 bread HONK~. Check back in 12 hours.")

  @commands.command(aliases = ["bal"])
  async def balance(self, ctx):
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 0,"coins": 0,}
      levelling.insert_one(newuser)
      print("New User made.")
    bal = stats["balance"]
    coins = stats["coins"] #Coins can only be gained by doing quests
    embed = discord.Embed(title= f"{ctx.author.display_name}'s bread", color= discord.Color.blue()) #This might also change as you get $
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name = "Bread", value = bal)
    embed.add_field(name = "Coins", value = coins)

    #Determines footer.
    if bal < 1000:
      embed.set_footer(text="Wow, you're poor.") 
    elif bal < 5000:
      embed.set_footer(text="Still in rags.")
    elif bal < 15000:
      embed.set_footer(text="Middle class.")
    elif bal < 50000:
      embed.set_footer(text="You could afford a decent birdsuit with that.")
    elif bal < 100000:
      embed.set_footer(text="You're rich.")
    elif bal < 1000000:
      embed.set_footer(text="Goose God is proud.")
    else:
      embed.set_footer(text="Goo(d)se God, go outside!")
    await ctx.send(embed=embed)

  @commands.command(aliases = ["sac","sc","sf"])
  async def sacrifice(self, ctx):
    sacrificePositive = ["<:goosepizza:802019887546368021> PIZZA. You gain","The skies open and a goose-shaped cloud gives you","Your friends think you've gone insane, praying to a Goose God. But you know better, and you've been rewarded with","The Goose Lord smiles upon you. You're mysteriously gifted","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","You really suck at sacrificing and accidently duplicate some of your coins instead. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive"] #I'm not creative ok.
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 1,"coins": 0,}
      levelling.insert_one(newuser)
    earnings = random.randint(-15,50)
    if earnings > 0:
      response = random.choice(sacrificePositive)
      responseTwo = " "+str(earnings)+" bread."
      response += responseTwo
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>") #Eventually wanna make a list of these messages
      await asyncio.sleep(2)
      await message.edit(content=response)
    elif earnings < 0:
      earnings *= -1
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      await asyncio.sleep(2)
      await message.edit(content=f"You've angered the Gods. You lose {earnings} bread on the side of the road.") 
      earnings *= -1
      #See comment above. Also I have no idea how to format strings since [2:] didn't work.
    else:
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      await asyncio.sleep(2)
      await message.edit(content="LOL, no one cared. You got nothing, but I did steal your empathy banana. HOOONK~")
    #Checks how much earnings is.
    if earnings >= 0 or (earnings < 0 and abs(earnings) <= int(stats["balance"])):
      if stats["balance"] != 0:
        bal = stats["balance"] + earnings
      else:
        bal = earnings
    else:
      bal = 0 #No negative balances. No debt.
    levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})

  @commands.command(aliases = ["blb","bleaderboard","breadleaderboard"])
  async def breadlb(self, ctx, pplShown = None):
    if pplShown == None:
      pplShown = 5
    
    rankings = levelling.find().sort("balance",-1)
    i = 1
    emptychance = 0
    em = discord.Embed(title = f"Top {pplShown} Richest People", color = discord.Color.blue())
    em.set_thumbnail(url=ctx.guild.icon_url)
    for x in rankings:
      try:
        temp = ctx.guild.get_member(x["id"])
        temp1 = x["balance"]
        em.add_field(name=f"{i}: {temp.name}", value=f"Bread: {temp1}", inline=False)
        i += 1
      except:
        emptychance += 1
      if i == int(pplShown):
        em.add_field(name="You're all really poor.", value="Use an economy command to get this leaderboard started.")
    em.set_footer(text="Stop and worship Goose God, you heathen.")
    await ctx.send(embed = em)
class Info(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(aliases = ["a","abt"])
  async def about(self,ctx):
    em = discord.Embed(title = "About", color= discord.Color.blue(),description = "On September 15th, Nights promised to make a bot that only responded to HONKS. That night, HONKERS, the bot now known as GOOSE GOD, was born. The project was left in a dusty python folder that didn't even bother using a .env file to hide its bot token, all the way until 1/21/21, when Nights decided that instead of studying for her two finals the day after, to instead pull up repl.it and being anew with the bot. Within two days it was a piece of shit that responds to honks. \n\nOk, enough poeticism. It's a fucking goose bot. What more do I have to say? *grumbles*")
    await ctx.send(embed = em)

#The least useful part of the whole thing
def cog_setup(x):
  bot.add_cog(Events(x))
  bot.add_cog(Misc(x))
  bot.add_cog(Economy(x))
  bot.add_cog(Honk(x))
  bot.add_cog(Info(x))

keep_alive()
cog_setup(bot)
bot.run(os.getenv('ELMOISOURMOM'))