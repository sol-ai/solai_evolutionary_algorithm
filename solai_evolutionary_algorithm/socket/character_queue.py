import redis
import uuid
import sys
import json
import threading
from copy import deepcopy

SIMULATION_DATA_QUEUE = "queue:simulation-data"
SIMULATION_RESULT_QUEUE = 'queue:simulation-result'


class SimulationQueue:

    current_generation_simulation_results = {}

    def __init__(self, host='redis', port=6370, population_size=10):
        self.population_size = population_size
        self.redis = redis.StrictRedis(host=host, port=port, db=0)

    def push_character_pair(self, character1, character2):
        self.push_simulation_data([character1, character2])

    def push_simulation_data(self, character_configs):
        # TODO: Specify metrics somewhere else
        simulation_data = self.__generate_simulation_data(character_configs)
        self.redis.lpush(SIMULATION_DATA_QUEUE, simulation_data)

    def get_simulation_result(self, block=True):
        if block:
            result = self.redis.blpop(SIMULATION_RESULT_QUEUE)
        else:
            result = self.redis.lpop(SIMULATION_RESULT_QUEUE)
        result = json.loads(result[1].decode("utf-8"))
        return result

    def get_simulation_results(self):
        while len(self.current_generation_simulation_results) < self.population_size:
            simulation_result = self.get_simulation_result()
            simulation_id = simulation_result["simulationId"]
            self.current_generation_simulation_results[simulation_id] = simulation_result

        current_generation_simulation_results = deepcopy(
            self.current_generation_simulation_results)
        self.current_generation_simulation_results = dict()
        return current_generation_simulation_results

    def get_simulation_data(self):
        return self.redis.lpop(SIMULATION_DATA_QUEUE)

    def __generate_simulation_data(self, character_configs):
        # TODO: Specify metrics somewhere else
        simulation_id = str(uuid.uuid1())
        metrics = ["gameLength", "nearDeathFrames"]
        simulation_data = json.dumps({"simulationId": simulation_id,
                                      "charactersConfigs": character_configs, "metrics": metrics})
        return simulation_data
