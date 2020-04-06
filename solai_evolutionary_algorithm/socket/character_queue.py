import redis
import json


class CharacterQueue:

    def __init__(self):
        self.r = redis.StrictRedis(host='redis', port=6379, db=0)

    def push_character(self, character):
        character_json = json.dumps(character)
        self.r.lpush('characters', character_json)

    def push_characters(self, characters):
        for character in characters:
            self.push_character(character)

    def pop_character(self):
        return self.r.lpop('characters')
