from pymongo import MongoClient

uri = "mongodb+srv://nsql:nsql@cluster0.hopgxl2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('NSQL')
