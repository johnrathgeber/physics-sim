import math, game_vars as gv, board_vars as bv

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

    def update_collisions(self, balls):
        for ball in balls:
            if not (ball.x == self.x and ball.y == self.y):
                dist = math.sqrt(abs(self.x - ball.x) ** 2 + abs(self.y - ball.y) ** 2)
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
                    m1 = self.heavy_weight if self.heavy else self.weight
                    m2 = ball.heavy_weight if ball.heavy else ball.weight
                    ncomp1_new = (ncomp1 * (m1 - gv.ball_bounce * m2) + 
                        ncomp2 * (1 + gv.ball_bounce) * m2) / (m1 + m2)
                    ncomp2_new = (ncomp2 * (m2 - gv.ball_bounce * m1) + 
                        ncomp1 * (1 + gv.ball_bounce) * m1) / (m1 + m2)
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

    def move(self, keys, balls):
        self.update_collisions(balls)
        self.update_player_movement(keys)
        super().move()
        self.check_dead()

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
    def __init__(self, color, start_x, start_y, radius, npc_weight):
        super().__init__(color, start_x, start_y, radius, npc_weight)
    
    def move(self, balls, pballs):
        self.update_collisions(balls)
        self.update_npc_movement(pballs)
        super().move()

    def update_npc_movement(self, pballs):
        mn_dist = float('inf')
        mn_pball = None
        for pball in pballs:
            dist = math.sqrt(abs(self.x - pball.x) ** 2 + abs(self.y - pball.y) ** 2)
            if dist < mn_dist:
                mn_dist = dist
                mn_pball = pball
        n1, n2 = (self.x - mn_pball.x) * dist / 5000000, (self.y - mn_pball.y) * dist / 5000000
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
        if self.dx ** 2 + self.dy ** 2 > gv.npc_max_speed ** 2:
            self.dx = (self.dx / (abs(self.dx) + abs(self.dy))) * gv.npc_max_speed
            self.dy = (self.dy / (abs(self.dx) + abs(self.dy))) * gv.npc_max_speed
