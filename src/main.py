import os
import time
import cursor
import discord, asyncio
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style
from os import getenv
from dotenv import load_dotenv

load_dotenv("configuration.env")
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=getenv("PREFIX"), intents=intents)
tree = bot.tree
exnm = "cogs."
extensions = []

async def main():
    if __name__ == "__main__":
        for extn in extensions:
            try:
                await bot.load_extension(exnm + extn)
            except Exception as e:
                print(Fore.RED + Style.BRIGHT + f"  COGS-ERROR | {extn} | {e}" + Style.RESET_ALL)
                time.sleep(60)
asyncio.run(main())


TITL1 = r"""   ______  ______  ______  __      ______  __   __    """
TITL2 = r"""  /\  ___\/\  __ \/\  ___\/\ \    /\  __ \/\ "-.\ \   """
TITL3 = r"""  \ \ \___\ \ \/\ \ \ \___\ \ \___\ \  __ \ \ \-.  \  """
TITL4 = r"""   \ \_____\ \_____\ \_____\ \_____\ \_\ \_\ \_\\"\_\ """
TITL5 = r"""    \/_____/\/_____/\/_____/\/_____/\/_/\/_/\/_/ \/_/ """

def clear():
    if os.name in ("nt", "dos"):
        cursor.hide()
        os.system("cls")
    elif os.name in ("linux", "osx", "posix"): os.system("clear")
    else: print("\n") * 100

def project():
    PROJECT_ON = Style.RESET_ALL + "\n" + Fore.BLUE + Style.BRIGHT + TITL1 + "\n" + Fore.BLUE + Style.BRIGHT + TITL2 + "\n" + Fore.BLUE + Style.BRIGHT + TITL3 + "\n" + Fore.BLUE + Style.BRIGHT + TITL4 + "\n" + Fore.BLUE + Style.BRIGHT + TITL5 + Style.RESET_ALL + "\n"
    print(PROJECT_ON)

@bot.event 
async def on_ready():
    clear()
    project()


@bot.command(name="sync")
@commands.is_owner()
async def syncTree(ctx):
    await tree.sync()
    ctx.send("Done!")

@tree.command(name="reload")
@app_commands.checks.has_any_role(948702864233074688)
async def reload_cmd(interaction: discord.Interaction, extension: str):
    await bot.reload_extension(exnm + extension)
    await interaction.response.send_message(f":repeat: Reloaded extension **{extension}.py**")

bot.run(getenv("TOKEN"), reconnect=True)