import discord
import requests
from discord import app_commands
from discord.ext import commands
from config import API_KEY

class ResponsesCog(commands.Cog):
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
    
    @app_commands.command(name="weather")
    @app_commands.describe(city="Enter a city:")
    async def weather(self, interaction: discord.Interaction, city:str):
        """Receive current weather conditions for a specific city"""
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"  
        data = requests.get(url).json() 
        location = data['location']['name']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        temp_f = data['current']['temp_f']
        humidity = data['current']["humidity"]
        wind_kph = data['current']['wind_kph']
        wind_mph = data['current']['wind_mph']
        condition = data['current']['condition']['text']
        image_url = "http:" +data['current']['condition']['icon']
        embed = discord.Embed(color=discord.Colour.dark_blue(), title = f"Weather in {location}, {country}", description=f"The condition is {condition}")
        embed.add_field(name="Temperature", value=f"C: {temp_c} | F: {temp_f}")
        embed.add_field(name="Wind", value=f"{wind_kph} km/h | {wind_mph} mph")
        embed.add_field(name="Humidity", value=f"{humidity}%")
        embed.set_thumbnail(url=image_url)
        await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(ResponsesCog(bot))

