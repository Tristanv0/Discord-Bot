import discord
import random
from discord import app_commands
from discord.ext import commands
from deck import *
from economy import Economy


#Creates an instance of Economy
database_path = 'economy_database.db' 
economy_system = Economy(database_path)

class GamesCog(commands.Cog):
    def __init__(self, bot, economy_system):
        self.bot = bot
        self.economy_system = economy_system

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games cog loaded")
    
    @staticmethod
    def check_game_eligibility(guild_id, player, bet):
        #to check if player is eligible to play a game with a required bet (e.g. blackjack)
        
        #for first time users who has no data in database
        if economy_system.get_user_balance(guild_id, player) == None:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="``/work`` or ``/bal`` first before gambling your life away!!", inline=False)
            return embed
        
        #for string input in bet
        if (bet.isalpha() and bet == 'all'):
            bet = economy_system.get_user_balance(guild_id, player)
        elif (bet.isalpha() and bet != 'all'):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="You must enter a ``numeric`` value or ``'all'`` when placing a bet.", inline=False)
            return embed
        
        #for integer input
        if int(bet) < 10:       #min bet of $10
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="There is a minimum bet of ``$10``", inline=False)
            return embed
        
        #check if bet amount larger than what player can afford
        if economy_system.get_user_balance(guild_id, player) < int(bet):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value=f'You cannot afford to bet ``${bet}``', inline=False)
            return embed
        
        return None
        
    @app_commands.command(name="8ball")
    @app_commands.describe(question="Ask me a question")
    async def eight_ball(self, interaction: discord.Interaction, question:str):
        """Ask the magic 8ball"""
        choice = random.choice(["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see yes", "Most likely", "Outlook good", 
                                "Yes", "Signs point to yes", "Reply Hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", 
                                "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"])
        embed = discord.Embed(colour=discord.Colour.dark_grey())
        embed.add_field(name=f" {interaction.user.name}: {question}", value = "", inline=False)
        embed.add_field(name = "", value = "", inline=False)
        embed.add_field(name=f":8ball: {choice}.", value = "", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip")
    async def coinflip(self, interaction: discord.Interaction):
        """Flip a coin"""
        flip = random.choice(["Heads", "Tails"])
        embed = discord.Embed(colour=discord.Colour.dark_gold(), description=f":coin: {flip}!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roll")
    async def roll(self, interaction: discord.Interaction):
        """Roll a dice and get a random number between 2 and 12"""
        random_number = random.randint(2, 12)
        embed = discord.Embed(colour=discord.Colour.red(), description=f"🎲 You rolled a **{random_number}**!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesCog(bot, economy_system))
