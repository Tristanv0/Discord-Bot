import discord
import random
from discord import app_commands
from discord.ext import commands
from deck import *
from economy import Economy
from cogs.games import GamesCog

#Creates an instance of Economy
database_path = 'economy_database.db' 
economy_system = Economy(database_path)


class BaccaratCog(commands.Cog):
    def __init__(self, bot, economy_system):
        self.bot = bot
        self.economy_system = economy_system
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Baccarat cog loaded")

    @app_commands.command(name="baccarat")
    @app_commands.describe(player="Bet on player")
    @app_commands.describe(banker="Bet on banker")
    @app_commands.describe(tie='Bet on tie')
    async def baccarat(self, interaction:discord.Interaction, player:int=None, banker:int=None, tie:int=None): # will only accept int inputs
        """Baccarat"""
        guild_id = interaction.user.guild.id
        user = interaction.user.name
        if (player == None) and (banker == None) and (tie == None):
            embed= discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="You have to place a bet!", inline=False)
            await interaction.response.send_message(embed=embed)
            return
        
        bet = 0
        if player != None:
            bet += player
        if banker != None:
            bet += banker
        if tie != None:
            bet += tie

        #check for eligibility
        eligibilty = GamesCog.check_game_eligibility(guild_id, user, str(bet))
        if eligibilty != None:
            await interaction.response.send_message(embed=eligibilty)
            return
        
        economy_system.update_user_balance(guild_id, user, int(bet))
        player_cards = []
        player_card_values = []
        banker_cards = []
        banker_card_values = []
        card = ''
        card_value = 0
        #pull 2 random cards for player and dealer
        for i in range(2):
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            player_card_values.append(card_value)
            player_cards.append(card)
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            banker_card_values.append(card_value)
            banker_cards.append(card)
            
        player_total = (player_card_values[0] + player_card_values[1]) % 10
        banker_total = (banker_card_values[0] + banker_card_values[1]) % 10

        #natural win
        if player_total > 7 or banker_total > 7:
            if player_total == banker_total:
                embed_message = discord.Embed(colour=discord.Colour.purple(),
                                        description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**It's a Tie**")
                embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
                if tie != None:
                    economy_system.user_winning(guild_id, user, bet+tie*8)
                    embed_message.set_footer(text=f"{user} won: ${bet+tie*8} (bet total: ${bet})")
                else:
                    economy_system.user_winning(guild_id, user, bet)
                    embed_message.set_footer(text=f"{user} pushed: ${bet}")
                await interaction.response.send_message(embed=embed_message)
                return
            elif player_total > banker_total:
                embed_message = discord.Embed(colour=discord.Colour.blue(),
                                        description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**Natural win for Player**")
                embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
                if player != None:
                    economy_system.user_winning(guild_id, user, player*2)
                    embed_message.set_footer(text=f"{user} won: ${player*2} (bet total: ${bet})")
                else:
                    embed_message.set_footer(text=f"{user} lost: ${bet}")
                await interaction.response.send_message(embed=embed_message)
                return
            elif banker_total > player_total:
                embed_message = discord.Embed(colour=discord.Colour.red(),
                                        description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**Natural win for Banker**")
                embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
                if banker != None:
                    economy_system.user_winning(guild_id, user, banker*1.95)
                    embed_message.set_footer(text=f"{user} won: ${banker*1.95} (bet total: ${bet})")
                else:
                    embed_message.set_footer(text=f"{user} lost: ${bet}")
                await interaction.response.send_message(embed=embed_message)
                return
            
        elif player_total == 6 or player_total == 7:
            if banker_total <= 5:
                card = random.choice(list(DECK.keys()))
                card_value = DECK[card]
                banker_card_values.append(card_value)
                banker_cards.append(card)

        
        elif player_total <= 5:
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            player_card_values.append(card_value)
            player_cards.append(card)
            player_total += card_value 
            
            if banker_total <= 2:
                card = random.choice(list(DECK.keys()))
                card_value = DECK[card]
                banker_card_values.append(card_value)
                banker_cards.append(card)
                banker_total += card_value 
                
            elif banker_total == 3:
                if player_card_values[2] != 8 :
                    #if banker total is 3 and player third card is NOT 8:
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    banker_card_values.append(card_value)
                    banker_cards.append(card)
                    banker_total += card_value 
            
            elif banker_total == 4:
                if player_card_values[2] % 10 >= 2 and player_card_values[2] % 10 <= 7:
                    #2, 3, 4, 5, 6, 7
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    banker_card_values.append(card_value)
                    banker_cards.append(card)
                    banker_total += card_value 
            
            elif banker_total == 5:
                if player_card_values[2] % 10 >= 4 and player_card_values % 10 <= 7:
                    # 4, 5, 6, 7
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    banker_card_values.append(card_value)
                    banker_cards.append(card)
                    banker_total += card_value 
            
            elif banker_total == 6:
                if player_card_values[2] % 10 == 6 or player_card_values[2] % 10 == 7:
                    # 6, 7
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    banker_card_values.append(card_value)
                    banker_cards.append(card)
                    banker_total += card_value 
        
        player_total %= 10
        banker_total %= 10
        if player_total == banker_total:
            embed_message = discord.Embed(colour=discord.Colour.purple(),
                                          description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**It's a tie**")
            embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
            if tie != None:
                    economy_system.user_winning(guild_id, user, bet+tie*8)
                    embed_message.set_footer(text=f"{user} won: ${bet+tie*8} (bet total: ${bet})")
            else:
                economy_system.user_winning(guild_id, user, bet)
                embed_message.set_footer(text=f"{user} pushed: ${bet}")
            await interaction.response.send_message(embed=embed_message)
            return
                
        if player_total > banker_total:
            embed_message = discord.Embed(colour=discord.Colour.blue(),
                                          description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**Player wins**")
            embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
            if player != None:
                economy_system.user_winning(guild_id, user, player*2)
                embed_message.set_footer(text=f"{user} won: ${player*2} (bet total: ${bet})")
            else:
                embed_message.set_footer(text=f"{user} lost: ${bet}")
            await interaction.response.send_message(embed=embed_message)
            return
            
        if player_total < banker_total:
            embed_message = discord.Embed(colour=discord.Colour.red(),
                                          description=f"**Player Hand**\n{''.join(card for card in player_cards)}\nPlayer hand: {player_total}\n\n**Banker Hand**\n{''.join(card for card in banker_cards)}\nBanker hand: {banker_total}\n\n**Banker wins**")
            embed_message.set_author(name=f"{user}'s Baccarat Game" , icon_url=interaction.user.display_avatar)
            if banker != None:
                economy_system.user_winning(guild_id, user, banker*1.95)
                embed_message.set_footer(text=f"{user} won: ${banker*1.95} (bet total: ${bet})")
            else:
                embed_message.set_footer(text=f"{user} lost: ${bet}")
            await interaction.response.send_message(embed=embed_message)
            return
            
            
async def setup(bot):
    await bot.add_cog(BaccaratCog(bot, economy_system))