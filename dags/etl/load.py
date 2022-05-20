from core.config import MONGO_URI
from pymongo import MongoClient


def load_to_datalake(best_sellers: list):
    """
    Save best sellers books in datalake.

    First, remove best sellers in datalake with the same week of new best sellers to be save.
    After, save best sellers.

    Parameters:
        best_sellers (list): list of best sellers dictionary
        """

    week = best_sellers[0]['week']

    client = MongoClient(MONGO_URI)
    col = client.bsb_datalake.best_sellers

    col.delete_many({'week': week})
    col.insert_many(best_sellers)


def read_from_datalake():
    """Get best sellers from datalake, without '_id' field."""

    client = MongoClient(MONGO_URI)
    col = client.bsb_datalake.best_sellers

    best_sellers = list(col.find({}, {'_id': 0}))
    return best_sellers


def load_to_datawarehouse(best_sellers: list):
    """
    Save best sellers in data warehouse.

    Best sellers to be save are already with transformed data.

    Parameters:
        best_sellers (list): list of best sellers dictionary, with transformed data
    """

    client = MongoClient(MONGO_URI)
    col = client.bsb_datawarehouse.best_sellers

    col.insert_many(best_sellers)
