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

    def init_evolution_instance(self):
        self.start_time = datetime.now()
        evolution = {
            "evolutionStart": str(self.start_time), "generations": []}
        self.evolution_instance_id = self.evolution_instances.insert_one(
            evolution).inserted_id

    def add_character_generation(self, generation):
        self.evolution_instances.update_one({'_id': self.evolution_instance_id}, {
            '$push': {'generations': generation}
        })

    def end_evolution_instance(self):
        finish_time = datetime.now()
        total_time_taken = str(finish_time - self.start_time)
        self.evolution_instances.update_one({'_id': self.evolution_instance_id}, {'$set':
                                                                                  {'totalTimeTaken': total_time_taken}})
        self.client.close()
