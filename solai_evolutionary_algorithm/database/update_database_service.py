
from solai_evolutionary_algorithm.database.database import Database
from solai_evolutionary_algorithm.evolution.evolver_config import EvolverListener


class UpdateDatabaseService(EvolverListener):

    def on_start(self, config):
        self.database = Database()
        self.database.init_evolution_instance(config)

    def on_new_generation(self, evaluated_generation, is_last_generation):
        self.database.add_character_generation(evaluated_generation)

    def on_end(self, fitness_archive, novel_archive):
        self.database.add_fitness_archive(fitness_archive)
        self.database.add_novel_archive(novel_archive)
        self.database.end_evolution_instance()
