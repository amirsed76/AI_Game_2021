GEM_SCORES = [10, 25, 35, 75]

CONSTRAINTS = {
    "min_score_for_get_gem_1": -100000,
    "min_score_for_get_gem_2": 15,
    "min_score_for_get_gem_3": 50,
    "min_score_for_get_gem_4": 140,

    "max_eating_gem_1": 15,
    "max_eating_gem_2": 8,
    "max_eating_gem_3": 5,
    "max_eating_gem_4": 4,

}

TRAP_CONSTRAINT_SCORE = [35 * i for i in range(1, 21)]  # max traps == 10
# GAME_OVER_SCORE = -1

HIT_HURT = -20
TRAP_HURT = -40
TURN_HURT = -1