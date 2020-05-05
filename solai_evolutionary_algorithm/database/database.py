import pymongo
from copy import deepcopy
from datetime import datetime
import os
import uuid


USERNAME = "haraldvinje"
PASSWORD = os.environ["DB_PASSWORD"]
CLUSTER_URL = "mongodb+srv://" + USERNAME + ":" + PASSWORD + \
    "@cluster0-dzimv.mongodb.net/test?retryWrites=true&w=majority"


class Database:

    def __init__(self):
        self.client = pymongo.MongoClient(CLUSTER_URL)
        self.collection = self.client.solai
        self.evolution_instances = self.collection.evolution_instances

    def create_evolution_instance(self):
        current_time = str(datetime.now())
        evolution = {"evolutionStart": current_time, "generations": []}
        self.evolution_instance_id = self.evolution_instances.insert_one(
            evolution).inserted_id

    def add_character_generation(self, generation):
        self.evolution_instances.update_one({'_id': self.evolution_instance_id}, {
            '$push': {'generations': generation}
        })

    def close_connection(self):
        self.client.close()
