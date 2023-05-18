import os
import pymongo
from dotenv import load_dotenv

load_dotenv("configuration.env")

# Database
mydb = pymongo.MongoClient(os.getenv("DATABASE"))
db = mydb.coclan
sinners = db.filter

def sinner(userId: int):
    """Check if the user id is in the blacklist on the database
    Args:
        userId (int): User id
    Returns:
        bool: True if user id is in the blacklist, False if doesn't
    """
    filterDocument = sinners.find_one({"listas": {"$exists": True}})
    if userId in filterDocument.get("listas", []):
        return True
    else:
        return False