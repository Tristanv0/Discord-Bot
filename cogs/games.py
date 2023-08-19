import discord
import time
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
    
    
    
    @app_commands.command(name='blackjack')
    @app_commands.describe(bet="Enter a bet amount")
    async def bet(self, interaction: discord.Interaction, bet: str):
        """A classic game of Blackjack"""
        guild_id = interaction.user.guild.id
        player = interaction.user.name
        
        #for first time users who has no data in database
        if economy_system.get_user_balance(guild_id, player) == None:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="``/work`` or ``/bal`` first before gambling your life away!!", inline=False)
            await interaction.response.send_message(embed=embed)
            return
        
        #for string input in bet
        if (bet.isalpha() and bet == 'all'):
            bet = economy_system.get_user_balance(guild_id, player)
        elif (bet.isalpha() and bet != 'all'):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="You must enter a ``numeric`` value or ``'all'`` when placing a bet.", inline=False)
            await interaction.response.send_message(embed=embed)
            return
        
        #for integer input
        if int(bet) < 10:       #min bet of $10
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value="There is a minimum bet of ``$10``", inline=False)
            await interaction.response.send_message(embed=embed)
            return

        if economy_system.get_user_balance(guild_id, player) < int(bet):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name='', value=f'You cannot afford to bet ``${bet}``', inline=False)
            await interaction.response.send_message(embed=embed)
            return
   
        economy_system.update_user_balance(guild_id, player, int(bet))
        player_cards = []
        player_total = 0
        player_card_values = []
        dealer_cards = []
        dealer_total = 0
        dealer_card_values = []
        card = ''
        card_value = 0
        player_soft = False
        
        #pull 2 random cards for player and dealer
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
        
        yes = discord.ui.Button(
            label='Yes',
            style= discord.ButtonStyle.green
        )
        no = discord.ui.Button(
            label='No',
            style=discord.ButtonStyle.red
        )
        hit = discord.ui.Button(
            label='Hit',
            style= discord.ButtonStyle.green
        )
        stand = discord.ui.Button(
            label='Stand',
            style=discord.ButtonStyle.red
        )
        doubledown = discord.ui.Button(
            label='Double Down',
            style=discord.ButtonStyle.blurple
        )
        split = discord.ui.Button(
            label="Split",
            style=discord.ButtonStyle.grey
        )
        view = discord.ui.View()
        gamebutton = discord.ui.View()
        
        #checking for aces
        if 1 in player_card_values:
            ace_index = player_card_values.index(1)
            player_card_values[ace_index] += 10
            player_total += 10
            player_soft = True
            
        if 1 in dealer_card_values:
            ace_index = dealer_card_values.index(1)
            dealer_card_values[ace_index] += 10
            dealer_total += 10

        if player_total == 21:
            if dealer_total == 21:
                embed_message = discord.Embed(colour=discord.Colour.orange(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: Blackjack\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards[0:2])}\nDealer's hand: Blackjack\n\n You and the dealer got Blackjack. Its a push")
                embed_message.set_footer(text=f"{player} won: ${int(bet)}")
                winning = int(bet)
                economy_system.user_winning(guild_id, player, winning)
                await interaction.response.send_message(embed=embed_message, view=None) 
            else:
                del dealer_cards[-1]
                embed_message = discord.Embed(colour=discord.Colour.green(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: Blackjack\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **BLACKJACK!!** Nice job!")
                embed_message.set_footer(text=f"{player} won: ${int(bet)*2.5}")
                winning = int(bet)*2.5
                economy_system.user_winning(guild_id, player, winning)
                await interaction.response.send_message(embed=embed_message, view=None)
            
        #offer insurance if dealer's first card is an ace  
        if dealer_card_values[0] == 11:
            if player_soft:
                embed_message = discord.Embed(colour=discord.Colour.purple(),
                                            title=f"{player}'s Blackjack Game\nInsurance?",
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
            else:
                embed_message = discord.Embed(colour=discord.Colour.purple(),
                                            title=f"{player}'s Blackjack Game\nInsurance?",
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
            view.add_item(yes)
            view.add_item(no)
            await interaction.response.send_message(embed=embed_message, view=view)       
        
        if dealer_card_values[0] != 11 and dealer_total == 21:
            del dealer_cards[-1]
            embed_message = discord.Embed(colour=discord.Colour.red(), 
            title=f"{player}'s Blackjack Game", 
            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's hand: Blackjack\n\n Dealer got **Blackjack**.")
            embed_message.set_footer(text=f"{player} lost: ${bet}")
            
            
        async def yes_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                insurance = int(bet) / 2
                economy_system.update_user_balance(guild_id, player, insurance)
                if dealer_total == 21:
                    winning = insurance*3
                    economy_system.user_winning(guild_id, player, winning)
                    del dealer_cards[-1]
                    if player_soft:
                        embed_message = discord.Embed(colour=discord.Colour.green(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's hand: Blackjack\n\n Dealer got **Blackjack**.")
                        embed_message.set_footer(text=f"{player} won: ${winning} (Insurance)")
                    else:
                        embed_message = discord.Embed(colour=discord.Colour.green(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's hand: Blackjack\n\n Dealer got **Blackjack**.")
                        embed_message.set_footer(text=f"{player} won: ${winning} (Insurance)")
                    await interaction.response.edit_message(embed=embed_message, view=None) 
                else:
                    if player_soft:
                        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                            title=f"{player}'s Blackjack Game\nDealer doesn't have Blackjack.", 
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                        embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    else:
                        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                            title=f"{player}'s Blackjack Game\nDealer doesn't have Blackjack.", 
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                        embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    gamebutton = discord.ui.View()
                    gamebutton.add_item(hit)
                    gamebutton.add_item(stand)
                    gamebutton.add_item(doubledown)
                    await interaction.response.edit_message(embed=embed_message, view=gamebutton)

        async def no_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                if dealer_total == 21:
                    del dealer_cards[-1]
                    if player_soft:
                        embed_message = discord.Embed(colour=discord.Colour.red(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's hand: Blackjack\n\n Dealer got **Blackjack**.")
                        embed_message.set_footer(text=f"{player} lost: ${bet}")
                    else:
                        embed_message = discord.Embed(colour=discord.Colour.red(), 
                        title=f"{player}'s Blackjack Game", 
                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour hand: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's hand: Blackjack\n\n Dealer got **Blackjack**.")
                        embed_message.set_footer(text=f"{player} lost: ${bet}")
                    await interaction.response.edit_message(embed=embed_message, view=None)
                else:
                    if player_soft:
                        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                            title=f"{player}'s Blackjack Game\nDealer doesn't have Blackjack.", 
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                        embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    else:
                        embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                            title=f"{player}'s Blackjack Game\nDealer doesn't have Blackjack.", 
                                            description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                        embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}") 
                                                    
                    gamebutton = discord.ui.View()
                    gamebutton.add_item(hit)
                    gamebutton.add_item(stand)
                    gamebutton.add_item(doubledown)
                    await interaction.response.edit_message(embed=embed_message, view=gamebutton)
                    
        if player_soft is False:
            embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
            embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
        else: 
            embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
            embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")

        gamebutton.add_item(hit)
        gamebutton.add_item(stand)
        if self.economy_system.get_user_balance(guild_id, player) >= int(bet):
            gamebutton.add_item(doubledown)
        if player_card_values[0] == player_card_values[1]:
            gamebutton.add_item(split)
        
        if player_soft is False:
            embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
            embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
        else: 
            embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
            embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
            
        async def hit_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                if 11 in player_card_values:
                    player_soft = True
                else:
                    player_soft = False
                card = random.choice(list(DECK.keys()))
                card_value = DECK[card]
                if (card_value == 1) and (1 not in player_card_values) and (sum(player_card_values) <= 10): #e.g. 5, 5, and pulls an ace
                    card_value += 10    #card_value should have value of 11
                    player_soft = True  #player has soft 20
                        
                player_card_values.append(card_value)      #[5, 5, 11]
                player_cards.append(card)
                player_total = 0
                player_total = sum(player_card_values)      #5+5+11=21
                if (player_total >= 22) and (player_soft == False): #hard value above 21 = loss
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[1]}\n\n **You** busted! Better luck next time.")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    await interaction.response.edit_message(embed=embed_message, view=None)
                
                elif (player_total >= 22) and (player_soft == True): #soft value above 21, subtract 10 and that becomes hard value
                    ace_index = player_card_values.index(11)
                    player_card_values[ace_index] -= 10
                    player_total -= 10
                    player_soft = False
                    embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    gamebutton.remove_item(doubledown)
                    gamebutton.remove_item(split)
                    await interaction.response.edit_message(embed=embed_message, view=gamebutton)
                    
                elif (player_total < 21) and (player_soft == True):
                    embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total-10}/{player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    gamebutton.remove_item(doubledown)
                    gamebutton.remove_item(split)
                    await interaction.response.edit_message(embed=embed_message, view=gamebutton)

                else:
                    embed_message = discord.Embed(colour=discord.Colour.purple(), 
                                        title=f"{player}'s Blackjack Game", 
                                        description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[2]}\nDealer's up card: {dealer_card_values[0]}\n\n")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)}")
                    gamebutton.remove_item(doubledown)
                    if player_card_values[0] == player_card_values[1]:
                        gamebutton.remove_item(split)
                    await interaction.response.edit_message(embed=embed_message, view=gamebutton)
        
        
        
        
        async def stand_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                if 11 in player_card_values:
                    dealer_soft = True
                else:
                    dealer_soft = False
                player_total = sum(player_card_values)
                dealer_total = sum(dealer_card_values)

                while dealer_total < 18 and dealer_soft == True: #continously go through this while loop until dealer has > 17.
                    card = random.choice(list(DECK.keys()))      #if dealer gets soft 17, must take card.
                    card_value = DECK[card]                         
                    dealer_cards.append(card)
                    dealer_total += card_value
                    if dealer_total > 21:                        #if dealer gets higher than 21 while ace is 11, ace now valued at 1
                        dealer_soft = False                      #goes into the next while loop where dealer_soft is False   
                        dealer_total -= 10                       #e.g. Ace and 3, 9 = 11+3+9= 23, 23-10 = 13
                
                while dealer_total < 17 and dealer_soft == False: #13 < 17 & dealer_soft = False
                    card = random.choice(list(DECK.keys()))       #13 + 5 = 18, exit while loop  
                    card_value = DECK[card]
                    dealer_cards.append(card)
                    dealer_total += card_value
            
                dealer_cards.remove('<:backside:1138692953141948476>')

                
                if dealer_total > 21:       #if dealer busts
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** The dealer busts!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*2}")
                    winning = int(bet)*2
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total > dealer_total:   
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** You beat the dealer!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*2}")
                    winning = int(bet)*2
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total == dealer_total:
                    embed_message = discord.Embed(colour=discord.Colour.orange(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n It's a push.")
                    embed_message.set_footer(text=f"{player} pushed: ${int(bet)}")
                    winning = int(bet)
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                else:
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n The **dealer** won this time. Better luck next time.")
                    embed_message.set_footer(text=f"{player} lost: ${int(bet)}")
                    await interaction.response.edit_message(embed=embed_message, view=None)




        async def doubledown_callback(interaction:discord.Interaction):
            if interaction.user.name == player:
                self.economy_system.update_user_balance(guild_id, player, int(bet)) 
                card = random.choice(list(DECK.keys()))
                card_value = DECK[card]
                player_card_values.append(card_value)
                player_cards.append(card)
                player_total = 0
                
                for value in player_card_values:
                    player_total += value
                    
                dealer_total = 0
                for value in dealer_card_values:
                    dealer_total += value
                    
                while dealer_total < 17:
                    card = random.choice(list(DECK.keys()))
                    card_value = DECK[card]
                    dealer_cards.append(card)
                    dealer_total += card_value
                dealer_cards.remove('<:backside:1138692953141948476>')
                
                if player_total >= 22:
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{dealer_cards[0]}{dealer_cards[1]}\nDealer's total: {dealer_total}\n\n **You** busted! Better luck next time.")
                    embed_message.set_footer(text=f"{player}'s bet: ${int(bet)*2}")
                    await interaction.response.edit_message(embed=embed_message, view=None)
                
                if dealer_total > 21:
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** The dealer busts!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*4}")
                    winning = int(bet)*4
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total > dealer_total:
                    embed_message = discord.Embed(colour=discord.Colour.green(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n **Congrats!** You beat the dealer!")
                    embed_message.set_footer(text=f"{player} won: ${int(bet)*4}")
                    winning = int(bet)*4
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                elif player_total == dealer_total:
                    embed_message = discord.Embed(colour=discord.Colour.orange(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n It's a push.")
                    embed_message.set_footer(text=f"{player} pushed: ${int(bet)*2}")
                    winning = int(bet)*2
                    self.economy_system.user_winning(guild_id, player, winning)
                    await interaction.response.edit_message(embed=embed_message, view=None)

                else:
                    embed_message = discord.Embed(colour=discord.Colour.red(), 
                                    title=f"{player}'s Blackjack Game", 
                                    description=f"**Your Hand**\n{''.join(card for card in player_cards)}\nYour total: {player_total}\n\n**Dealer's Hand**\n{''.join(card for card in dealer_cards)}\nDealer's total: {dealer_total}\n\n The **dealer** won this time. Better luck next time.")
                    embed_message.set_footer(text=f"{player} lost: ${int(bet)*2}")
                    await interaction.response.edit_message(embed=embed_message, view=None)



        #async def split_callback(interaction:discord.Interaction):
        yes.callback = yes_callback
        no.callback = no_callback
        hit.callback = hit_callback
        stand.callback = stand_callback
        doubledown.callback = doubledown_callback
        #split.callback = split_callback
        await interaction.response.send_message(embed=embed_message, view=gamebutton)


async def setup(bot):
    await bot.add_cog(GamesCog(bot, economy_system))
