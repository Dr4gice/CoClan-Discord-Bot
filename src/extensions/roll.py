import random
import discord
from functions.filters import sinner
from discord import app_commands
from discord.ext import commands


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a random number")
    @app_commands.guilds(886214918624407642)
    @app_commands.describe(num1="first number", num2="last number")
    async def roll(self, interaction: discord.Interaction, num1: int = None, num2: int = None):
        if sinner(interaction.user.id):
            return

        if num1 is not None and num2 is not None:
            NUMBER = random.randint(int(num1), int(num2))
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{NUMBER}** ({num1}-{num2})")
        elif num1 is not None or num2 is not None:
            NUMBER = random.randint(1, int(num1) if num1 is not None else int(num2))
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{NUMBER}** ({1}-{num1 if num1 is not None else num2})")
        else:
            NUMBER = random.randint(1,100)
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{NUMBER}** ({1}-{100})")
    

    @app_commands.command(name="coinflip", description="Flip a coin")
    @app_commands.guilds(886214918624407642)
    async def coinflip(self, interaction: discord.Interaction):
        if sinner(interaction.user.id):
            return

        RESULT = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(RESULT)


    @app_commands.command(name="pick", description="Picks one of the given options")
    @app_commands.guilds(886214918624407642)
    @app_commands.describe(option1="first option", option2="second option", option3="third option", option4="fourth option", option5="fifth option")
    async def pick(self, interaction: discord.Interaction, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
        if sinner(interaction.user.id):
            return

        OPTIONS = [option1, option2, option3, option4, option5]
        NUMBER_OPTIONS = sum(option is not None for option in OPTIONS)

        if NUMBER_OPTIONS > 0:
            NUMBER = random.randint(1, NUMBER_OPTIONS)
            selectedOption = OPTIONS[NUMBER - 1]
            await interaction.response.send_message(selectedOption)


async def setup(bot):
    await bot.add_cog(Casino(bot))