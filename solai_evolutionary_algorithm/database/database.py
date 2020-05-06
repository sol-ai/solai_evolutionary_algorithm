import pymongo
from copy import deepcopy
from datetime import datetime
import os
import uuid
import json
from dataclasses import asdict
from solai_evolutionary_algorithm.evolution.evolver import EvolutionListener
from solai_evolutionary_algorithm.evolution.evolver import EvolverConfig
from typing import Dict


USERNAME = "haraldvinje"
PASSWORD = os.environ["DB_PASSWORD"]
CLUSTER_URL = "mongodb+srv://" + USERNAME + ":" + PASSWORD + \
    "@cluster0-dzimv.mongodb.net/test?retryWrites=true&w=majority"


class Database:

    def __init__(self):
        self.client = pymongo.MongoClient(CLUSTER_URL)
        self.database = self.client.solai
        self.evolution_instances = self.database.evolution_instances

    def init_evolution_instance(self, config):
        self.start_time = datetime.now()
        evolution = {
            "evolutionStart": str(self.start_time), "generations": []}
        self.evolution_instance_id = self.evolution_instances.insert_one(
            evolution).inserted_id
        self.post_config(config)

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

    def post_config(self, config: EvolverConfig) -> None:
        self.evolution_instances.update_one({'_id': self.evolution_instance_id}, {
                                            '$set': {'evolutionConfig': self.__serialize_evolution_config(config)}})

    def __serialize_evolution_config(self, config: EvolverConfig) -> Dict[str, any]:
        config_dict = config.__dict__
        serialized_dict = {}
        for key in config_dict:
            if hasattr(config_dict[key], 'serialize'):
                serialized_dict[key] = config_dict[key].serialize()
            else:
                serialized_dict[key] = config_dict[key]

        del serialized_dict['evolution_listeners']
        return serialized_dict
