import discord
import random

def handle_response(message): 
    p_message = message.lower()

    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == 'help':
        embed = discord.Embed(
            colour=discord.Colour.dark_blue(),
            title="List of Commands",
            description="``roll``   |    Roll a dice!"
        )
        return embed