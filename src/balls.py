import math
import src.board_vars as bv

ball_bounce = 0.9
npc_acceleration = 1

class Ball:
    def __init__(self, color, start_x, start_y, radius, weight):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.radius = radius
        self.heavy = False
        self.weight = weight
        self.heavy_weight = 1
        self.dx = 0
        self.dy = 0
        self.powered = False

    def update_collisions(self, balls, start_idx):
        global ball_bounce
        for i in range(start_idx + 1, len(balls)):
            ball = balls[i]
            if not (ball.x == self.x and ball.y == self.y):
                dist = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
                if dist <= self.radius + ball.radius:
                    n1, n2 = (self.x - ball.x) / dist, (self.y - ball.y) / dist
                    if dist < self.radius + ball.radius:
                        overlap = self.radius + ball.radius - dist
                        self.x += overlap * n1
                        self.y += overlap * n2
                        ball.x -= overlap * n1
                        ball.y -= overlap * n2
                    t1, t2 = -n2, n1
                    ncomp1 = self.dx * n1 + self.dy * n2
                    ncomp2 = ball.dx * n1 + ball.dy * n2
                    if self.powered:
                        m1 = self.heavy_weight * 100
                    elif self.heavy:
                        m1 = self.heavy_weight
                    else:
                        m1 = self.weight
                    if ball.powered:
                        m2 = ball.heavy_weight * 100
                    elif ball.heavy:
                        m2 = ball.heavy_weight
                    else:
                        m2 = ball.weight
                    ncomp1_new = (ncomp1 * (m1 - ball_bounce * m2) +
                        ncomp2 * (1 + ball_bounce) * m2) / (m1 + m2)
                    ncomp2_new = (ncomp2 * (m2 - ball_bounce * m1) +
                        ncomp1 * (1 + ball_bounce) * m1) / (m1 + m2)
                    tcomp1 = self.dx * t1 + self.dy * t2
                    tcomp2 = ball.dx * t1 + ball.dy * t2
                    self.dx, ball.dx = ncomp1_new * n1 + tcomp1 * t1, ncomp2_new * n1 + tcomp2 * t1
                    self.dy, ball.dy = ncomp1_new * n2 + tcomp1 * t2, ncomp2_new * n2 + tcomp2 * t2

    def move(self):
        self.x += self.dx
        self.y += self.dy

class PlayerBall(Ball):
    def __init__(self, color, start_x, start_y, up, down, left, right, heavy_key,
            radius, gravity, jump_force, vertical_force, lateral_force,
            lateral_friction, floor_bounce, heavy_weight, heavy_force_multiplier, weight):
        super().__init__(color, start_x, start_y, radius, weight)
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.heavy_key = heavy_key
        self.heavy = False
        self.gravity = gravity
        self.jump_force = jump_force
        self.vertical_force = vertical_force
        self.lateral_force = lateral_force
        self.lateral_friction = lateral_friction
        self.floor_bounce = floor_bounce
        self.heavy_weight = heavy_weight
        self.heavy_force_multiplier = heavy_force_multiplier
        self.score = 0
        self.alive = True
        self.powered_time = 0
        self.powerup_refresh = 300

    def move(self, keys, balls, start_idx):
        self.update_collisions(balls, start_idx)
        self.update_player_movement(keys)
        super().move()
        self.check_dead()
        self.check_power()

    def check_power(self):
        if self.powered:
            self.powered_time += 1
            if self.powered_time >= self.powerup_refresh:
                self.powered_time = 0
                self.powered = False

    def update_player_movement(self, keys):
        self.heavy = keys[self.heavy_key]
        if keys[self.up]:
            self.dy -= self.vertical_force if not self.heavy else self.vertical_force * self.heavy_force_multiplier
        if keys[self.down]:
            self.dy += self.vertical_force if not self.heavy else self.vertical_force * self.heavy_force_multiplier
        if keys[self.right]:
            self.dx += self.lateral_force if not self.heavy else self.lateral_force * self.heavy_force_multiplier
        if keys[self.left]:
            self.dx -= self.lateral_force if not self.heavy else self.lateral_force * self.heavy_force_multiplier
        if self.dx > 0:
            self.dx -= self.lateral_friction
        if self.dx < 0:
            self.dx += self.lateral_friction

        if abs(self.dx) < 0.001:
            self.dx = 0
        if self.y + self.radius >= bv.floor_y and keys[self.up]:
            self.dy = self.jump_force if not self.heavy else self.jump_force * self.heavy_force_multiplier
        elif self.y + self.radius >= bv.floor_y:
            self.y = bv.floor_y - self.radius
            bounce_mul = 0.6 if self.heavy else 1
            self.dy = -self.dy * self.floor_bounce * bounce_mul
            if abs(self.dy) < self.gravity * 2:
                self.dy = 0
        self.dy += self.gravity

    def check_dead(self):
        dead = self.x - self.radius < bv.bar_width or self.x + self.radius > bv.WIDTH - bv.bar_width
        self.alive = not dead

class NPCBall(Ball):
    def __init__(self, color, start_x, start_y, radius, npc_weight, npc_max_speed):
        super().__init__(color, start_x, start_y, radius, npc_weight)
        self.npc_max_speed = npc_max_speed

    def move(self, balls, pballs, start_idx):
        self.update_collisions(balls, start_idx)
        self.update_npc_movement(pballs)
        super().move()

    def update_npc_movement(self, pballs):
        global npc_acceleration
        mn_dist = float('inf')
        mn_pball = None
        for pball in pballs:
            dist = math.sqrt(abs(self.x - pball.x) ** 2 + abs(self.y - pball.y) ** 2)
            if dist < mn_dist:
                mn_dist = dist
                mn_pball = pball
        n1 = (self.x - mn_pball.x) * mn_dist * npc_acceleration / 5000000
        n2 = (self.y - mn_pball.y) * mn_dist * npc_acceleration / 5000000
        self.dx -= n1
        self.dy -= n2
        if self.y + self.radius >= bv.floor_y:
            self.y = bv.floor_y - self.radius
            self.dy = -self.dy
        if self.x + self.radius >= bv.WIDTH - bv.bar_width:
            self.x = bv.WIDTH - bv.bar_width - self.radius
            self.dx = -self.dx
        if self.x - self.radius <= bv.bar_width:
            self.x = bv.bar_width + self.radius
            self.dx = -self.dx
        if self.dx ** 2 + self.dy ** 2 > self.npc_max_speed ** 2:
            self.dx = (self.dx / (abs(self.dx) + abs(self.dy))) * self.npc_max_speed
            self.dy = (self.dy / (abs(self.dx) + abs(self.dy))) * self.npc_max_speed
