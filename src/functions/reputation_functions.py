import pymongo
from os import getenv
from dotenv import load_dotenv


load_dotenv("configuration.env")
DB = pymongo.MongoClient(getenv("DATABASE"))
REP_CONFIG_COLLECTION = DB.coclan.reputation.config
REP_PERMA_COLLECTION = DB.coclan.reputation.permanent
REP_TEMP_COLLECTION = DB.coclan.reputation.temporal


def sumReputation(userId, amount):
    DOCUMENT_CONFIGURATION = REP_CONFIG_COLLECTION.find_one({})
    DOCUMENT_PERMANENT = REP_PERMA_COLLECTION.find_one({"id": userId})
    DOCUMENT_TEMPORAL = REP_TEMP_COLLECTION.find_one({"id": userId})
    SUM_REPUTATION = 1

    permanentReputation = DOCUMENT_PERMANENT["reputation"]
    temporalReputation = DOCUMENT_TEMPORAL["reputation"]

    for i in range(int(amount)):
        if DOCUMENT_CONFIGURATION["toggle_limit"] == True:
            if DOCUMENT_TEMPORAL["reputation"] < DOCUMENT_CONFIGURATION["maximum_reputation"]:
                permanentReputation += SUM_REPUTATION
                temporalReputation += SUM_REPUTATION
            else:
                break
        else:
            permanentReputation += SUM_REPUTATION
            temporalReputation += SUM_REPUTATION
    REP_PERMA_COLLECTION.update_one({}, {"$set": {"reputation": permanentReputation}})
    REP_TEMP_COLLECTION.update_one({}, {"set": {"reputation": temporalReputation}})


def subtractReputation(userId, amount):
    DOCUMENT_CONFIGURATION = REP_CONFIG_COLLECTION.find_one({})
    DOCUMENT_PERMANENT = REP_PERMA_COLLECTION.find_one({"id": userId})
    DOCUMENT_TEMPORAL = REP_TEMP_COLLECTION.find_one({"id": userId})
    SUM_REPUTATION = 1

    permanentReputation = DOCUMENT_PERMANENT["reputation"]
    temporalReputation = DOCUMENT_TEMPORAL["reputation"]

    for i in range(int(amount)):
        if DOCUMENT_CONFIGURATION["toggle_limit"] == True:
            if permanentReputation > 0:
                permanentReputation -= SUM_REPUTATION
            if temporalReputation > 0:
                temporalReputation -= SUM_REPUTATION
    REP_PERMA_COLLECTION.update_one({}, {"$set": {"reputation": permanentReputation}})
    REP_TEMP_COLLECTION.update_one({}, {"set": {"reputation": temporalReputation}})


async def ranksReputation(interaction, user, guild):
    DOCUMENT_PERMANENT = REP_PERMA_COLLECTION.find_one({"id": user.id})

    if DOCUMENT_PERMANENT["reputation"] >= 300:
        RANK = guild.get_role(getenv("CAPTAIN"))
        if RANK not in user.roles:
            await user.add_roles(RANK)
            await interaction.channel.send(f"{user.mention}, Congrats for reaching **{RANK}**! you can now use <#{getenv('CAPTAIN_CHANNEL')}> for auctions!")
            
    elif DOCUMENT_PERMANENT["reputation"] >= 150:
        RANK = guild.get_role(getenv("SERGEANT"))
        if RANK not in user.roles:
            await user.add_roles(RANK)
            await interaction.channel.send(f"{user.mention}, Congrats for reaching **{RANK}**! you can now use <#{getenv('SERGEANT_CHANNEL')}> for auctions!")
    elif DOCUMENT_PERMANENT["reputation"] >= 75:
        RANK = guild.get_role(getenv("CORPORAL"))
        if RANK not in user.roles:
            await user.add_roles(RANK)
            await interaction.channel.send(f"{user.mention}, Congrats for reaching **{RANK}**! you can now use <#{getenv('CORPORAL_CHANNEL')}> for auctions!")