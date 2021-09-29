from server.logics.network import Socket
from server.logics.map import Tile
from server.logics import game_rules

PLAYER_CHARACTERS = ["A", "B", "C", "D"]
Trap_CHARACTERS = ["a", "b", "c", "d"]


class Agent:
    def __init__(self, agent_id, tile, init_score, trap_count, connection: Socket):
        self.tile = tile
        self.init_score = init_score
        self._id = agent_id
        self._trap_count = trap_count
        self.connection = connection
        self.trap_tiles = []
        self.gems = []
        self.hit_hurts = []
        self.trap_hurts = []
        self.turn_age = 0

    @property
    def id(self):
        return self._id + 1

    @property
    def score(self):
        point = self.init_score
        gem_counts = self.get_gems_count()
        for i, gem_count in enumerate(gem_counts.values()):
            point += gem_count * game_rules.GEM_SCORES[i]
        point += len(self.hit_hurts) * game_rules.HIT_HURT
        point += len(self.trap_hurts) * game_rules.TRAP_HURT
        point += self.turn_age * game_rules.TURN_HURT
        return point

    @property
    def character(self):
        return PLAYER_CHARACTERS[self._id]

    @property
    def trap_character(self):
        return Trap_CHARACTERS[self._id]

    @property
    def trap_count(self):
        return max([0, self._trap_count - len(self.trap_tiles)])

    def add_trap_tile(self, tile):
        self.trap_tiles.append(tile)

    @property
    def name(self):
        return PLAYER_CHARACTERS[self._id]

    def add_gem(self, gem):
        self.gems.append(gem)

    def get_gems_count(self):
        return {
            "gem1": self.gems.count(Tile.TileType.GEM1),
            "gem2": self.gems.count(Tile.TileType.GEM2),
            "gem3": self.gems.count(Tile.TileType.GEM3),
            "gem4": self.gems.count(Tile.TileType.GEM4),
        }
