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


    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """List of all commands"""
        embed = discord.Embed(colour=discord.Colour.dark_blue(), title="List of commands", description="``roll``   |    Roll a dice!")
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(ResponsesCog(bot))

