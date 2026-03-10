import discord
from discord.ext import commands
from config import INTRO_OUTPUT_CHANNEL_ID
from config import INTRO_PANEL_CHANNEL_ID

# input fields(discord can support only max 5)
class IntroModal(discord.ui.Modal, title="Introduce Yourself"):

    name = discord.ui.TextInput(label="Name / Nickname")
    age = discord.ui.TextInput(label="Age / Pronouns")
    study = discord.ui.TextInput(label="What are you studying / Which year")
    subjects = discord.ui.TextInput(label="Subjects or skills you're focusing on")
    goals = discord.ui.TextInput(label="Your study goals / preferred study times",style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        output_channel = interaction.guild.get_channel(INTRO_OUTPUT_CHANNEL_ID)
# Embed title
        embed = discord.Embed(
            title="📚 New Study Buddy Introduction",
            color=discord.Color.blue()
        )
        embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.display_avatar.url
        )
# displaying user details
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Name/Nickname", value=self.name.value, inline=False)
        embed.add_field(name="Age / Pronouns", value=self.age.value, inline=False)
        embed.add_field(name="Study / Year", value=self.study.value, inline=False)
        embed.add_field(name="Subjects / Skills", value=self.subjects.value, inline=False)
        embed.add_field(name="Study Goals", value=self.goals.value, inline=False)
        await output_channel.send(embed=embed)
# sending ephemeral message 
        await interaction.response.send_message(
            "✅ Your introduction has been posted!",
            ephemeral=True
        )

# UI button
class IntroView(discord.ui.View):
    @discord.ui.button(label="INTRODUCE", style=discord.ButtonStyle.primary, emoji="👋")
    async def introduce(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IntroModal())


class Introduction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
async def setup(bot):
    await bot.add_cog(Introduction(bot))
    print("Introduction Module Started")

# This is the end