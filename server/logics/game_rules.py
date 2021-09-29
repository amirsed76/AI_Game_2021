GEM_SCORES = [1, 5, 8, 12]

CONSTRAINTS = {
    "min_score_for_get_gem_1": 0,
    "min_score_for_get_gem_2": 5,
    "min_score_for_get_gem_3": 20,
    "min_score_for_get_gem_4": 30,

    "max_eating_gem_1": 20,
    "max_eating_gem_2": 10,
    "max_eating_gem_3": 8,
    "max_eating_gem_4": 5,

}

TRAP_CONSTRAINT_SCORE = [5 * i for i in range(1, 21)]  # max traps == 10
GAME_OVER_SCORE = -1

HIT_HURT = -2
TRAP_HURT = -2
TURN_HURT = -1