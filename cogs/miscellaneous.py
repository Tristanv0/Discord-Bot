import discord
from discord import app_commands
from discord.ext import commands


class MiscellaneousCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Responses cog loaded")

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """List of all commands"""
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Command List", icon_url="http://discord.com/assets/7c8f476123d28d103efe381543274c25.png")
        embed.add_field(name=":speech_balloon: General (2)", value="``/ping`` , ``/weather``", inline=False)
        embed.add_field(name=":game_die: Games (4)", value="``8ball`` , ``/blackjack`` , ``/coinflip`` , ``/roll``", inline=False)
        embed.add_field(name=":musical_note: Music (5)", value="``/play`` , ``/pause`` , ``/resume`` , ``/skip`` , ``/queue``", inline=False)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        """A simple ping command"""
        embed = discord.Embed(colour=discord.Colour.brand_green(), title=f":ping_pong: Pong! {round(self.bot.latency*1000)}ms")
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(MiscellaneousCog(bot))

