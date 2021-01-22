import discord
from discord.ext import commands
import os
import requests
import json
import random 
from replit import db

#Ok so personally I use camelcase instead of underscores but like discord.py uses underscores so I might be jumping back and forth with variable naming. :/

#Maybe add more later
earnings = 'fillerText' #So the list below doesn't error out, just a placeholder.
honkQuotes = ['honk.','hOOOONK','honk?','HONK','HONK','HONK HONK','HoNK hoNKK. HOOOOONK~','HOnk hONK','HONK BONK','HONK HONK HONK','HONKERS','HOOOONK. HOOOONK','HOONk hoNK','HONKITY FONKITY','hOnK hOnk', 'hoNK hONk', 'honk', 'honk.']
sacrificePositive = [f"<:goosepizza:802019887546368021> PIZZA. You gain {earnings} coins.",]

bot = commands.Bot(command_prefix="$")

def get_image(): #Still working on this one. Very, very confused.
  response = requests.get("https://source.unsplash.com/?goose,geese")
  pass

def get_quote(): #So I can be discount Atlas
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"'+json_data[0]['q']+'"\n\t - ' + json_data[0]['a']
  return(quote)

@bot.event
async def on_ready(): #Sets a status upon going online.
  print('Bot logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='TESTING. DO NOT USE.'))

@bot.event
async def on_message(message):
  #Checks if the bot is the one who sent the message.
  if message.author == bot.user:
    return
  #Fuck you Atlas. Fuck. You.
  if message.content.lower() == '$discountatlas' or message.content.lower() == '$da' or message.content.lower() == '$q' or message.content.lower() == '$quote':
    quote = get_quote()
    await message.channel.send(quote)
  #HONK
  if "honk" in message.content.lower() or "goose" in message.content.lower():
    response = random.choice(honkQuotes)
    await message.channel.send(response)
  #To sista *winks with olives*
  if "eye" in message.content.lower():
      await message.add_reaction('👀')
  #Reacts to bread.
  if '🍞' in message.content() or '🥖' in message.content():
      await message.channel.send('is for me? <:goosebread:802019887542960148>')
  elif 'bread' in message.content.lower():
      await message.add_reaction('🍞')
  await bot.process_commands(message)

@bot.command()
#Amount of coins shenanigans.
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  wallet_amt = users[str(user.id)]["Wallet \N{EGG}"]
  bank_amt = users[str(user.id)]["Bank"]
  embed = discord.Embed(title= f"{ctx.author.name}'s balance", color= discord.Color.blue())
  embed.add_field(name = "Wallet", value = wallet_amt)
  embed.add_field(name = "Bank", value = bank_amt)
  await ctx.send(embed=embed)

async def open_account(user):
  users = await get_bank_data()
  with open("bank.json","r") as f:
    users = json.load(f)

  if str(user.id) in users:
    pass #Forgot what this does
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["Wallet \N{EGG}"]=0
    users[str(user.id)]["Bank"]=0

  with open("bank.json","w") as f:
    json.dump(users,f)


async def get_bank_data():
  with open("bank.json","r") as f:
    users = json.load(f)
  return users

#Sacrifice your bread to the Gods. Other ones should be leeching (make friends), dueling/stealing, gambling. 8ball should be a thing too. Racing as well, foraging. And army time, serenading, etc. You can buy and sell geese/items.
@bot.command()
async def sacrifice(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  earnings = random.randrange(-15-50)

  if earnings.isnumeric() == True:
    await ctx.send(f"The Goose Lord smiles upon you. You're mysteriously gifted {earnings} coins") #Eventually wanna make a list of these messages
  else:
    await ctx.send(f"You've angered the Gods. You lose {earnings} coins on the side of the road") #See comment above
  if earnings.isnumeric() == True or (earnings.isnumeric() == False and abs(earnings) <= wallet_amt):
    wallet_amt = users[str(user.id)]["Wallet \N{EGG}"] + earnings
  else:
    wallet_amt = 0
  with open("bank.json","w") as f:
    json.dump(users,f)

#This line is optional. mhm.
bot.run(os.getenv('ARGLE'))