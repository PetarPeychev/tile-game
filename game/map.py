import pygame
import automatagen
import random
from tile_types import *
import resource, sys
from misc_functions import recursionlimit
from settings import *
from queue import Queue
#import numpy as np
#import matplotlib.pyplot as plt

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def collides_with(self, x, y):
        tile_x = int(x / TILESIZE)
        tile_y = int(y / TILESIZE)
        try:
            if self.array[tile_y][tile_x] != 1:
                return False
            else:
                return True
        except:
            return True

    def generate(self):
        self.generate_caves()
        caves = self.floodfill(AIR)
        largest_cave = []
        smaller_caves = []
        for cave in caves:
            if len(cave) > len(largest_cave):
                smaller_caves.append(largest_cave)
                largest_cave = cave
            else:
                smaller_caves.append(cave)


    def generate_caves(self):
        # instantiate TerrainGenerator with default settings
        terrgen = automatagen.TerrainGenerator(initial_density = 0.55)
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

    def check_node_validity(self, x, y, target_type, visited_list):
        if x not in range(self.width) or y not in range(self.height):
            return False
        else:
            if self.array[y][x] == target_type and (x, y) not in visited_list:
                return True
            else:
                return False

    def floodfill(self, target_type):
        # goes through map and stores a list of lists of tuple coordinates (list of caves)
        # and returns them, effectively storing all caves on the map, using BFS floodfill
        cave_list = []
        visited_list = []
        for y in range(self.height):
            for x in range(self.width):
                if self.check_node_validity(x, y, target_type, visited_list):
                    current_cave = []
                    q = Queue()
                    q.put((x, y))
                    visited_list.append((x, y))
                    while not q.empty():
                        (x1, y1) = q.get()
                        current_cave.append((x1, y1))
                        visited_list.append((x1, y1))

                        if (self.check_node_validity(x1 + 1, y1, target_type, visited_list)):
                            q.put((x1 + 1, y1))
                            visited_list.append((x1 + 1, y1))
                        if (self.check_node_validity(x1 - 1, y1, target_type, visited_list)):
                            q.put((x1 - 1, y1))
                            visited_list.append((x1 - 1, y1))
                        if (self.check_node_validity(x1, y1 + 1, target_type, visited_list)):
                            q.put((x1, y1 + 1))
                            visited_list.append((x1, y1 + 1))
                        if (self.check_node_validity(x1, y1 - 1, target_type, visited_list)):
                            q.put((x1, y1 - 1))
                            visited_list.append((x1, y1 - 1))
                    cave_list.append(current_cave)
        return cave_list

# mapp = Map(256, 64)
# mapp.generate()
# for arr in mapp.array:
#     for elem in arr:
#         if elem == 1:
#             print(' □ ', end = '')
#         else:
#             print('   ', end = '')
#     print('')
# print(mapp.array)
# print(mapp.cave_dict)
# def normalize(subarr):
#     def norm(x):
#         if x > 255:
#             x = 255
#         else:
#             x = x * 40
#         return x
#     return list(map(norm, subarr))
# maparr = list(map(normalize, mapp.array))
# print(maparr)
# plt.imshow(maparr)
# plt.show()
