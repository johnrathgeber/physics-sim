import pygame
import random
import src.board_vars as bv
import src.balls as balls
from src.balls import PlayerBall, NPCBall
from src.powerup import Powerup
from src.settings_screen import settings_loop
from src.config import GameConfig
from src.game_vars import calculate_game_vars

pygame.init()
screen = pygame.display.set_mode((bv.WIDTH, bv.HEIGHT))
pygame.display.set_caption("Physics Sim")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
RED = (193, 21, 21)
BLUE = (118, 77, 230)
GREEN = (77, 200, 77)
GRAY = (50, 50, 50)
CREAM = (246, 243, 224)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 60, bold=True)

def title_screen():
    title_image = pygame.image.load("assets/title.png")
    title_rect = title_image.get_rect(center=(bv.WIDTH // 2, bv.HEIGHT // 2))
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
        screen.fill(CREAM)
        screen.blit(title_image, title_rect)
        pygame.display.flip()
        clock.tick(30)
    return True

if not title_screen():
    pygame.quit()
    exit()

GameConfig.create_default_preset()

config = settings_loop(screen, clock)
if config is None:
    pygame.quit()
    exit()

gv = calculate_game_vars(config)

balls.ball_bounce = gv['ball_bounce']
balls.npc_acceleration = gv['npc_acceleration']

red_start_x = bv.WIDTH // 2 + int(gv['r_radius'] + 30)
blue_start_x = bv.WIDTH // 2 - int(gv['b_radius'] + 30)
red_start_y = bv.HEIGHT // 3
blue_start_y = bv.HEIGHT // 3

running = True

def reset_game():
    rball.x, rball.y = rball.start_x, rball.start_y
    bball.x, bball.y = bball.start_x, bball.start_y
    rball.dx, rball.dy = 0, 0
    bball.dx, bball.dy = 0, 0
    rball.powered = False
    bball.powered = False
    rball.powered_time = 0
    bball.powered_time = 0
    powerup.alive = False
    powerup.dead_time = 0

rball = PlayerBall(
    RED, red_start_x, red_start_y,
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE,
    gv['r_radius'], gv['r_gravity'], gv['r_jump_force'], gv['r_vertical_force'],
    gv['r_lateral_force'], gv['r_lateral_friction'], gv['r_floor_bounce'],
    gv['r_heavy_weight'], gv['r_heavy_force_multiplier'], gv['r_weight']
)
bball = PlayerBall(
    BLUE, blue_start_x, blue_start_y,
    pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT,
    gv['b_radius'], gv['b_gravity'], gv['b_jump_force'], gv['b_vertical_force'],
    gv['b_lateral_force'], gv['b_lateral_friction'], gv['b_floor_bounce'],
    gv['b_heavy_weight'], gv['b_heavy_force_multiplier'], gv['b_weight']
)
pballs = [rball, bball]
npcballs = []
for i in range(1, gv['num_npc_balls_per_side'] + 1):
    npcballs.append(NPCBall(
        BLACK,
        bv.bar_width + 50 + gv['npc_ball_radius'],
        bv.HEIGHT - 100 - (50 + gv['npc_ball_radius']) * i,
        gv['npc_ball_radius'],
        gv['npc_weight'],
        gv['npc_max_speed']
    ))
    npcballs.append(NPCBall(
        BLACK,
        bv.WIDTH - (bv.bar_width + 50 + gv['npc_ball_radius']),
        bv.HEIGHT - 100 - (50 + gv['npc_ball_radius']) * i,
        gv['npc_ball_radius'],
        gv['npc_weight'],
        gv['npc_max_speed']
    ))

balls = pballs + npcballs

powerup_x = random.randint(bv.bar_width + 50, bv.WIDTH - bv.bar_width - 50)
powerup_y = random.randint(50, bv.floor_y - 50)
powerup = Powerup(powerup_x, powerup_y, "ultra heavy", GREEN)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    for i, ball in enumerate(balls):
        if isinstance(ball, PlayerBall):
            ball.move(keys, balls, i)
        elif isinstance(ball, NPCBall):
            ball.move(balls, pballs, i)

    screen.fill(LIGHT_GRAY)
    pygame.draw.rect(screen, GRAY, (0, bv.floor_y, bv.WIDTH, 50))
    pygame.draw.rect(screen, BLACK, (0, 0, bv.bar_width, bv.HEIGHT))
    pygame.draw.rect(screen, BLACK, (bv.WIDTH - bv.bar_width, 0, bv.bar_width, bv.HEIGHT))
    score_text = font.render(f"{bball.score} - {rball.score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(bv.WIDTH // 2, 100))
    screen.blit(score_text, text_rect)
    for pball in pballs:
        if pball.powered:
            pygame.draw.circle(screen, BLACK, (int(pball.x), int(pball.y)), pball.radius)
            pygame.draw.circle(screen, pball.color, (int(pball.x), int(pball.y)), pball.radius - 5)
        elif pball.heavy:
            pygame.draw.circle(screen, WHITE, (int(pball.x), int(pball.y)), pball.radius)
            pygame.draw.circle(screen, pball.color, (int(pball.x), int(pball.y)), pball.radius - 3)
        else:
            pygame.draw.circle(screen, pball.color, (int(pball.x), int(pball.y)), pball.radius)
        if pball.y < 0:
            pygame.draw.rect(screen, pball.color, (pball.x - 2, 5, 4, 9))
    powerup.step(pballs)
    if powerup.alive:
        pygame.draw.circle(screen, powerup.color, (int(powerup.x), int(powerup.y)), powerup.radius)
        pygame.draw.circle(screen, WHITE, (int(powerup.x), int(powerup.y)), powerup.radius - 7)
        pygame.draw.circle(screen, powerup.color, (int(powerup.x), int(powerup.y)), powerup.radius - 14)
        pygame.draw.circle(screen, WHITE, (int(powerup.x), int(powerup.y)), powerup.radius - 21)
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
