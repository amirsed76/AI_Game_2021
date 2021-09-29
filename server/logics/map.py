from enum import Enum
import numpy as np


class Tile:
    class TileType(Enum):
        WALL = 'W'
        EMPTY = 'E'
        TELEPORT = 'T'
        GEM1 = '1'
        GEM2 = '2'
        GEM3 = '3'
        GEM4 = '4'

    def __init__(self, x, y, tile_type=TileType.EMPTY):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.teleports = []

    @property
    def address(self):
        return self.y, self.x

    def __repr__(self):
        return self.tile_type.value

    def is_teleport(self):
        return self.tile_type == self.TileType.TELEPORT

    def get_gem(self):
        if self.tile_type in [self.TileType.GEM1, self.TileType.GEM2, self.TileType.GEM3, self.TileType.GEM4]:
            return self.tile_type

        else:
            return None

    def is_wall(self):
        return self.tile_type == self.TileType.WALL

    def is_empty(self):
        return self.tile_type == self.TileType.EMPTY


class Map:
    def __init__(self, map_content):

        map_tiles = []
        teleports = []
        for y, row in enumerate(map_content):
            row_tiles = []
            for x, item in enumerate(row):
                tile = Tile(x=x, y=y, tile_type=Tile.TileType(item))
                row_tiles.append(tile)
                if tile.tile_type == Tile.TileType.TELEPORT:
                    teleports.append(tile)
            map_tiles.append(row_tiles)

        self.tiles = np.array(map_tiles)
        self.height, self.width = self.tiles.shape
        self._teleports = teleports

    def __repr__(self):
        return str(self.tiles)

    def get_tile(self, y, x):
        if y not in range(self.height) or x not in range(self.width):
            return None
        return self.tiles[y][x]

    def get_show(self):
        height, width = self.tiles.shape

        return np.array([[self.tiles[y][x].tile_type.value for x in range(width)] for y in range(height)])

    def get_teleports(self):
        return self._teleports

