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
        else:
            user = user.name

        avatar = interaction.user.avatar
        balance = self.economy_system.get_user_balance(guild, user)
        bank = self.economy_system.get_user_bank(guild, user)
        embed = discord.Embed(colour=discord.Colour.yellow(),
                                    title=f"{user}'s Balance")
        embed.set_thumbnail(url=avatar)
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

    @work.error
    async def on_work_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='On Cooldown!', value=f'{str(error)}', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)    

async def setup(bot):
    await bot.add_cog(EconomyCog(bot, economy_system))