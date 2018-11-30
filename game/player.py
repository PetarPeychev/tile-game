import pygame
from colors import *
from settings import *
from tile_types import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE * 2,
                                    TILESIZE * 3))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.vx, self.vy = 0, 0

    def get_user_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if not self.is_floating():
                self.vy = -PLAYER_JUMP
        if keys[pygame.K_e]:
            self.throw_hook(pygame.mouse.get_pos())

    def move(self, dx = 0, dy = 0):
        player_top = int((self.rect.top) / TILESIZE)
        player_bottom = int((self.rect.bottom - 1) / TILESIZE)
        player_left = int((self.rect.left) / TILESIZE)
        player_right = int((self.rect.right - 1) / TILESIZE)

        distance_top = self.game.map.height
        distance_bottom = self.game.map.height
        distance_left = self.game.map.width
        distance_right = self.game.map.width

        for row in range(player_top, player_bottom + 1):
            for col in range(player_right + 1, self.game.map.width):
                try:
                    if self.game.map.array[row][col] in COLLIDABLES:
                        new_distance_right = col * TILESIZE - self.rect.right
                        if new_distance_right < distance_right:
                            distance_right = new_distance_right
                        break
                    else:
                        new_distance_right = self.game.map.width * TILESIZE - self.rect.right
                except: new_distance_right = self.game.map.width * TILESIZE - self.rect.right
                if new_distance_right < distance_right:
                    distance_right = new_distance_right
            for col in range(player_left - 1, -1, -1):
                try:
                    if self.game.map.array[row][col] in COLLIDABLES:
                        new_distance_left = self.rect.left - col * TILESIZE - 16
                        if new_distance_left < distance_left:
                            distance_left = new_distance_left
                        break
                    else:
                        new_distance_left = self.rect.left
                except: new_distance_left = self.rect.left
                if new_distance_left < distance_left:
                    distance_left = new_distance_left

        for col in range(player_left, player_right + 1):
            for row in range(player_bottom + 1, self.game.map.height):
                try:
                    if self.game.map.array[row][col] in COLLIDABLES:
                        new_distance_bottom = row * TILESIZE - self.rect.bottom
                        if new_distance_bottom < distance_bottom:
                            distance_bottom = new_distance_bottom
                        break
                    else:
                        new_distance_bottom = self.game.map.height * TILESIZE - self.rect.bottom
                except: new_distance_bottom = self.game.map.height * TILESIZE - self.rect.bottom
                if new_distance_bottom < distance_bottom:
                    distance_bottom = new_distance_bottom
            for row in range(player_top - 1, -1, -1):
                try:
                    if self.game.map.array[row][col] in COLLIDABLES:
                        new_distance_top = self.rect.top - row * TILESIZE - 16
                        if new_distance_top < distance_top:
                            distance_top = new_distance_top
                        break
                    else:
                        new_distance_top = self.rect.top
                except: new_distance_top = self.rect.top
                if new_distance_top < distance_top:
                    distance_top = new_distance_top

        if dx > 0:
            # if (not self.is_floating() and
            #     self.game.map.array[player_bottom - 1][player_right + 1] == 0 and
            #     self.game.map.array[player_bottom][player_right + 1] == 1):
            #     self.rect.y -= TILESIZE
            #     self.rect.x += dx
            # else:
            #     self.rect.x += min(dx, distance_right)
            self.rect.x += min(dx, distance_right)
        elif dx < 0:
            # if (not self.is_floating() and
            #     self.game.map.array[player_bottom - 1][player_left - 1] == 0 and
            #     self.game.map.array[player_bottom][player_left - 1] == 1):
            #     self.rect.y -= TILESIZE
            #     self.rect.x += dx
            # else:
            #     self.rect.x -= min(-dx, distance_left)
            self.rect.x -= min(-dx, distance_left)
        if dy > 0:
            self.rect.y += min(dy, distance_bottom)
        elif dy < 0:
            if distance_top <= 0:
                self.vy = -0.5 * self.vy
            else:
                self.rect.y -= min(-dy, distance_top)

    def is_floating(self):
        player_top = int((self.rect.top) / TILESIZE)
        player_bottom = int((self.rect.bottom - 1) / TILESIZE)
        player_left = int((self.rect.left) / TILESIZE)
        player_right = int((self.rect.right - 1) / TILESIZE)

        distance_bottom = self.game.map.width

        for col in range(player_left, player_right + 1):
            for row in range(player_bottom + 1, self.game.map.height):
                try:
                    if self.game.map.array[row][col] in COLLIDABLES:
                        new_distance_bottom = row * TILESIZE - self.rect.bottom
                        if new_distance_bottom < distance_bottom:
                            distance_bottom = new_distance_bottom
                        break
                    else:
                        new_distance_bottom = self.game.map.height * TILESIZE - self.rect.bottom
                except: new_distance_bottom = self.game.map.height * TILESIZE - self.rect.bottom
                if new_distance_bottom < distance_bottom:
                    distance_bottom = new_distance_bottom

        if distance_bottom == 0:
            return False
        else:
            return True

    def get_gravity(self):
        if self.is_floating() and self.vy < GRAV_ACC:
            self.vy += GRAV_ACC * self.game.dt

    def top_collides_map(self):
        if self.game.map.collides_with(self.rect.x + 0.5 * TILESIZE,
                                       self.rect.y):
            return True
        if self.game.map.collides_with(self.rect.x + 1.5 * TILESIZE,
                                            self.rect.y):
            return True
        return False

    def bottom_colides_map(self):
        if self.game.map.collides_with(self.rect.x + 0.5 * TILESIZE,
                                            self.rect.y + 3 * TILESIZE):
            return True
        if self.game.map.collides_with(self.rect.x + 1.5 * TILESIZE,
                                            self.rect.y + 3 * TILESIZE):
            return True
        return False

    def left_collides_map(self):
        if self.game.map.collides_with(self.rect.x,
                                            self.rect.y + 0.5 * TILESIZE):
            return True
        if self.game.map.collides_with(self.rect.x,
                                            self.rect.y + 1.5 * TILESIZE):
            return True
        if self.game.map.collides_with(self.rect.x,
                                            self.rect.y + 2.5 * TILESIZE):
            return True
        return False

    def right_collides_map(self):
        if self.game.map.collides_with(self.rect.x + 2 * TILESIZE,
                                            self.rect.y + 0.5 * TILESIZE):
            return True
        if self.game.map.collides_with(self.rect.x + 2 * TILESIZE,
                                            self.rect.y + 1.5 * TILESIZE):
            return True
        if self.game.map.collides_with(self.rect.x + 2 * TILESIZE,
                                            self.rect.y + 2.5 * TILESIZE):
            return True
        return False

    def throw_hook(self, rel_pos):
        (camera_x, camera_y) = self.game.camera.camera.topleft
        (abs_x, abs_y) = (rel_pos[0] - camera_x, rel_pos[1] - camera_y)
        print(abs_x, abs_y)

    def update(self):
        self.get_user_movement()
        self.get_gravity()
        self.move(dx = self.vx * self.game.dt)
        self.move(dy = self.vy * self.game.dt)
        self.vx = 0
