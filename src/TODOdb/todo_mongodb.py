from pymongo import MongoClient

uri: str = "mongodb://localhost:27017/"
client: MongoClient = MongoClient(uri)
