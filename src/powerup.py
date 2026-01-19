import math
import random
import colorsys
import src.board_vars as bv

class Powerup:
    def __init__(self, start_x, start_y, p_type, color):
        self.x = start_x
        self.y = start_y
        self.radius = 30
        self.type = p_type
        self.alive = False
        self.dead_time = 0
        self.refresh_time = 300
        self.base_color = color
        self.color = color
        self.hue = 0.0
        self.rotation = 0

    def randomize_position(self):
        self.x = random.randint(bv.bar_width + self.radius + 20,
                               bv.WIDTH - bv.bar_width - self.radius - 20)
        self.y = random.randint(self.radius + 20, bv.floor_y - self.radius - 20)

    def update_color(self):
        rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def collision(self, pballs):
        if not self.alive:
            return
        for ball in pballs:
            dist = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
            if dist <= self.radius + ball.radius:
                ball.powered = True
                ball.powered_time = 0
                self.alive = False

    def step(self, pballs):
        self.collision(pballs)
        if self.alive:
            self.hue += 0.003
            if self.hue >= 1.0:
                self.hue = 0.0
            self.update_color()
        if not self.alive:
            self.dead_time += 1
            if self.dead_time >= self.refresh_time:
                self.alive = True
                self.dead_time = 0
                self.randomize_position()
