import redis
import json


class CharacterQueue:

    def __init__(self):
        self.r = redis.StrictRedis(host='redis', port=6379, db=0)

    def push_character(self, character):
        rval = json.dumps(character)
        self.r.set('key1', rval)

    def push_characters(self, characters):
        for character in characters:
            self.push_character(character)

    def get_character(self):
        print(self.r.get('key1'))
