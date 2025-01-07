from pymongo import MongoClient


class MongoDBHandler:
    def __init__(self, config):
        self.client = MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]

    def add_new_entry(self, data):
        """Insert a new tracking record."""
        collection = self.db["tracking_data"]
        collection.insert_one(data)
