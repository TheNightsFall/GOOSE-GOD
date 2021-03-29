import discord
from discord.ext import commands
import requests
import json
import random
import asyncio
from PIL import Image
from io import BytesIO

class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #Grabs a random quote. Atlas, you suck. Get one-upped.
  def get_quote(self):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = '"'+json_data[0]['q']+'"\n\t - ' + json_data[0]['a']
    return(quote)

  @commands.command(aliases = ["q","da","discountatlas"], brief = "Fetches a quote.", description = "Fetches a quote.")
  async def quote(self, ctx):
    quote = self.get_quote()
    await ctx.send(quote)

  @commands.command(brief = "Get chased by a crowd.", description = "Get chased by a crowd.")
  async def chased(self,ctx, user:discord.Member = None):
    if user == None:
      user = ctx.author
    chasing = Image.open("images/image1/chasing.jpg")
    asset = user.avatar_url_as(size=64)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((171,171))
    chasing.paste(pfp, (1523,514))
    chasing.save("images/image1/chasingp.jpg") 
    await ctx.send(content = f"{user.display_name} gets chased!",file = discord.File("images/image1/chasingp.jpg"))

  
  @commands.command(brief = "Honks at someone.", description = "Honks at someone.")
  async def honk(self, ctx, user: discord.User=None):
    if user == None:
      await ctx.send("You can't honk at yourself, silly!")
    else:
      await ctx.send(f"{ctx.author.display_name} honked at {user.mention}!")
  
  @commands.command(aliases = ["mc", "cook"], brief = "Microwaves some food.", description = "MMMMMMMMMM")
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def microwave(self, ctx):
    #Clearly I know how to cook
    foodGloriousFood = [":potato:",":bread:",":peanuts:",":meat_on_bone:",":pizza:",":corn:",":coffee:",":pie:",":honeypot:",":watermelon:",":banana:",":pineapple:",":french_bread:",":hotdog:",":taco:",":salad:",":rice:",":sushi:",":spoon:", "a broken microwave.", "mail",]
    borkBork = random.choice(foodGloriousFood)
    timeLeft = 5
    message = await ctx.send("<:microwave:813862298522877984> Microwaving...please wait **"+str(timeLeft)+"** seconds")
    for x in range(0,5):
      await asyncio.sleep(1)
      timeLeft -= 1
      await message.edit(content="<:microwave:813862298522877984> Microwaving...please wait **"+str(timeLeft)+"** seconds")
    await message.edit(content="You got "+borkBork)
  #Why do I need a ping command? Idk man
  @commands.command(brief = "Ping pong.", description = "Ping pong.")
  async def ping(self, ctx):
      if round(self.bot.latency * 1000) <= 50:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(self.bot.latency *1000)}** milliseconds! What a gamer! HONK!!", color=0x44ff44)
      elif round(self.bot.latency * 1000) <= 100:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(self.bot.latency *1000)}** milliseconds! Still decent. honk.", color=0xffd000)
      elif round(self.bot.latency * 1000) <= 200:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(self.bot.latency *1000)}** milliseconds! honk?", color=0xff6600)
      else:
        embed=discord.Embed(title="PONG", description=f":ping_pong: The ping is **{round(self.bot.latency *1000)}** milliseconds! Get that internet checked. hon-- *lags out*", color=0x990000)
      await ctx.send(embed=embed)
def setup(bot):
  bot.add_cog(Misc(bot))