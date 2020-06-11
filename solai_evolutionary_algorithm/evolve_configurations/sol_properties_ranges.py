character_properties_ranges = {"radius": (28.0, 50.0),
                               "moveVelocity": (200.0, 800.0)}

melee_ability_ranges = {
    "name": "abilityName",
    "type": "MELEE",
    "radius": (16.0, 200.0),
    "distanceFromChar": (0.0, 200.0),
    "speed": (0.0, 0.0),
    "startupTime": (1, 30),
    "activeTime": (1, 60),
    "executionTime": (1, 30),
    "endlagTime": (1, 30),
    "rechargeTime": (10, 30),
    "damage": (100.0, 1000.0),
    "baseKnockback": (10.0, 1000.0),
    "knockbackRatio": (0.1, 1.0),
    "knockbackPoint": (-500.0, 500.0),
    "knockbackTowardPoint": (False, True)
}


projectile_ability_ranges = {
    "name": "abilityName",
    "type": "PROJECTILE",
    "radius": (5, 50),
    "distanceFromChar": (0, 200),
    "speed": (100, 800),
    "startupTime": (1, 60),
    "activeTime": (20, 1000),
    "executionTime": (1, 30),
    "endlagTime": (1, 30),
    "rechargeTime": (10, 120),
    "damage": (15, 500),
    "baseKnockback": (50, 1000),
    "knockbackRatio": (0.1, 1.0),
    "knockbackPoint": (-500, 500),
    "knockbackTowardPoint": (False, True)
}
