from solai_evolutionary_algorithm.evolution.evolution_types import EndCriteria


class FixedGenerationsEndCriteria(EndCriteria):
    def __init__(self, generations: int):
        self.generations = generations
        self.curr_generation = 0

    def __call__(self) -> bool:
        self.curr_generation += 1
        return self.curr_generation >= self.generations

    def serialize(self):
        return {'description': f'Ends after {self.generations} generations are produced'}
