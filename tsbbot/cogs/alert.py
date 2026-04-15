import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
import os


DATA_FILE = "data/alerts.json"


# json operations

def load_alerts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_alerts(alerts):
    with open(DATA_FILE, "w") as f:
        json.dump(alerts, f, indent=4)



# modal

class AlertModal(discord.ui.Modal, title="Set Alert Time"):

    hour = discord.ui.TextInput(label="Hour (1-12)")
    minute = discord.ui.TextInput(label="Minute (0-59)")
    second = discord.ui.TextInput(label="Second (0-59)")
    ampm = discord.ui.TextInput(label="AM / PM")

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):

        self.cog.temp_data[interaction.user.id] = {
            "hour": self.hour.value.zfill(2),
            "min": self.minute.value.zfill(2),
            "sec": self.second.value.zfill(2),
            "ampm": self.ampm.value.upper()
        }

        await interaction.response.send_message(
            "Select days:",
            view=DayView(self.cog),
            ephemeral=True
        )


# dropdown code

class DaySelect(discord.ui.Select):
    def __init__(self, cog):
        self.cog = cog

        options = [
            discord.SelectOption(label=d) for d in [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday", "Daily"
            ]
        ]

        super().__init__(
            placeholder="Select days",
            min_values=1,
            max_values=7,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        selected_days = self.values

        if "Daily" in selected_days:
            selected_days = ["Daily"]

        data = self.cog.temp_data.get(interaction.user.id)

        if not data:
            await interaction.response.send_message("Error", ephemeral=True)
            return

        new_alert = {
            "user_id": interaction.user.id,
            "hour": data["hour"],
            "min": data["min"],
            "sec": data["sec"],
            "ampm": data["ampm"],
            "days": selected_days
        }

        self.cog.alerts.append(new_alert)
        save_alerts(self.cog.alerts)

        await interaction.response.send_message(
            f"Alert set for {data['hour']}:{data['min']} {data['ampm']} ({', '.join(selected_days)})",
            ephemeral=True
        )


class DayView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=60)
        self.add_item(DaySelect(cog))


# panel code

class AlertView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Set Alert", style=discord.ButtonStyle.primary)
    async def set_alert(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AlertModal(self.cog))

    @discord.ui.button(label="View Alert", style=discord.ButtonStyle.secondary)
    async def view_alert(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_alerts = [a for a in self.cog.alerts if a["user_id"] == interaction.user.id]

        if not user_alerts:
            await interaction.response.send_message("No alerts found.", ephemeral=True)
            return

        msg = " Your Alerts:\n\n"
        for a in user_alerts:
            msg += f"{a['hour']}:{a['min']} {a['ampm']} → {', '.join(a['days'])}\n"

        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.button(label="Delete Alert", style=discord.ButtonStyle.danger)
    async def delete_alert(self, interaction: discord.Interaction, button: discord.ui.Button):

        before = len(self.cog.alerts)

        self.cog.alerts = [
            a for a in self.cog.alerts if a["user_id"] != interaction.user.id
        ]

        save_alerts(self.cog.alerts)

        if before == len(self.cog.alerts):
            await interaction.response.send_message("No alerts to delete.", ephemeral=True)
        else:
            await interaction.response.send_message("Alerts deleted.", ephemeral=True)


# main program

class Alert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alerts = load_alerts()
        self.temp_data = {}
        self.triggered = set()
        self.check_alerts.start()

    @tasks.loop(seconds=5)
    async def check_alerts(self):

        now = datetime.now()

        current_hour = now.strftime("%I")
        current_min = now.strftime("%M")
        current_ampm = now.strftime("%p")
        current_day = now.strftime("%A")

        for alert in self.alerts:

            if (
                alert["hour"] == current_hour and
                alert["min"] == current_min and
                alert["ampm"] == current_ampm and
                (current_day in alert["days"] or "Daily" in alert["days"])
            ):

                key = f"{alert['user_id']}_{current_hour}_{current_min}"

                if key not in self.triggered:
                    self.triggered.add(key)

                    try:
                        user = await self.bot.fetch_user(alert["user_id"])
                        await user.send("⏰ Study Reminder! Time to focus!")
                        
                    except Exception as e:
                        print("DM failed:", e)

    @commands.Cog.listener()
    async def on_ready(self):

        from config import ALERT_PANEL_CHANNEL_ID

        channel = await self.bot.fetch_channel(ALERT_PANEL_CHANNEL_ID)

        # delete old panels
        async for msg in channel.history(limit=20):
            if msg.author == self.bot.user:
                try:
                    await msg.delete()
                except:
                    pass

        embed = discord.Embed(
            title="Study Alert System",
            description="Set your reminders easily.",
            color=discord.Color.blue()
        )

        await channel.send(embed=embed, view=AlertView(self))


async def setup(bot):
    await bot.add_cog(Alert(bot))
    print("Alert Module Started")
