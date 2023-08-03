import os
import asyncio
import discord
from discord.ext import commands

TOKEN = "MTEzNTY5MzcyODQ5Mzg3OTMyNg.GXS1RH.AE1Y2Dom38JGrmUdEqXFssxLIrv0t6sYDj9xy8"
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# Asynchronous function to load extensions
async def load_cogs():
    try:
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{file[:-3]}")
    except Exception as e:
        print(e)

# Asynchronous initialization hook
@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
