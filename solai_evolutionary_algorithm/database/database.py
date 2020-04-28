import pymongo
from copy import deepcopy

HOST = "mongodb://mongodb:27017"
DATABASE_NAME = "solai_characters"
DUMMY_COLLECTION = "simulations"


class Database:

    def __init__(self):
        self.client = pymongo.MongoClient(HOST)
        self.db = self.client[DATABASE_NAME]
        self.simulations = self.db[DUMMY_COLLECTION]
        self.simulations.delete_many({})

    def add_dummy_generation(self, generation, generation_number):
        characters_generation = self.simulations
        generation_entry = {
            'generationNumber': generation_number, 'characters': generation}
        characters_generation.insert_one(generation_entry)

    def close_connection(self):
        self.client.close()

    def get_generation(self, generation_number):
        return self.simulations.find_one({'generationNumber': generation_number})
