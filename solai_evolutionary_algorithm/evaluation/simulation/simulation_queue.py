from time import time
from typing import Tuple, Any, List, TypedDict, Dict, Optional, Union

import redis
import uuid
import sys
import json
import threading
from copy import deepcopy

SIMULATION_DATA_QUEUE = "queue:simulation-data"
SIMULATION_RESULT_QUEUE = 'queue:simulation-result'

AbilityConfig = TypedDict("AbilityConfig", {
    "name": str,
    "type": str,  # "MELEE" | "PROJECTILE"
    "radius": float,
    "distanceFromChar": float,
    "speed": float,
    "startupTime": int,
    "activeTime": int,
    "executionTime": int,
    "endlagTime": int,
    "rechargeTime": int,
    "damage": float,
    "baseKnockback": float,
    "knockbackRatio": float,
    "knockbackPoint": float,
    "knockbackTowardPoint": bool
})

CharacterConfig = TypedDict('CharacterConfig', {
    'characterId': str,
    'radius': float,
    'moveVelocity': float,
    'abilities': List[AbilityConfig]
})

SimulationData = TypedDict("SimulationData", {
    "simulationId": str,
    "charactersConfigs": List[CharacterConfig],
    "metrics": List[str]
})
SimulationResult = TypedDict("SimulationResult", {
    "simulationId": str,
    "simulationData": SimulationData,
    "metrics": Dict[str, List[float]]
})

class SimulationQueue:

    def __init__(self, host='redis', port=6379):
        print(f"Connecting to redis simulation queue at host: {host} port: {port}")
        self.redis = redis.StrictRedis(host=host, port=port, db=0)

    def push_simulation_data(self, simulation_data: SimulationData) -> None:
        serialized_simulation_data = json.dumps(simulation_data)
        self.redis.lpush(SIMULATION_DATA_QUEUE, serialized_simulation_data)

    def get_simulation_result(self, block=True) -> Optional[SimulationResult]:
        if block:
            result = self.redis.blpop(SIMULATION_RESULT_QUEUE)
        else:
            result = self.redis.lpop(SIMULATION_RESULT_QUEUE)
        result = json.loads(result[1].decode("utf-8"))
        return result

    def push_simulations_data_wait_results(self, simulations_data: List[SimulationData]) -> List[SimulationResult]:
        """
        Pushes simulations and waits for an equal amount of results to be present
        """
        for simulation_data in simulations_data:
            self.push_simulation_data(simulation_data)

        pushed_simulations_count = len(simulations_data)
        current_results = []
        start_time = time()
        prev_time = start_time
        while len(current_results) < pushed_simulations_count:
            simulation_result = self.get_simulation_result()
            current_results.append(simulation_result)

            new_time = time()
            if new_time-prev_time > 20:
                print(f"waited for simulation results for {new_time - start_time:.2f}s, "
                      f"got {len(current_results)} of {pushed_simulations_count}")
                prev_time = new_time
        print(f"Simulated {pushed_simulations_count} simulations in {time() - start_time:.2f}s")

        # copied_current_results = deepcopy(current_results)
        return current_results

    def get_simulation_data(self):
        return self.redis.lpop(SIMULATION_DATA_QUEUE)

    def create_simulation_id(self):
        return str(uuid.uuid4())

    def push_population(self, population):
        self.redis.lpush("queue:population", json.dumps(population))

    def get_population(self):
        result = self.redis.blpop("queue:population")
        result = json.loads(result[1].decode("utf-8"))
        return result
