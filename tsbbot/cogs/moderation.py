import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.everyone_counter = {}

    @commands.Cog.listener()
    async def on_message(self, message):

# Ignore bot messages
        if message.author.bot:
            return
        user_id = message.author.id

# Detect @everyone or @here
        if message.mention_everyone:
            self.everyone_counter[user_id] = self.everyone_counter.get(user_id, 0) + 1
            if self.everyone_counter[user_id] >= 3: # 3 tags
                try:
                    await message.delete()
                    #  3 Mins timeout to the user. Change how much you want..... Ex. minutes=5
                    await message.author.timeout(discord.utils.utcnow() + timedelta(minutes=3),reason="Repeated @everyone mentions")
                    await message.channel.send(f"{message.author.mention} ⚠️ Please do not spam @everyone.")
                except discord.Forbidden:
                    pass
                self.everyone_counter[user_id] = 0
        else:
            self.everyone_counter[user_id] = 0
        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
    print("Moderation Module Started")


# This is the End...