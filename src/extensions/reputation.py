from xmlrpc.client import boolean
import pymongo
import discord
from functions.filters import sinner
from functions.reputation_functions import sumReputation, subtractReputation, ranksReputation
from time import time
from discord import app_commands
from discord.ext import commands
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
    async def remaining_reputation(self, interaction: discord.Interaction):
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



    @REPUTATION_GROUP.command(name="add", description="Add reputation to members")
    @app_commands.checks.has_any_role(getenv("AUCTIONEER"), getenv("TRIAL_AUCTIONEER"))
    @app_commands.describe(member1="first member to give reputation", member2="second member to give reputation", amount="amount of reputation to be given")
    async def add_reputation(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, amount: int):
        if sinner(interaction.user.id):
            return
        
        GUILD = self.bot.get_guild(getenv("GUILD"))
        REPUTATION_CHANNEL = self.bot.get_channel(getenv("REPUTATION_CHANNEL"))

        if interaction.channel.id == REPUTATION_CHANNEL.id:
            DOCUMENT_PERMANENT_1 = REP_PERMA_COLLECTION.find_one({"id": member1.id})
            DOCUMENT_TEMPORAL_1 = REP_TEMP_COLLECTION.find_one({"id": member1.id})
            DOCUMENT_PERMANENT_2 = REP_PERMA_COLLECTION.find_one({"id": member2.id})
            DOCUMENT_TEMPORAL_2 = REP_TEMP_COLLECTION.find_one({"id": member2.id})

            if DOCUMENT_PERMANENT_1 is not None:
                if DOCUMENT_TEMPORAL_1 is not None:
                    sumReputation(member1.id, int(amount))
                else:
                    DOCUMENT_TEMPORAL_1.insert_one({
                        "id": member1.id,
                        "reputation": 0
                    })
                    sumReputation(member1.id, int(amount))
            else:
                DOCUMENT_PERMANENT_1.insert_one({
                    "id": member1.id,
                    "reputation": 0
                })
                DOCUMENT_TEMPORAL_1.insert_one({
                    "id": member1.id,
                    "reputation": 0
                })
                sumReputation(member1.id, int(amount))

            if DOCUMENT_PERMANENT_2 is not None:
                if DOCUMENT_TEMPORAL_2 is not None:
                    sumReputation(member2.id, int(amount))
                else:
                    DOCUMENT_TEMPORAL_2.insert_one({
                        "id": member2.id,
                        "reputation": 0
                    })
                    sumReputation(member2.id, int(amount))
            else:
                DOCUMENT_PERMANENT_2.insert_one({
                    "id": member2.id,
                    "reputation": 0
                })
                DOCUMENT_TEMPORAL_2.insert_one({
                    "id": member2.id,
                    "reputation": 0
                })
                sumReputation(member2.id, int(amount))

            await interaction.response.send_message(f"**{amount}** Rep added to {member1.mention} & {member2.mention}")
        
        ranksReputation(interaction, member1, GUILD)
        ranksReputation(interaction, member2, GUILD)

    @add_reputation.error
    async def add_reputation_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingAnyRole):
            embed = discord.Embed(description="You don't have permissions to run this command.", color=0xd42c54)
            await interaction.response.send_message(embed=embed)


    @REPUTATION_GROUP.command(name="remove", description="Remove reputation to members")
    @app_commands.checks.has_any_role(getenv("AUCTIONEER"), getenv("TRIAL_AUCTIONEER"))
    @app_commands.describe(member="member to remove reputation", amount="amount of reputation to be removed")
    async def remove_reputation(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if sinner(interaction.user.id):
            return

        GUILD = self.bot.get_guild(getenv("GUILD"))
        REPUTATION_CHANNEL = self.bot.get_channel(getenv("REPUTATION_CHANNEL"))

        if interaction.channel.id == REPUTATION_CHANNEL.id:
            DOCUMENT_PERMANENT = REP_PERMA_COLLECTION.find_one({"id": member.id})
            DOCUMENT_TEMPORAL = REP_TEMP_COLLECTION.find_one({"id": member.id})

            if DOCUMENT_PERMANENT is not None:
                if DOCUMENT_TEMPORAL is not None:
                    subtractReputation(member.id, int(amount))
                else:
                    DOCUMENT_TEMPORAL.insert_one({
                        "id": member.id,
                        "reputation": 0
                    })
                    subtractReputation(member.id, int(amount))
            else:
                DOCUMENT_PERMANENT.insert_one({
                    "id": member.id,
                    "reputation": 0
                })
                DOCUMENT_TEMPORAL.insert_one({
                    "id": member.id,
                    "reputation": 0
                })
                subtractReputation(member.id, int(amount))

            await interaction.response.send_message(f"**{amount}** Rep removed from {member.mention}")

    @add_reputation.error
    async def remove_reputation_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingAnyRole):
            embed = discord.Embed(description="You don't have permissions to run this command.", color=0xd42c54)
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Reputation(bot))