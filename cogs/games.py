
import discord
import random
from discord import app_commands
from discord.ext import commands
from deck import *

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games cog loaded")

    @app_commands.command(name='blackjack')
    @app_commands.describe(bet="Enter a bet amount")
    async def bet(self, interaction: discord.Interaction, bet: str):
        """A classic game of Blackjack"""
        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                      title=f"{interaction.user.name}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{random.choice(DECK)} {random.choice(DECK)} \n\n**Dealer's Hand**\n{random.choice(DECK)}{FACEDOWN}")
        embed_message.set_footer(text=f"{interaction.user.name}'s bet: ${bet}")
        await interaction.response.send_message(embed=embed_message)

async def setup(bot):
    await bot.add_cog(GamesCog(bot))
