import pygame
# import math
from balls import PlayerBall, NPCBall

pygame.init()
WIDTH, HEIGHT = 1900, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Sim")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
RED = (193, 21, 21)
BLUE = (118, 77, 230)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 60, bold=True)

score_red = 0
score_blue = 0

red_start_x, red_start_y = (2 * WIDTH) // 3, HEIGHT // 3
blue_start_x, blue_start_y = WIDTH // 3, HEIGHT // 3

# x, y = red_start_x, red_start_y
# x2, y2 = blue_start_x, blue_start_y
radius = 20
# dx, dy = 0, 0
# dx2, dy2 = 0, 0

gravity = 0.5
jump_force = -7
vertical_force = 0.4
min_fall_speed = 0.5
lateral_force = 0.1
lateral_friction = 0.02
bounce = 0.7
ball_bounce = 0.9
floor_y = 1000
heavy_weight = 2
heavy_force_multiplier = 0.8
# bheavy = False
# rheavy = False

bar_width = 100

# def reset_game():
#     global x, y, dx, dy, x2, y2, dx2, dy2, rheavy, bheavy
#     x, y = red_start_x, red_start_y
#     x2, y2 = blue_start_x, blue_start_y
#     dx, dy = 0, 0
#     dx2, dy2 = 0, 0
#     rheavy = False
#     bheavy = False

running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     dist = math.sqrt(abs(x - x2) ** 2 + abs(y - y2) ** 2)
#     if dist <= 2 * radius:
#         n1, n2 = (x - x2) / dist, (y - y2) / dist
#         if dist < 2 * radius:
#             overlap = 2 * radius - dist
#             x += overlap * n1
#             y += overlap * n2
#             x2 -= overlap * n1
#             y2 -= overlap * n2
#         t1, t2 = -n2, n1
#         ncomp1 = dx * n1 + dy * n2
#         ncomp2 = dx2 * n1 + dy2 * n2
#         m1 = heavy_weight if rheavy else 1
#         m2 = heavy_weight if bheavy else 1
#         ncomp1_new = (ncomp1 * (m1 - ball_bounce * m2) + ncomp2 * (1 + ball_bounce) * m2) / (m1 + m2)
#         ncomp2_new = (ncomp2 * (m2 - ball_bounce * m1) + ncomp1 * (1 + ball_bounce) * m1) / (m1 + m2)
#         tcomp1 = dx * t1 + dy * t2
#         tcomp2 = dx2 * t1 + dy2 * t2
#         dx, dx2 = ncomp1_new * n1 + tcomp1 * t1, ncomp2_new * n1 + tcomp2 * t1
#         dy, dy2 = ncomp1_new * n2 + tcomp1 * t2, ncomp2_new * n2 + tcomp2 * t2

#     keys = pygame.key.get_pressed()
#     rheavy = keys[pygame.K_SPACE]
#     bheavy = keys[pygame.K_LSHIFT]
#     if keys[pygame.K_UP]:
#         dy -= vertical_force if not rheavy else vertical_force * heavy_force_multiplier
#         if dy > 0:
#             dy = max(dy, min_fall_speed)
#     if keys[pygame.K_DOWN]:
#         dy += vertical_force if not rheavy else vertical_force * heavy_force_multiplier
#     if keys[pygame.K_RIGHT]:
#         dx += lateral_force if not rheavy else lateral_force * heavy_force_multiplier
#     if keys[pygame.K_LEFT]:
#         dx -= lateral_force if not rheavy else lateral_force * heavy_force_multiplier
#     if dx > 0:
#         dx -= lateral_friction
#     if dx < 0:
#         dx += lateral_friction

#     if abs(dx) < 0.001:
#         dx = 0
#     if y + radius >= floor_y and keys[pygame.K_UP]:
#         dy = jump_force if not rheavy else jump_force * heavy_force_multiplier
#     elif y + radius >= floor_y:
#         y = floor_y - radius
#         r_bounce_multiplier = 0.6 if rheavy else 1
#         dy = -dy * bounce * r_bounce_multiplier
#         if abs(dy) < gravity * 2:
#             dy = 0
#     dy += gravity
#     x += dx
#     y += dy

#     if keys[pygame.K_w]:
#         dy2 -= vertical_force if not bheavy else vertical_force * heavy_force_multiplier
#         if dy2 > 0:
#             dy2 = max(dy2, min_fall_speed)
#     if keys[pygame.K_s]:
#         dy2 += vertical_force if not bheavy else vertical_force * heavy_force_multiplier
#     if keys[pygame.K_d]:
#         dx2 += lateral_force if not bheavy else lateral_force * heavy_force_multiplier
#     if keys[pygame.K_a]:
#         dx2 -= lateral_force if not bheavy else lateral_force * heavy_force_multiplier
#     if dx2 > 0:
#         dx2 -= lateral_friction
#     if dx2 < 0:
#         dx2 += lateral_friction

#     if abs(dx2) < 0.001:
#         dx2 = 0
#     if y2 + radius >= floor_y and keys[pygame.K_w]:
#         dy2 = jump_force if not bheavy else jump_force * heavy_force_multiplier
#     elif y2 + radius >= floor_y:
#         y2 = floor_y - radius
#         b_bounce_multiplier = 0.6 if bheavy else 1
#         dy2 = -dy2 * bounce * b_bounce_multiplier
#         if abs(dy2) < gravity * 2:
#             dy2 = 0
#     dy2 += gravity
#     x2 += dx2
#     y2 += dy2

#     red_died = False
#     blue_died = False
#     if x - radius < bar_width or x + radius > WIDTH - bar_width:
#         red_died = True
#     if x2 - radius < bar_width or x2 + radius > WIDTH - bar_width:
#         blue_died = True
#     if red_died and blue_died:
#         reset_game()
#     elif red_died:
#         score_blue += 1
#         reset_game()
#     elif blue_died:
#         score_red += 1
#         reset_game()

#     screen.fill(LIGHT_GRAY)
#     pygame.draw.rect(screen, GRAY, (0, floor_y, WIDTH, 50))
#     pygame.draw.rect(screen, BLACK, (0, 0, bar_width, HEIGHT))
#     pygame.draw.rect(screen, BLACK, (WIDTH - bar_width, 0, bar_width, HEIGHT))
#     score_text = font.render(f"{score_blue} - {score_red}", True, (0, 0, 0))
#     text_rect = score_text.get_rect(center=(WIDTH // 2, 100))
#     screen.blit(score_text, text_rect)
#     if rheavy:
#         pygame.draw.circle(screen, WHITE, (int(x), int(y)), radius)
#         pygame.draw.circle(screen, RED, (int(x), int(y)), radius - 3)
#     else:
#         pygame.draw.circle(screen, RED, (int(x), int(y)), radius)
#     if bheavy:
#         pygame.draw.circle(screen, WHITE, (int(x2), int(y2)), radius)
#         pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), radius - 3)
#     else:
#         pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), radius)
#     if y < 0:
#         pygame.draw.rect(screen, RED, (x - 2, 5, 4, 9))
#     if y2 < 0:
#         pygame.draw.rect(screen, BLUE, (x2 - 2, 5, 4, 9))
#     pygame.display.flip()
#     clock.tick(60)

rball = PlayerBall(RED, red_start_x, red_start_y, 
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE,
            radius, gravity, jump_force, vertical_force, min_fall_speed, lateral_force,
            lateral_friction, bounce, heavy_weight, heavy_force_multiplier)
bball = PlayerBall(BLUE, blue_start_x, blue_start_y, 
            pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT,
            radius, gravity, jump_force, vertical_force, min_fall_speed, lateral_force,
            lateral_friction, bounce, heavy_weight, heavy_force_multiplier)
pballs = [rball, bball]
npcballs = []
num_bludgers_each_side = 3
for i in range(1, num_bludgers_each_side + 1):
    npcballs.append(NPCBall(BLACK, 200, 80*i, 30))
    npcballs.append(NPCBall(BLACK, WIDTH - 200, 80*i, 30))
balls = pballs + npcballs
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    balls_cpy = balls[::-1]

    for pball in pballs:
        pball.move(keys, balls_cpy)
        balls_cpy.pop()
    for npcball in npcballs:
        npcball.move(balls_cpy, pballs)
        balls_cpy.pop()

    screen.fill(LIGHT_GRAY)
    pygame.draw.rect(screen, GRAY, (0, floor_y, WIDTH, 50))
    pygame.draw.rect(screen, BLACK, (0, 0, bar_width, HEIGHT))
    pygame.draw.rect(screen, BLACK, (WIDTH - bar_width, 0, bar_width, HEIGHT))
    # score_text = font.render(f"{score_blue} - {score_red}", True, (0, 0, 0))
    # text_rect = score_text.get_rect(center=(WIDTH // 2, 100))
    # screen.blit(score_text, text_rect)
    for pball in pballs:
        if pball.heavy:
            pygame.draw.circle(screen, WHITE, (int(pball.x), int(pball.y)), pball.radius)
            pygame.draw.circle(screen, pball.color, (int(pball.x), int(pball.y)), pball.radius - 3)
        else:
            pygame.draw.circle(screen, pball.color, (int(pball.x), int(pball.y)), pball.radius)
        if pball.y < 0:
            pygame.draw.rect(screen, pball.color, (pball.x - 2, 5, 4, 9))
    for npcball in npcballs:
        pygame.draw.circle(screen, npcball.color, (int(npcball.x), int(npcball.y)), npcball.radius)
    pygame.display.flip()
    clock.tick(60)
    
    # red_died = False
    # blue_died = False
    # if x - radius < bar_width or x + radius > WIDTH - bar_width:
    #     red_died = True
    # if x2 - radius < bar_width or x2 + radius > WIDTH - bar_width:
    #     blue_died = True
    # if red_died and blue_died:
    #     reset_game()
    # elif red_died:
    #     score_blue += 1
    #     reset_game()
    # elif blue_died:
    #     score_red += 1
    #     reset_game()

pygame.quit()