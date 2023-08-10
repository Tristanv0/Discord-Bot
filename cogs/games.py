import discord
import random
from discord import app_commands
from discord.ext import commands
from deck import DECK,FACEDOWN

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games cog loaded")

    @app_commands.command(name='blackjack')
    @app_commands.describe(bet="Enter a bet amount")
    async def bet(self, interaction: discord.Interaction, bet: str):
        """A classic game of Blackjack"""
        player_cards = []
        player_total = 0
        dealer_cards = []
        dealer_total = 0
        card = ''
        card_value = 0
        for i in range(2):
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            player_cards.append(card)
            player_total += card_value
            card = random.choice(list(DECK.keys()))
            card_value = DECK[card]
            dealer_cards.append(card)
            dealer_total += card_value
        dealer_cards.append(FACEDOWN)
        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                      title=f"{interaction.user.name}'s Blackjack Game", 
                                      description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\n")
        embed_message.set_footer(text=f"{interaction.user.name}'s bet: ${bet}")
        await interaction.response.send_message(embed=embed_message)


async def setup(bot):
    await bot.add_cog(GamesCog(bot))
