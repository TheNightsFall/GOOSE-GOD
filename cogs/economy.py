
import discord
from discord.ext import commands
import os
import random
import asyncio
import math #oh god oh no
import pymongo
import dns

cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]
servercom = cluster["disc0"]["servercom"]

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(brief = "Free bread.", description = "Free bread.")
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

  @commands.command(aliases = ["bal"], brief = "Checks your balance.", description = "Checks your balance.")
  async def balance(self, ctx):
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 0,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
      print("New User made.")
    stats = levelling.find_one({"id": ctx.author.id})
    bread = stats["balance"]
    coins = stats["coins"] #Coins can only be gained by doing quests
    bal = 1000*int(stats["coins"]) + int(stats["balance"])
    embed = discord.Embed(title= f"{ctx.author.display_name}'s balance", color= discord.Color.blue()) #This might also change as you get $
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name = "Bread", value = bread)
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

  #Feeling hungry, might remove later
  @commands.command(aliases = ["exchange"], brief = "Convert bread to coins.", description = "Convert bread to coins.")
  async def convert(self, ctx):
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 1,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
      await ctx.send("You have nothing to convert.")
    else:
      cans = math.floor(stats["balance"]/1000)
      if cans != 0:
        bal = int(stats["balance"])-cans*1000
        levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
        levelling.update_one({"id":ctx.author.id}, {"$set":{"coins":cans}})
        await ctx.send("Converted "+str(cans*1000)+" bread into "+str(cans)+ " coins. HONK")
      else:
        await ctx.send("You're too poor, HONK. You need 1000 bread per coin.")
  @commands.command(aliases = ["sac","sc","sf"], brief = "Sacrifice for bread.", description = "Sacrifice to the Gods, hoping for some bread.")
  @commands.cooldown(15, 21600, commands.BucketType.user)
  async def sacrifice(self, ctx):
    sacrificePositive = ["<:goosepizza:802019887546368021> PIZZA. You gain","The skies open and a goose-shaped cloud gives you","Your friends think you've gone insane, praying to a Goose God. But you know better, and you've been rewarded with","The Goose Lord smiles upon you. You're mysteriously gifted","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","You really suck at sacrificing and accidently duplicate some of your coins instead. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive","The Goose God smiles upon you. You receive"]
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
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      await asyncio.sleep(2)
      await message.edit(content=response)
    elif earnings < 0:
      earnings *= -1
      message = await ctx.send("Sacrificing <a:gooserun:802019886846967869>")
      await asyncio.sleep(2)
      await message.edit(content=f"You've angered the Gods. You lose {earnings} bread on the side of the road.") 
      earnings *= -1
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
  
  @commands.command(aliases = ["coin","cf", "coinflip"], brief = "Flips a coin.", description = "Flips a coin.")
  @commands.cooldown(2, 3, commands.BucketType.user)
  async def flip(self, ctx, sideChosen = None):
    userChoice = 0
    if sideChosen == None:
      await ctx.send("Type 'heads' if you call heads and 'tails' if you call tails.")
    elif sideChosen.lower() == 'heads' or sideChosen.lower() == 'head' or sideChosen.lower() == 'h':
      userChoice = 2
    elif sideChosen.lower() == 'tails' or sideChosen.lower() == 'tail' or sideChosen.lower() == 't':
      userChoice = 3
    else:
      await ctx.send("Invalid argument. Type 'heads' if you call heads and 'tails' if you call tails.")
    compChoice = random.randint(2,3)
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 0,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
      print("New User made.")
    stats = levelling.find_one({"id": ctx.author.id})
    if userChoice == compChoice and userChoice != 0:
      w = "You won **15** bread! HONK."
      if stats["balance"] != 0:
        bal = stats["balance"] + 15
      else:
        bal = 15
      levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
    elif userChoice != 0:
      w= "You lost **15** bread. honk."
      if stats["balance"] >= 15:
        bal = stats["balance"] - 15
        levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
    if compChoice == 2 and userChoice != 0:
      await ctx.send(":coin: The coin landed on heads! "+w)
    elif userChoice != 0:
      await ctx.send(":coin: The coin landed on tails! "+w)
  
  @commands.command(aliases = ["race"], brief = "Go racing, see if you win.", description = "Go racing, see if you win.")
  async def racing(self, ctx, amt = None):
    amt = 10 if amt == None or amt.isnumeric() == False else int(amt)
    n = random.randint(1,5)
    stats = levelling.find_one({"id": ctx.author.id})
    if stats is None:
      newuser = {"id": ctx.author.id, "honks": 0, "balance": 0,"coins": 0, "quests": 0}
      levelling.insert_one(newuser)
      print("New User made.")
    stats = levelling.find_one({"id": ctx.author.id})
    if n == 1:
      bal = int(stats["balance"]) + amt*3 if stats["balance"] != 0 else amt*3
    else:
      bal = int(stats["balance"]) - amt if stats["balance"] != 0 and amt <= stats["balance"] else 0
    levelling.update_one({"id":ctx.author.id}, {"$set":{"balance":bal}})
    amt3 = 3*amt
    result = f"You won the race and gained {amt3} bread." if n == 1 else f"You lost the race and lose {amt} bread."
    message = await ctx.send("Racing <a:pepegoose:802019887337439303>")
    await asyncio.sleep(3)
    await message.edit(content=result)

  @commands.command(aliases = ["breadlb","bleaderboard","breadleaderboard"], brief = "Top breadwinners.", description = "Lists the top breadwinners in your server.")
  async def blb(self, ctx, pplShown = None):
    pplShown = 5 if pplShown == None or pplShown.isnumeric() == False else int(pplShown)
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

def setup(bot):
  bot.add_cog(Economy(bot))