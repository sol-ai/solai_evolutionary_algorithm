import pymongo
from copy import deepcopy

HOST = "mongodb://mongodb:27017"
DATABASE_NAME = "solai_characters"
COLLECTION = "dummy_generations"


class Database:

    client = pymongo.MongoClient(HOST)
    db = client[DATABASE_NAME]
    dummy_characters_generations = db[COLLECTION]

    def __init__(self):
        self.dummy_characters_generations.delete_many({})

    def add_dummy_generation(self, generation, generation_number):
        dummy_characters_generations = self.dummy_characters_generations
        generation_entry = {
            'generationNumber': generation_number, 'characters': generation}
        dummy_characters_generations.insert_one(generation_entry)

    def close_connection(self):
        self.client.close()

    def get_generation(self, generation_number):
        return self.dummy_characters_generations.find_one({'generationNumber': generation_number})
