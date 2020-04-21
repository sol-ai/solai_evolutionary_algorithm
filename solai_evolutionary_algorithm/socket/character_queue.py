import redis
import uuid
import sys
import json

SIMULATION_DATA_QUEUE = "queue:simulation-data"
SIMULATION_RESULT_QUEUE = 'queue:simulation-result'


class CharacterQueue:

    def __init__(self, host='redis', port=6370):
        self.redis = redis.StrictRedis(host=host, port=port, db=0)

    def push_character(self, character):
        character_json = json.dumps(character)
        self.redis.lpush('characters', character_json)

    def push_characters(self, characters):
        characters_strings = map(json.dumps, characters)
        self.redis.lpush('characters', *characters_strings)

    def pop_character(self):
        return self.redis.lpop('characters')

    def push_character_pair(self, character1, character2):
        self.push_simulation_data([character1, character2])

    def push_simulation_data(self, character_configs):
        # TODO: Specify metrics somewhere else
        simulation_id = str(uuid.uuid1())
        metrics = ["gameLength"]
        simulation_data = {'simulationId': simulation_id,
                           'charactersConfigs': character_configs, 'metrics': metrics}
        simulation_data_string = str(simulation_data)
        self.redis.lpush(SIMULATION_DATA_QUEUE, simulation_data_string)

    def get_simulation_data(self):
        return self.redis.lpop(SIMULATION_RESULT_QUEUE)
