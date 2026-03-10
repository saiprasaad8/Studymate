import discord
from discord.ext import commands
import asyncio
from cogs.introduction import IntroView
from config import INTRO_PANEL_CHANNEL_ID

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

#loading all modules
async def load_cogs():
    await bot.load_extension("cogs.screenshare")
    await bot.load_extension("cogs.welcomer")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.introduction")
    await bot.load_extension("cogs.announce")

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print("\n")
    print(f"Synced {len(synced)} command(s)")
    channel = await bot.fetch_channel(INTRO_PANEL_CHANNEL_ID)
    async for msg in channel.history(limit=5):
        if msg.author == bot.user:
            try:
                await msg.delete()
            except:
                pass
    print("\nBot Started Successfully and Ready to Use")
    embed = discord.Embed(
        title="👋 Introduce Yourself",
        description="Click the button below and introduce yourself to the study community!",
        color=discord.Color.green()
    )
    view = IntroView()
    await channel.send(embed=embed, view=view)

async def main():
    async with bot:
        print("\n")
        await load_cogs()
        await bot.start("bot token")

asyncio.run(main())



# This is the end.....