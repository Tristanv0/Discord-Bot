from economy import Economy
import random
import discord
from discord import app_commands
from discord.ext import commands

#Creates an instance of Economy
database_path = 'economy_database.db' 
economy_system = Economy(database_path)

class EconomyCog(commands.Cog):
    def __init__(self, bot, economy_system):
        self.bot = bot
        self.economy_system = economy_system
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy cog loaded")
        
    @app_commands.command(name='bal')
    @app_commands.describe(user='Enter the username')
    @app_commands.autocomplete()
    async def bal(self, interaction: discord.Interaction, user: discord.Member = None):
        """Check the balance of anyone in the server"""
        guild = interaction.user.guild.id
        if not user:
            user = interaction.user.name
            avatar = interaction.user.display_avatar
        else:
            avatar = user.display_avatar
            user = user.name 
        balance = self.economy_system.get_user_balance(guild, user)
        bank = self.economy_system.get_user_bank(guild, user)
        embed = discord.Embed(colour=discord.Colour.yellow())
        embed.set_author(name=f"{user}'s Balance", icon_url=avatar)
        if balance is not None:
            embed.add_field(name=f"Cash", value=f"${balance}", inline=True)
            embed.add_field(name=f"Bank", value=f"${bank}", inline=True)
            embed.add_field(name=f"Total", value=f"{bank+balance}",inline=True)
            await interaction.response.send_message(embed=embed)
 
        else:
            balance = 100
            bank = 0
            self.economy_system.insert_user(guild, user, balance, bank)
            embed.add_field(name=f"Cash", value=f"${balance}", inline=True)
            embed.add_field(name=f"Bank", value=f"${bank}", inline=True)
            embed.add_field(name=f"Total", value=f"{bank+balance}",inline=True)
            await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name='work')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def work(self,interaction: discord.Interaction):
        """Go to work"""
        guild = interaction.user.guild.id
        user = interaction.user.name
        pay = random.randint(80, 150)
        self.economy_system.user_winning(guild, user, pay)
        embed = discord.Embed(colour=discord.Colour.green())
        embed.add_field(name="Work", value=f"After a hard day of work, you earned ``${pay}``!", inline=False)
        await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name='deposit')
    @app_commands.describe(amount="Enter amount to deposit")
    @app_commands.checks.cooldown(1, 2.0, key=lambda i: (i.guild_id, i.user.id))
    async def deposit(self, interaction: discord.Interaction, amount: str):
        """Deposit cash into your bank"""
        guild = interaction.user.guild.id
        user = interaction.user.name
        if amount == 'all':
            cash = economy_system.get_user_balance(guild, user)
            economy_system.deposit(guild, user, cash)
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.add_field(name='', value=f"Successfully ``deposited`` ``${cash}`` into your bank!", inline=False)
            await interaction.response.send_message(embed=embed)
        elif amount.isnumeric():
            balance = economy_system.get_user_balance(guild, user)
            if balance >= int(amount):
                economy_system.deposit(guild, user, int(amount))
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.add_field(name='', value=f"Successfully ``deposited`` ``${amount}`` into your bank!", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.add_field(name='', value=f"You don't have enough on you to deposit ``${amount}`` into your bank.", inline=False)
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value=f"You must enter a ``numeric`` value or ``all``!", inline=False)
            await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name='withdraw')
    @app_commands.describe(amount="Enter amount to withdraw")
    @app_commands.checks.cooldown(1, 2.0, key=lambda i: (i.guild_id, i.user.id))
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        """withdraw cash from your bank"""
        guild = interaction.user.guild.id
        user = interaction.user.name
        if amount == 'all':
            bank_balance = economy_system.get_user_bank(guild, user)
            economy_system.withdraw(guild, user, bank_balance)
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.add_field(name='', value=f"Successfully ``withdrew`` ``${bank_balance}`` from your bank!", inline=False)
            await interaction.response.send_message(embed=embed)
        elif amount.isnumeric():
            bank = economy_system.get_user_bank(guild, user)
            if bank >= int(amount):
                economy_system.withdraw(guild, user, int(amount))
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.add_field(name='', value=f"Successfully ``withdrew`` ``${amount}`` from your bank!", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.add_field(name='', value=f"You don't have enough in your bank to withdraw ``${amount}``.", inline=False)
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value=f"You must enter a ``numeric`` value or ``all``!", inline=False)
            await interaction.response.send_message(embed=embed)
    
    @work.error
    async def on_work_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='On Cooldown!', value=f'{str(error)}', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)    
    
    @deposit.error
    async def on_deposit_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='On Cooldown!', value=f'{str(error)}', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True) 
    
    @withdraw.error
    async def on_deposit_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='On Cooldown!', value=f'{str(error)}', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True) 
            
async def setup(bot):
    await bot.add_cog(EconomyCog(bot, economy_system))