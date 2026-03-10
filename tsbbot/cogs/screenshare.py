import discord
from discord.ext import commands
import asyncio
from config import STUDY_VC_ID, ALERT_CHANNEL_ID


class ScreenShare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tasks = {}

# Main Logic

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

# Get alert channel
        alert_channel = member.guild.get_channel(ALERT_CHANNEL_ID)


# When user joins vc
        if before.channel != after.channel and after.channel and after.channel.id == STUDY_VC_ID:

# Cancel previous task if exists
            if member.id in self.active_tasks:
                self.active_tasks[member.id].cancel()

# Start 2-minute timer task
            task = asyncio.create_task(self.screen_timer(member, alert_channel))
            self.active_tasks[member.id] = task
            await alert_channel.send(
                f"{member.mention} 👋 Welcome to the Screen Share VC! Please start screen sharing within **2 minutes**."
            )

# When user leaves vc
        if before.channel and before.channel.id == STUDY_VC_ID:
# Cancel running timer if user leaves early
            if member.id in self.active_tasks:
                self.active_tasks[member.id].cancel()
                del self.active_tasks[member.id]

# Timer
    async def screen_timer(self, member, alert_channel):
        try:
# First 60 seconds hold time
            await asyncio.sleep(60)
# If user left VC, stop
            if not member.voice or member.voice.channel.id != STUDY_VC_ID:
                return
# If user already sharing screen, stop timer
            if member.voice.self_stream:
                return
# 1 minute warning
            await alert_channel.send(
                f"{member.mention} ⏳ 1 minute remaining to start screen sharing."
            )
# 45 seconds hold time
            await asyncio.sleep(45)
            if not member.voice or member.voice.channel.id != STUDY_VC_ID:
                return
# If user started screen share, then stop
            if member.voice.self_stream:
                return
# 15th second warning
            await alert_channel.send(
                f"{member.mention} ⚠️ 15 seconds left to present your screen."
            )
# Final 15 seconds
            await asyncio.sleep(15)
            if member.voice and member.voice.channel.id == STUDY_VC_ID:
# Final check
                if not member.voice.self_stream:
                    await member.move_to(None)
                    await alert_channel.send(
                    f"{member.mention} ❌ Removed for not presenting screen."
                    )
        except asyncio.CancelledError:
            pass
        finally:
            self.active_tasks.pop(member.id, None)


async def setup(bot):
    await bot.add_cog(ScreenShare(bot))
    print("Screen Share Module Started Sucessfully")


# This is the end...