import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import requests
import json
import random
import asyncio
import math #oh god oh no
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import pymongo
import dns
from keep_alive import keep_alive

#Sets up the database and collection.
cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]
servercom = cluster["disc0"]["servercom"]
#levelling.update_many({}, {"$set": {"quest": 0}}) IT WORKS IT WORKS
#<a:pepegoose:802019887337439303> yeet
#Sets up the bot.
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", case_insensitive=True, intents=intents)
bot.remove_command("help")

#all the random lists of stuff used throughout this
sacrificePositive = ["<:goosepizza:802019887546368021> PIZZA. You gain","The skies open and a goose-shaped cloud gives you","Your friends think you've gone insane, praying to a Goose God. But you know better, and you've been rewarded with","The Goose Lord smiles upon you. You're mysteriously gifted","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","You really suck at sacrificing and accidently duplicate some of your coins instead. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive"]
commandInt = {
  "reactions": 2,
  "parodies": 3,
  "battle": 5,
  "quests": 7,
  "honkresponse": 11,
}
class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener() 
  async def on_ready(self): #When bot goes online.
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
        else:
          pass
        #Adding a honk to the user's dict.
        stats = levelling.find_one({"id": message.author.id})
        if stats is None:
            newuser = {"id": message.author.id, "honks": 1, "balance": 0, "coins": 0, "quest": 0,}
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
      #These three reactions should soon be toggleable, on and off.
      stats = servercom.find_one({"id": message.guild.id})
      if stats["commandint"]%2 == 0:
        if "eye" in message.content.lower():
          await message.add_reaction('👀')
        if "solar" in message.content.lower():
          await message.add_reaction('🐧')
        if "coffee" in message.content.lower():
          await message.add_reaction('☕')
        if "interesting" in message.content.lower():
          await message.add_reaction(r'<:eddy_interesting:760913535013748746>')
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      seconds = math.floor(error.retry_after)
      if seconds > 3600:
        hours = str(math.floor(seconds/3600))
        minutes = str(math.floor((int(seconds) - int(hours)*3600)/60))
      await ctx.send("Command on cooldown. Try again in "+hours+" hours and "+minutes+" minutes.")
    elif isinstance(error, commands.BadArgument):
      pass
    elif isinstance(error, CommandNotFound):
      await ctx.send("Command doesn't exist. HONK.")
    else:
      raise error
class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #Grabs a random quote. Atlas, you suck. Get one-upped.
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
    stats = servercom.find_one({"id": ctx.guild.id})
    if stats is None:
      newguild = {"id": ctx.guild.id, "commandint": 2310,}
      servercom.insert_one(newguild)
    stats = servercom.find_one({"id": ctx.guild.id})
    if stats["commandint"]%3 == 0:
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
  
  @commands.command(aliases = ["mc", "cook"])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def microwave(self, ctx):
    foodGloriousFood = ["🥔","🍞","🥜","🍖","🍕","🥫","☕","🥧","🍯","🍉","🍌","🍍","🥖","🌭","🌮","🥗","🍚","🍣","🥄", "a broken microwave.", "mail",]
    borkBork = random.choice(foodGloriousFood)
    timeLeft = 5
    message = await ctx.send("<:microwave:813862298522877984> Microwaving...please wait **"+str(timeLeft)+"** seconds")
    for x in range(0,5):
      await asyncio.sleep(1)
      timeLeft -= 1
      await message.edit(content="<:microwave:813862298522877984> Microwaving...please wait **"+str(timeLeft)+"** seconds")
    await message.edit(content="You got "+borkBork)
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
  @commands.command()
  #immediately gets insulted for not using bits
  async def disable(self, ctx, com = None):
    global commandInt
    stats = servercom.find_one({"id": ctx.guild.id})
    if stats is None:
      newguild = {"id": ctx.guild.id, "commandint": 2310,}
      servercom.insert_one(newguild)
    stats = servercom.find_one({"id": ctx.guild.id})
    if com == None:
      await ctx.send("You can't disable no command, silly. HONK HONK. Type '$disable commands' to see a list of what you can disable and enable.")
    elif com.lower() == "command" or com.lower() == "commands":
      em = discord.Embed(title="Toggleable Commands", description="What you can turn off by typing after $disable.", color =discord.Color.blue())
      em.set_thumbnail(url=ctx.guild.icon_url)
      em.add_field(name="Reactions", value = "Turns off all reactions but bread", inline=True)
      em.add_field(name="Images", value="Disables parody commands, like quotes and Twoset related commands.", inline=True)
      em.add_field(name="Battle", value="Can't battle others in your server", inline=True)
      em.add_field(name="Quests", value="Can't do quests in the server", inline=True)
      em.add_field(name="Honkresponse", value="Doesn't respond to honks. Still counts them.", inline=True)
      await ctx.send(embed = em)
    else:
      try:
        if stats["commandint"]%commandInt[com] == 0:
          newInt = stats["commandint"]/commandInt[com]
          servercom.update_one({"id":ctx.guild.id}, {"$set":{"commandint": newInt}})
          await ctx.send("Command disabled *sniffs and honks*")
        else:
          await ctx.send("You've already disabled this command. HONK")
      except KeyError:
        await ctx.send("You can't disable a nonexistent command HONK~. Type '$disable commands' to see a list of what you can disable and enable.")
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
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 200, "coins": 0, "quest": 0}
      levelling.insert_one(newuser)
    stats = levelling.find_one({"id": ctx.author.id})
    bal = stats["balance"] + 200
    levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
    await ctx.send("You've gained 200 bread HONK~. Check back in 12 hours.")

  @commands.command(aliases = ["bal"])
  async def balance(self, ctx):
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 0,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
      print("New User made.")
    stats = levelling.find_one({"id": ctx.author.id})
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
  @commands.cooldown(15, 21600, commands.BucketType.user)
  async def sacrifice(self, ctx):
    global sacrificePositive #I'm not creative ok.
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 1,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
    stats = levelling.find_one({"id": ctx.author.id})
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
  
  @commands.command(aliases = ["coin","cf"])
  @commands.cooldown(25, 21600, commands.BucketType.user)
  async def coinflip(self, ctx, sideChosen = None):
    if sideChosen == None:
      await ctx.send("Type 'heads' if you call heads and 'tails' if you call tails.")
    pass

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
#Helper functions, will probably have to make one for opening database.

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