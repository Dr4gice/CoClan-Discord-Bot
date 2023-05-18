import sys, os
from xmlrpc.client import boolean
sys.dont_write_bytecode = True
import pymongo
import operator
import random
import colorama, cursor, ctypes
import discord, asyncio
from functions.filters import sinner
from datetime import datetime, timedelta
from time import gmtime, strftime, strptime, time
from millify import millify
from logging import exception
from discord import app_commands
from discord.ext import commands, tasks
from colorama.initialise import init
from colorama import init, Fore, Back, Style, Cursor
from os import getenv
from dotenv import load_dotenv


load_dotenv("configuration.env")
DB = pymongo.MongoClient(getenv("DATABASE"))
REP_CONFIG_COLLECTION = DB.coclan.reputation.config
REP_PERMA_COLLECTION = DB.coclan.reputation.permanent
REP_TEMP_COLLECTION = DB.coclan.reputation.temporal



class Reputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.timer()


    async def timer(self):
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            TIMESTAMP = int(time())
            DOCUMENT = REP_CONFIG_COLLECTION.find_one({}, {"time_limit": 1})
            if TIMESTAMP >= DOCUMENT["time_limit"]:
                DAY_IN_SECONDS = 86400
                REP_CONFIG_COLLECTION.update_one({}, {"$set": {"time_limit": int(TIMESTAMP + DAY_IN_SECONDS)}})
                REP_TEMP_COLLECTION.drop()
                DB.coclan.create_collection("reputation.temporal")


    REPUTATION_GROUP = app_commands.Group(name="reputation", description="View your reputation")


    @REPUTATION_GROUP.command(name="view", description="View your reputation")
    async def view_reputation(self, interaction: discord.Interaction):
        if sinner(interaction.user.id):
            return
        
        DOCUMENT = REP_PERMA_COLLECTION.find_one({"id": interaction.user.id})
        MESSAGE = await interaction.response.send_message(f"{interaction.user.name} **{ACTUAL_REPUTATION}** Reputation")

        if DOCUMENT is not None:
            ACTUAL_REPUTATION = DOCUMENT["reputation"]
            MESSAGE
        else:
            ACTUAL_REPUTATION = 0
            MESSAGE


    @REPUTATION_GROUP.command(name="remaining", description="View your daily reputation limit left")
    async def repremaining(self, interaction: discord.Interaction):
        if sinner(interaction.user.id):
            return
        
        DOCUMENT_CONFIGURATION = REP_CONFIG_COLLECTION.find_one({})
        DOCUMENT = REP_TEMP_COLLECTION.find_one({"id": interaction.user.id})
        MAXIMUM_REPUTATION = DOCUMENT_CONFIGURATION["maximum_reputation"]
        MESSAGE = await interaction.response.send_message(f"{interaction.user.mention}, You are **{MAXIMUM_REPUTATION - DAILY_REPUTATION}** rep short of your daily limit")

        if DOCUMENT_CONFIGURATION["toggle_limit"] == True:
            if DOCUMENT is not None:
                DAILY_REPUTATION = DOCUMENT["reputation"]
                MESSAGE
            else:
                DAILY_REPUTATION = 0
                MESSAGE
        else:
            await interaction.response.send_message("the daily rep limit is disabled")







async def setup(bot):
    await bot.add_cog(Reputation(bot))