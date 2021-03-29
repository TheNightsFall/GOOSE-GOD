import discord
from discord.ext import commands
import os
import pymongo
import dns

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

class Util(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(aliases = ["a","abt"], brief = "Origins of the bot.", description = "Origins of the bot.")
  async def about(self,ctx):
    em = discord.Embed(title = "About", color= discord.Color.blue(),description = "On September 15th, Nights promised to make a bot that only responded to HONKS. That night, HONKERS, the bot now known as GOOSE GOD, was born. The project was left in a dusty python folder that didn't even bother using a .env file to hide its bot token, all the way until 1/21/21, when Nights decided that instead of studying for her two finals the day after, to instead pull up repl.it and being anew with the bot. Within two days it was a piece of shit that responds to honks. \n\nOk, enough poeticism. It's a fucking goose bot. What more do I have to say? *grumbles*")
    await ctx.send(embed = em)
  
  @commands.command(brief = "Disables commands.", description = "Disables certain commands, check $toggle for a list of what you can disable.")
  #*Immediately gets insulted for not using bits*. My own unique and terrible method of toggling commands.
  async def disable(self, ctx, com = None):
    global commandInt
    stats = servercom.find_one({"id": ctx.guild.id})
    if stats is None:
      newguild = {"id": ctx.guild.id, "commandint": 2310,}
      servercom.insert_one(newguild)
    stats = servercom.find_one({"id": ctx.guild.id})
    if com == None:
      await ctx.send("You can't disable no command, silly. HONK HONK. Type '$toggle' to see a list of what you can disable and enable.")
    else:
      try:
        if stats["commandint"]%commandInt[com] == 0:
          newInt = stats["commandint"]/commandInt[com]
          servercom.update_one({"id":ctx.guild.id}, {"$set":{"commandint": newInt}})
          await ctx.send("Command disabled *sniffs and honks*")
        else:
          await ctx.send("You've already disabled this command. HONK")
      except KeyError:
        await ctx.send("You can't disable a nonexistent command HONK~. Type '$toggle' to see a list of what you can disable and enable.")
  @commands.command(brief = "Enables commands.", description = "Enables certain commands, check $toggle for a list of what you can disable.")
  async def enable(self, ctx, com = None):
    global commandInt
    stats = servercom.find_one({"id": ctx.guild.id})
    if stats is None:
      newguild = {"id": ctx.guild.id, "commandint": 2310,}
      servercom.insert_one(newguild)
      await ctx.send("All commands are currently enabled. HONK.")
    stats = servercom.find_one({"id": ctx.guild.id})
    if com == None:
      await ctx.send("You have to list a command, silly. HONK ~. Type '$toggle' to see a list of what you can disable and enable.")
    else:
      try:
        if stats["commandint"]%commandInt[com] != 0:
          newInt = stats["commandint"]*commandInt[com]
          servercom.update_one({"id":ctx.guild.id}, {"$set":{"commandint": newInt}})
          await ctx.send("Command enabled *happy honking*")
        else:
          await ctx.send("You've already enabled this command. HONK")
      except KeyError:
        await ctx.send("You can't enable a nonexistent command HONK~. Type '$toggle' to see a list of what you can disable and enable.")
  @commands.command(brief = "List of toggleable commands.", description = "List of commands that can be disabled and enabled.")
  async def toggle(self, ctx):
    em = discord.Embed(title="Toggleable Commands", description="What you can turn off by typing after $disable.", color =discord.Color.blue())
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.add_field(name="Reactions", value = "Turns off all reactions but bread", inline=True)
    em.add_field(name="Parodies", value="Disables parody commands, like quotes and Twoset related commands.", inline=True)
    em.add_field(name="Battle", value="Can't battle others in your server", inline=True)
    em.add_field(name="Quests", value="Can't do quests in the server", inline=True)
    em.add_field(name="Honkresponse", value="Doesn't respond to honks. Still counts them.", inline=True)
    await ctx.send(embed = em)

def setup(bot):
  bot.add_cog(Util(bot))