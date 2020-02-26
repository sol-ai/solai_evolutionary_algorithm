import pymongo


class Database:

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    col = db["friends"]

    def __init__(self):
        my_friends = [
            {"name": "Tristan"},
            {"name": "Hilmo"},
            {"name": "Gard"},
            {"name": "Håkon"},
            {"name": "Peder"}
        ]

        self.col.delete_many({})
        self.col.insert_many(my_friends)
        for friend in self.col.find():
            print(friend)


Database()
