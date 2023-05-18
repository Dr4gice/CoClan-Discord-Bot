import random
import discord
from filters import sinner
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
            number = random.randint(int(num1), int(num2))
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{number}** ({num1}-{num2})")
        elif num1 is not None or num2 is not None:
            number = random.randint(1, int(num1) if num1 is not None else int(num2))
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{number}** ({1}-{num1 if num1 is not None else num2})")
        else:
            number = random.randint(1,100)
            await interaction.response.send_message(f"**{interaction.user.name}** rolled **{number}** ({1}-{100})")
    

    @app_commands.command(name="coinflip", description="Flip a coin")
    @app_commands.guilds(886214918624407642)
    async def coinflip(self, interaction: discord.Interaction):
        if sinner(interaction.user.id):
            return

        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(result)


    @app_commands.command(name="pick", description="Picks one of the given options")
    @app_commands.guilds(886214918624407642)
    @app_commands.describe(option1="first option", option2="second option", option3="third option", option4="fourth option", option5="fifth option")
    async def pick(self, interaction: discord.Interaction, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
        if sinner(interaction.user.id):
            return

        options = [option1, option2, option3, option4, option5]
        numOptions = sum(option is not None for option in options)

        if numOptions > 0:
            number = random.randint(1, numOptions)
            selectedOption = options[number - 1]
            await interaction.response.send_message(selectedOption)


async def setup(bot):
    await bot.add_cog(Casino(bot))