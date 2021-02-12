#for basic functionality
import discord
from discord.ext import commands
import os #for env
import requests
import json
import random
import time
#for image manipulation
from PIL import Image
from io import BytesIO
#for databases, will work out later
import pymongo
import dns
#to keep it running
from keep_alive import keep_alive

#Pymongo shenanigans, I don't understand a thing :(
cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]

intents = discord.Intents.default()
intents.members = True



bot = commands.Bot(command_prefix="$", case_insensitive=True, intents=intents)

#Basically @bot.event or @client.event, but now in cogs.
class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener() 
  async def on_ready(self): #Basically when bot goes online. Prints in console, sets a status.
    testing = 1
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
            newuser = {"id": message.author.id, "honks": 1}
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
    if isinstance(error, commands.BadArgument):
      await ctx.send("Something went wrong, or the command doesn't exist.")


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
    chasing = Image.open("chasing.jpg")
    asset = user.avatar_url_as(size=64)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((171,171))
    chasing.paste(pfp, (1523,514))
    chasing.save("chasingp.jpg") 
    await ctx.send(content = f"{user.display_name} gets chased!",file = discord.File("chasingp.jpg"))
  
  @commands.command()
  async def interesting(self, ctx, user:discord.Member = None):
    if user == None:
      user = ctx.author
    interest = Image.open("eddyinteresting.jpg")
    asset = user.avatar_url_as(size=64)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((249,249))
    interest.paste(pfp, (138, 128))
    interest.save("eddyinterestingp.jpg")
    await ctx.send(content = f"{user.display_name} is iNteReSTiNG", file=discord.File("eddyinterestingp.jpg"))
  
  @commands.command(aliases = ["hp","honk"]) #Have to get it so doing this won't activate the honking event
  async def honkplebe(self, ctx, user: discord.User=None):
    if user == None:
      await ctx.send("You can't honk at yourself, silly!")
    else: #This doesn't actually ping anyone.
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
class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases = ["bal"])
  async def balance(self, ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["Wallet"]
    bank_amt = users[str(user.id)]["Bank"]
    embed = discord.Embed(title= f"{ctx.author.display_name}'s balance", color= discord.Color.blue()) #This might also change as you get $
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name = "Wallet", value = wallet_amt)
    embed.add_field(name = "Bank", value = bank_amt)

    #Determines footer.
    if wallet_amt < 1000:
      embed.set_footer(text="Wow, you're poor.") 
    elif wallet_amt < 5000:
      embed.set_footer(text="Not as poor. Still in rags, though.")
    elif wallet_amt < 15000:
      embed.set_footer(text="Middle class, I guess.")
    elif wallet_amt < 50000:
      embed.set_footer(text="You could afford a decent birdsuit with that.")
    elif wallet_amt < 100000:
      embed.set_footer(text="You're rich.")
    elif wallet_amt < 1000000:
      embed.set_footer(text="Goose God is proud.")
    else:
      embed.set_footer(text="Goo(d)se God, go outside!")
    await ctx.send(embed=embed)

  @commands.command(aliases = ["sac","sc","sf"])
  async def sacrifice(self, ctx):
    sacrificePositive = ["<:goosepizza:802019887546368021> PIZZA. You gain","The skies open and a goose-shaped cloud gives you","Your friends think you've gone insane, praying to a Goose God. But you know better, and you've been rewarded with","The Goose Lord smiles upon you. You're mysteriously gifted","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","You really suck at sacrificing and accidently duplicate some of your coins instead. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive"] #I'm not creative ok.

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randint(-15,50)
    await get_bank_data()
    if earnings > 0:
      response = random.choice(sacrificePositive)
      responseTwo = " "+str(earnings)+" bread."
      response += responseTwo
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>") #Eventually wanna make a list of these messages
      time.sleep(2)
      await message.edit(content=response)
    elif earnings < 0:
      earnings *= -1
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      time.sleep(2)
      await message.edit(content=f"You've angered the Gods. You lose {earnings} bread on the side of the road.") 
      earnings *= -1
      #See comment above. Also I have no idea how to format strings since [2:] didn't work.
    else:
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      time.sleep(2)
      await message.edit(content="LOL, no one cared. You got nothing, but I did steal your empathy banana.")
    if earnings >= 0 or (earnings < 0 and abs(earnings) <= int(users[str(user.id)]["Wallet"])):
      users[str(user.id)]["Wallet"] += earnings
    else:
      users[str(user.id)]["Wallet"]= 0 #No negative balances. No debt.

    with open("bank.json","w") as f:
      json.dump(users,f)

  @commands.command(aliases = ["blb","bleaderboard","breadleaderboard"])
  async def breadlb(self, ctx, pplShown = 5):
    users = await get_bank_data()
    leaderBoard = {}
    total = []

    for user in users:
      name = int(user)
      total_amount = users[user]["Wallet"] + users[user]["Bank"]
      leaderBoard[total_amount] = name
      total.append(total_amount)
    total = sorted(total, reverse=True)
    em = discord.Embed(title = f"Top {pplShown} Richest People", color = discord.Color.blue())
    em.set_thumbnail(url=ctx.guild.icon_url)
    index = 1
    for amt in total:
      id_ = leaderBoard[amt]
      name=str(await bot.fetch_user(id_))
      name = name[:-5]
      em.add_field(name = f"{index}. {name}", value = f"{amt}", inline=False)
    
      if index == pplShown:
        break
      else:
        index += 1
    em.set_footer(text="Stop and worship Goose God, you heathen.")
    await ctx.send(embed = em)
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
      if emptychance >= int(pplShown):
        em.add_field(name="No one has honked. Shame.", value="Type 'honk' to get this leaderboard started.")
      em.set_footer(text="Making Goose God proud since never.")
      await ctx.send(embed = em)
   
class Info(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(aliases = ["a","abt"])
  async def about(self,ctx):
    em = discord.Embed(title = "About", color= discord.Color.blue(),description = "On September 15th, Nights promised to make a bot that only responded to HONKS. That night, HONKERS, the bot now known as GOOSE GOD, was born. The project was left in a dusty python folder that didn't even bother using a .env file to hide its bot token, all the way until 1/21/21, when Nights decided that instead of studying for her two finals the day after, to instead pull up repl.it and being anew with the bot. Within two days it was a piece of shit that responds to honks. \n\nOk, enough poeticism. It's a fucking goose bot. What more do I have to say? *grumbles*")
    await ctx.send(embed = em)

#Helper functions
async def open_account(user):
  users = await get_bank_data()
  if str(user.id) in users:
    pass #Forgot what this does
    questions = 0
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["Wallet"]=0
    users[str(user.id)]["Bank"]=0
    questions = 1
  if questions == 1:
    print("New account made.")

  with open("bank.json","w") as f:
    json.dump(users,f)

async def get_bank_data():
  with open("bank.json","r") as f:
    users = json.load(f)
  return users


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