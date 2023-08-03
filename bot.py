import discord
from discord import app_commands
from discord.ext import commands
import responses
TOKEN = "MTEzNTY5MzcyODQ5Mzg3OTMyNg.GXS1RH.AE1Y2Dom38JGrmUdEqXFssxLIrv0t6sYDj9xy8"
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print('f{username} said: "{user_message}" ({channel})')
        
    if user_message[0] == "?":
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private=False)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!.")

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


bot.run(TOKEN)