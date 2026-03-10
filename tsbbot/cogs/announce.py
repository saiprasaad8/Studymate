import discord
from discord.ext import commands
from discord import app_commands
from config import ADMIN_ROLE_ID


class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send an announcement to a selected channel")
    async def announce(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):

# Check admin role
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(
                "You are not allowed to use this command.",
                ephemeral=True
            )
            return
#Announcement message
        embed = discord.Embed(
            title="Announcement!",
            description=message,
            color=discord.Color.blue()
        )
#Announcement by
        embed.set_footer(
            text=f"Announcement by {interaction.user.name}",
            icon_url=interaction.user.display_avatar.url
        )
        await channel.send(embed=embed)
#Announcement sent
        await interaction.response.send_message(
            f"Your announcement sent to {channel.mention}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Announce(bot))
    print("Announcement Module Started")