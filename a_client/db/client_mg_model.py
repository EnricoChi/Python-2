from pymongo import MongoClient


class MessageHistory:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.message_history
