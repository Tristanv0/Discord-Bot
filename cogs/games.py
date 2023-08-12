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
    
    @app_commands.command(name="roll")
    async def roll(self, interaction: discord.Interaction):
        """Roll a dice and get a random number between 2 and 12"""
        random_number = random.randint(2, 12)
        embed = discord.Embed(colour=discord.Colour.dark_red(), title="Dice", description=f"🎲 You rolled a {random_number}!")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='blackjack')
    @app_commands.describe(bet="Enter a bet amount")
    async def bet(self, interaction: discord.Interaction, bet: str):
        """A classic game of Blackjack"""
        player = interaction.user.name
        player_cards = []
        player_total = 0
        player_card_values = []
        dealer_cards = []
        dealer_total = 0
        dealer_card_values = []
        card = ''
        card_value = 0
        for i in range(2):
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            player_card_values.append(card_value)
            player_cards.append(card)
            player_total += card_value
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            dealer_card_values.append(card_value)
            dealer_cards.append(card)
            dealer_total += card_value
        dealer_cards.append(FACEDOWN)
        
        
        hit = discord.ui.Button(
            label='Hit',
            style= discord.ButtonStyle.green
        )
        stand = discord.ui.Button(
            label='Stand',
            style=discord.ButtonStyle.red
        )
        b3 = discord.ui.Button(
            label='Double Down',
            style=discord.ButtonStyle.blurple
        )
        b4 = discord.ui.Button(
            label="Split",
            style=discord.ButtonStyle.grey
        )

        view = discord.ui.View()
        view.add_item(hit)
        view.add_item(stand)
        view.add_item(b3)
        if player_card_values[0] == player_card_values[1]:
            view.add_item(b4)
            
        
        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\n\n")
        embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
            
        async def hit_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                card = random.choice(list(DECK.keys()))
                card_value = DECK[card]
                player_card_values.append(card_value)
                player_cards.append(card)
                player_total = 0
                for value in player_card_values:
                    player_total += value
            
                if player_total >= 22:
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[1]}\n\n **You** busted! Better luck next time.")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    await interaction.response.edit_message(embed=embed_message, view=None)
                else:
                    embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\n")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    view.remove_item(b3)
                    if player_card_values[0] == player_card_values[1]:
                        view.remove_item(b4)
                    await interaction.response.edit_message(embed=embed_message, view=view)
        
        async def stand_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                dealer_total = 0
                for value in dealer_card_values:
                    dealer_total += value
                while dealer_total < 17:
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    dealer_cards.append(card)
                    dealer_total += card_value
                dealer_cards.remove('<:backside:1138692953141948476>')
                if dealer_total > 21:
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** The dealer busts!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*2}")
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total > dealer_total:
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** You beat the dealer!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*2}")
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total == dealer_total:
                    embed_message = discord.Embed(colour=discord.Colour.orange(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n It's a push.")
                    embed_message.set_footer(text=f"{player} pushed: ${int(bet)}")
                    await interaction.response.edit_message(embed=embed_message, view=None)

                else:
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                      title=f"{player}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n The **dealer** won this time. Better luck next time.")
                    embed_message.set_footer(text=f"{player} lost: ${int(bet)}")
                    await interaction.response.edit_message(embed=embed_message, view=None)

        #async def doubledown_callback(interaction:discord.Interaction):
        #async def split_callback(interaction:discord.Interaction):
        hit.callback = hit_callback
        stand.callback = stand_callback
        #doubledown.callback = doubledown_callback
        #split.callback = split_callback
        await interaction.response.send_message(embed=embed_message, view=view)


async def setup(bot):
    await bot.add_cog(GamesCog(bot))
