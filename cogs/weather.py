import discord
import requests
from discord import app_commands
from discord.ext import commands
from config import API_KEY

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather cog loaded")
        
    @app_commands.command(name="weather")
    @app_commands.describe(city="Enter a city")
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
    await bot.add_cog(WeatherCog(bot))