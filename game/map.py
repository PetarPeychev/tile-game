import pygame
import automatagen
import random
from tile_types import *

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate(self):
        # instantiate TerrainGenerator with default settings
        terrgen = automatagen.TerrainGenerator()
        # generate a random terrain half the size of the map
        boolarr = terrgen.generate(int(self.width / 2), int(self.height / 2))
        # store the seed for later use
        self.seed = terrgen.seed
        # create the empty map
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]
        # copy the random terrain into the map, doubling the size of each tile
        for y in range(0, self.height):
            for x in range(0, self.width):
                if boolarr[int(y / 2)][int(x / 2)]:
                    self.array[y][x] = 1
                else:
                    self.array[y][x] = 0

        # create a temp array to prevent interference with the smoothing algorithm
        temp_array = self.array
        # iterate over the temp array, counting the walls in each 3x3 section
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if temp_array[y][x] == 0:
                    count = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            nb_x = x + i
                            nb_y = y + j
                            if temp_array[nb_y][nb_x] == 1:
                                count += 1
                    # if the walls in a 3x3 are more than 5,
                    # randomly fill the center tile to smooth out map:
                    # @ @ @      @ @ @
                    # @      ->  @ @
                    # @          @
                    if count >= 5 and random.random() > 0.2:
                        self.array[y][x] = 1

        # store a cave counter, starting at 2 ** 16
        self.cave_count = 65536
        self.cave_dict = {}
        # perform floodfill over the map, incrementing the cave counter and
        # using the current count as a tile replacement
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.floodfill(x, y, 0)

        # put cave ids with less than 64 size in tiny, less than 128 in small
        tiny_caves = list(filter(lambda x: self.cave_dict[x] < 64, self.cave_dict.keys()))
        small_caves = list(filter(lambda x: self.cave_dict[x] < 128, self.cave_dict.keys()))

        # iterate over map
        for y in range(0, self.height):
            for x in range(0, self.width):
                type = self.array[y][x]
                # if cave is tiny, fill it with liquid, dependent on y-level
                if type in tiny_caves:
                    liquid = WATER
                    if y > 64 and y < 196:
                        liquid = random.choice(LIQUIDS)
                    elif y > 196:
                        liquid = LAVA
                    self.floodfill(x, y, type, replacement_type = liquid)
                    del self.cave_dict[type]
                # if cave is small, fill with random secondary tile
                elif type in small_caves:
                    self.floodfill(x, y, type, replacement_type = random.choice(SECONDARY_TILES))
                    del self.cave_dict[type]

    def floodfill(self, node_x, node_y, target_type, replacement_type = None):
        # check if the indices are out of range
        if node_x not in range(0, self.width) or node_y not in range(0, self.height):
            return
        # store the type of the tile
        node_type = self.array[node_y][node_x]
        # if the tile is not empty, stop recursion
        if node_type != target_type:
            return
        # if this is the first tile of a new cave,
        # increment the cave counter and use the new number as type
        if not replacement_type:
            self.cave_count += 1
            replacement_type = self.cave_count
            self.cave_dict[replacement_type] = 0
        # replace the tile with the new type
        self.array[node_y][node_x] = replacement_type
        if replacement_type > 65536:
            self.cave_dict[replacement_type] += 1
        # recurse south
        self.floodfill(node_x,
                       node_y + 1,
                       target_type,
                       replacement_type = replacement_type)
        # recurse north
        self.floodfill(node_x,
                       node_y - 1,
                       target_type,
                       replacement_type = replacement_type)
        # recurse west
        self.floodfill(node_x - 1,
                       node_y,
                       target_type,
                       replacement_type = replacement_type)
        # recurse east
        self.floodfill(node_x + 1,
                       node_y,
                       target_type,
                       replacement_type = replacement_type)

map = Map(36, 20)
map.generate()
for arr in map.array:
    for elem in arr:
        if elem == 1:
            print(' □ ', end = '')
        else:
            print('   ', end = '')
    print('')
print(map.array)
print(map.cave_dict)
