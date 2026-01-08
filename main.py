import pygame, game_vars as gv, board_vars as bv
from balls import PlayerBall, NPCBall

pygame.init()
screen = pygame.display.set_mode((bv.WIDTH, bv.HEIGHT))
pygame.display.set_caption("Physics Sim")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
RED = (193, 21, 21)
BLUE = (118, 77, 230)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 60, bold=True)

red_start_x, blue_start_x = bv.WIDTH // 2 + (gv.r_radius + 30), bv.WIDTH // 2 - (gv.b_radius + 30)
red_start_y, blue_start_y = bv.HEIGHT // 3, bv.HEIGHT // 3

running = True

def reset_game():
    rball.x, rball.y = rball.start_x, rball.start_y
    bball.x, bball.y = bball.start_x, bball.start_y
    rball.dx, rball.dy = 0, 0
    bball.dx, bball.dy = 0, 0

rball = PlayerBall(RED, red_start_x, red_start_y,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE,
            gv.r_radius, gv.r_gravity, gv.r_jump_force, gv.r_vertical_force, gv.r_lateral_force,
            gv.r_lateral_friction, gv.r_floor_bounce, gv.r_heavy_weight, 
            gv.r_heavy_force_multiplier, gv.r_weight)
bball = PlayerBall(BLUE, blue_start_x, blue_start_y,
            pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT,
            gv.b_radius, gv.b_gravity, gv.b_jump_force, gv.b_vertical_force, gv.b_lateral_force,
            gv.b_lateral_friction, gv.b_floor_bounce, gv.b_heavy_weight, 
            gv.b_heavy_force_multiplier, gv.b_weight)
pballs = [rball, bball]
npcballs = []
for i in range(1, gv.num_npc_balls_per_side + 1):
    npcballs.append(NPCBall(BLACK, bv.bar_width + 50 + gv.npc_ball_radius, 
        bv.HEIGHT - 100 - (50 + gv.npc_ball_radius)*i, gv.npc_ball_radius, gv.npc_weight))
    npcballs.append(NPCBall(BLACK, bv.WIDTH - (bv.bar_width + 50 + gv.npc_ball_radius), 
        bv.HEIGHT - 100 - (50 + gv.npc_ball_radius)*i, gv.npc_ball_radius, gv.npc_weight))
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
    pygame.draw.rect(screen, GRAY, (0, bv.floor_y, bv.WIDTH, 50))
    pygame.draw.rect(screen, BLACK, (0, 0, bv.bar_width, bv.HEIGHT))
    pygame.draw.rect(screen, BLACK, (bv.WIDTH - bv.bar_width, 0, bv.bar_width, bv.HEIGHT))
    score_text = font.render(f"{bball.score} - {rball.score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(bv.WIDTH // 2, 100))
    screen.blit(score_text, text_rect)
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
    
    red_died = not rball.alive
    blue_died = not bball.alive
    if red_died and blue_died:
        reset_game()
    elif red_died:
        bball.score += 1
        reset_game()
    elif blue_died:
        rball.score += 1
        reset_game()

pygame.quit()
