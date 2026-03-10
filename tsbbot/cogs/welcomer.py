import discord
from discord.ext import commands
from config import WELCOME_CHANNEL_ID

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        embed = discord.Embed(
            title="Welcome to the Server!",
            description=f"Hello {member.mention}, welcome to **{member.guild.name}**!",
            color=discord.Color.blue()           
        )
# USER PROFILE IMAGE
        embed.set_thumbnail(url=member.display_avatar.url)
# SERVER ICON
        if member.guild.icon:
            embed.set_author(
                name=member.guild.name,
                icon_url=member.guild.icon.url
            )
        embed.add_field(
            name="Get Started",
            value="• Read the rules\n• Introduce yourself\n• Join Study VC\n• Make Your Journal\n• Start Studying",
            inline=False
        )
        embed.set_footer(text=f"Member Count: {member.guild.member_count}")
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcomer(bot))
    print("Welcomer Module Started Sucessfully")


# This is the end