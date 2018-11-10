import pygame
import automatagen
import random

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate(self):
        terrgen = automatagen.TerrainGenerator()
        boolarr = terrgen.generate(int(self.width / 2), int(self.height / 2))
        self.seed = terrgen.seed
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]
        for y in range(0, self.height):
            for x in range(0, self.width):
                if boolarr[int(y / 2)][int(x / 2)]:
                    self.array[y][x] = 1
                else:
                    self.array[y][x] = 0

        temp_array = self.array

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
                    if count >= 5 and random.random() > 0.2:
                        self.array[y][x] = 1

map = Map(56, 44)
map.generate()
for arr in map.array:
    for elem in arr:
        if elem == 1:
            print(' @ ', end = '')
        else:
            print('   ', end = '')
    print('')
