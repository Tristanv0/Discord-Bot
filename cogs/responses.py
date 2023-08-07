import discord
import random
from discord import app_commands
from discord.ext import commands

class ResponsesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Responses cog loaded")

    @app_commands.command(name="roll")
    async def roll(self, interaction: discord.Interaction):
        """Roll a dice and get a random number between 2 and 12"""
        random_number = random.randint(2, 12)
        embed = discord.Embed(colour=discord.Colour.dark_red(), title="Dice", description=f"🎲 You rolled a {random_number}!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """List of all commands"""
        embed = discord.Embed(colour=discord.Colour.dark_blue(), title="List of commands", description="``roll``   |    Roll a dice!")
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(ResponsesCog(bot))

