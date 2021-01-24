import discord
from discord.ext import commands
from discord.ext import cogs
import os
import requests
import json
import random 
import time
from PIL import Image
from io import BytesIO
from keep_alive import keep_alive

#Nights' to-do list: Overhaul with cogs/get help command not looking fugly. Honking at people. Bank deposit/withdrawal system. Having geese and sending them on quests. Command cooldowns. Daily rewards, daily reminder that smol han. 

#Maybe add more later
honkQuotes = ['honk.','hOOOONK','honk?','HONK','HONK','HONK HONK','HoNK hoNKK. HOOOOONK~','HOnk hONK','HONK BONK','HONK HONK HONK','HONKERS','HOOOONK. HOOOONK','HOONk hoNK','HONKITY FONKITY','hOnK hOnk', 'hoNK hONk', 'honk', 'honk.']
sacrificePositive = [f"<:goosepizza:802019887546368021> PIZZA. You gain",f"The skies open and a goose-shaped cloud gives you",f"Your friends think you've gone insane, praying to a Goose God. But you know better, and you've been rewarded with",f"The Goose Lord smiles upon you. You're mysteriously gifted",f"The Goose God smiles upon you. You receive",f"The Goose God smiles upon you. You receive",f"The Goose God smiles upon you. You receive",f"You really suck at sacrificing and accidently duplicate some of your coins instead. You receive",f"The Goose God smiles upon you. You receive",f"The Goose God smiles upon you. You receive",f"The Goose God smiles upon you. You receive",f"The Goose God smiles upon you. You receive"]

bot = commands.Bot(command_prefix="$", case_insensitive=True)
bot.remove_command("help")
@bot.event
async def on_ready(): #Sets a status upon going online.
  print('Bot logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Under maintenance, don't use."))

@bot.event
async def on_message(message):
  #Checks if the bot is the one who sent the message.
  if message.author == bot.user:
    return
  #HONK
  else:
    if "honk" in message.content.lower():
      response = random.choice(honkQuotes)
      await message.channel.send(response)
      await open_honk_account(message,message.author)
      users = await get_honk_data()
      user = message.author
      await get_honk_data()
      users[str(message.guild.id)][str(user.id)]["Honks"] += 1
      with open("honk.json","w") as f:
        json.dump(users,f)
    #Reacts to bread emoji. But not flat bread or french bread. I hate those.
    if message.content == '🍞':
      await message.channel.send('is for me? <:goosebread:802019887542960148>')
    if 'bread' in message.content.lower():
      await message.add_reaction('🍞')
  #To sista *winks with olives*
    if "eye" in message.content.lower():
      await message.add_reaction('👀')

  #DO NOT REMOVE, ENSURES COMMANDS WILL RUN
  await bot.process_commands(message)

#I said it once, and I'll say it again. 
#Fuck you Atlas. Fuck. You.

def get_quote(): #So I can be discount Atlas. And yeah I imported a whole library just for this.
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"'+json_data[0]['q']+'"\n\t - ' + json_data[0]['a']
  return(quote)

@bot.command(aliases = ["q","quote","hq","da","discountatlas"])
async def humanquote(ctx):
  quote = get_quote()
  await ctx.send(quote)

@bot.command(aliases = ["bal"])
#Amount of coins shenanigans.
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  wallet_amt = users[str(user.id)]["Wallet"]
  bank_amt = users[str(user.id)]["Bank"]
  embed = discord.Embed(title= f"{ctx.author.display_name}'s balance", color= discord.Color.blue()) #This might also change as you get $
  embed.set_thumbnail(url=ctx.author.avatar_url)
  embed.add_field(name = "Wallet", value = wallet_amt)
  embed.add_field(name = "Bank", value = bank_amt)
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

#Sacrifice your bread to the Gods. Other ones should be leeching (make friends), dueling/stealing, gambling. 8ball should be a thing too. Racing as well, foraging. And army time, serenading, etc. You can buy and sell geese/items.
@bot.command(aliases = ["sac","sc","sf"])
async def sacrifice(ctx):
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

@bot.command(aliases = ["mlb"]) #Leaderboard for amoung of bread people have.
async def moneyleaderboard(ctx, pplShown = 5):
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

@bot.command(aliases = ["hc"])
async def hcount(ctx):
  await open_honk_account(ctx,ctx.author)
  user = ctx.author
  users = await get_honk_data()
  honkNumber = users[str(ctx.guild.id)][str(user.id)]["Honks"]
  name = ctx.message.author.display_name
  await ctx.send(f"User {name} has said 'honk' {honkNumber} times.")

async def open_honk_account(ctx,user):
  users = await get_honk_data()
  if str(ctx.guild.id) in users:
    if str(user.id) in users[str(ctx.guild.id)]:
      #Both guild and user account created, nothing to see here.
      pass
    else:
      #Makes the user account, guild already made.
      users[str(ctx.guild.id)][str(user.id)] = {}
      users[str(ctx.guild.id)][str(user.id)]["Honks"] = 0
      print("New Honk Data made.")
  else:
    #Makes both the guild and the user
    users[str(ctx.guild.id)] = {}
    users[str(ctx.guild.id)][str(user.id)] = {}
    users[str(ctx.guild.id)][str(user.id)]["Honks"] = 0
    print("New Honk Data Made, with guild data.")
  with open("honk.json","w") as f:
    json.dump(users,f)

#NOT to be confused with open_honk_account(). Already wasted 20 minutes of my life with that.
async def get_honk_data():
  with open("honk.json","r") as f:
    users = json.load(f)
    return users

@bot.command(aliases = ["lb"]) #Leaderboard for HONK
async def leaderboard(ctx, pplShown = 5):
  users = await get_honk_data()
  leaderboard = {}
  total = []

  for user in users[str(ctx.guild.id)]:
    name = int(user)
    total_amount = users[str(ctx.guild.id)][str(user)]["Honks"]
    leaderboard[total_amount] = name
    total.append(total_amount)
  total = sorted(total, reverse=True)
  em = discord.Embed(title = f"Top {pplShown} Honkiest Honkers", color = discord.Color.blue())
  em.set_thumbnail(url=ctx.guild.icon_url)
  index = 1
  for amt in total:
    id_ = leaderboard[amt]
    name=str(await bot.fetch_user(id_))
    name = name[:-5]
    em.add_field(name = f"{index}. {name}", value = f"{amt}", inline=False)
    
    if index == pplShown:
      break
    else:
      index += 1
  em.set_footer(text="Making Goose God proud since never.")
  await ctx.send(embed = em)

@bot.command()
async def chased(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  chasing = Image.open("chasing.jpg")
  asset = user.avatar_url_as(size = 64)
  data = BytesIO(await asset.read())
  pfp = Image.open(data) #171x171 px
  pfp = pfp.resize((171,171))
  chasing.paste(pfp, (1523,514))
  chasing.save("profile.jpg")
  await ctx.send(content = f"{user.display_name} gets chased!",file = discord.File("profile.jpg"))
@bot.command(aliases = ["a","abt"])
async def about(ctx):
  em = discord.Embed(title = "About", color= discord.Color.blue(),description = "On September 15th, Nights promised to make a bot that only responded to HONKS. That night, HONKERS, the bot now known as GOOSE GOD, was born. The project was left in a dusty python folder that didn't even bother using a .env file to hide its bot token, all the way until 1/21/21, when Nights decided that instead of studying for her two finals the day after, to instead pull up repl.it and being anew with the bot. Within two days it was a piece of shit that responds to honks. \n\nOk, enough poeticism. It's a fucking goose bot. What more do I have to say? *grumbles*")
  await ctx.send(embed = em)

#keep_alive()
#The least useful line in the whole program.
bot.run(os.getenv('ELMOISOURMOM'))