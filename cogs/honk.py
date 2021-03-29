import discord
from discord.ext import commands
import os
import pymongo
import dns

cluster = pymongo.MongoClient(os.getenv('NOTCONNECTIONSTRING'))
levelling = cluster["disc0"]["honking"]
servercom = cluster["disc0"]["servercom"]

class Honk(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(aliases = ["hc"], brief = "Number of user honks.", description = "Number of user honks.")
  async def hcount(self, ctx): 
    stats = levelling.find_one({"id": ctx.author.id})
    honkNumber = 0 if stats is None else stats["honks"]
    name = ctx.message.author.display_name
    await ctx.send(f"User '{name}' has said 'honk' {honkNumber} times.")

  @commands.command(aliases = ["leaderboard"], brief = "Top Honkers.", description = "Lists the top honkers in your server. HONK.")
  async def lb(self, ctx, pplShown = None):
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
def setup(bot):
  bot.add_cog(Honk(bot))