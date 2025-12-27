import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Sim")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (118, 77, 230)
GRAY = (50, 50, 50)

x, y = 500, 100
x2, y2 = 300, 100
radius = 20
dy = 0
dx = 0
dy2 = 0
dx2 = 0

gravity = 0.5
jump_force = -15
lateral_force = 4
lateral_friction = 0.05
bounce = 0.7
ball_bounce = 0.9
floor_y = 550

running = True

while running:
    do_keys = True
    dist = math.sqrt(abs(x - x2) ** 2 + abs(y - y2) ** 2)
    if dist <= 2 * radius:
        n1, n2 = (x - x2) / dist, (y - y2) / dist
        if dist < 2 * radius:
            overlap = 2 * radius - dist
            x += overlap * n1
            y += overlap * n2
            x2 -= overlap * n1
            y2 -= overlap * n2
        t1, t2 = -n2, n1
        ncomp1 = dx * n1 + dy * n2
        ncomp2 = dx2 * n1 + dy2 * n2
        ncomp1_new = (ncomp1 * (1 - ball_bounce) + ncomp2 * (1 + ball_bounce)) / 2
        ncomp2_new = (ncomp1 * (1 + ball_bounce) + ncomp2 * (1 - ball_bounce)) / 2
        tcomp1 = dx * t1 + dy * t2
        tcomp2 = dx2 * t1 + dy2 * t2
        dx, dx2 = ncomp1_new * n1 + tcomp1 * t1, ncomp2_new * n1 + tcomp2 * t1
        dy, dy2 = ncomp1_new * n2 + tcomp1 * t2, ncomp2_new * n2 + tcomp2 * t2
        do_keys = False
    if do_keys:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y + radius >= floor_y - 10:
                        dy = jump_force
                if event.key == pygame.K_RIGHT:
                    dx = lateral_force
                if event.key == pygame.K_LEFT:
                    dx = -lateral_force
                if event.key == pygame.K_w:
                    if y2 + radius >= floor_y - 10:
                        dy2 = jump_force
                if event.key == pygame.K_d:
                    dx2 = lateral_force
                if event.key == pygame.K_a:
                    dx2 = -lateral_force

    keys = pygame.key.get_pressed()
    if do_keys:
        if keys[pygame.K_RIGHT]:
            dx = lateral_force
        if keys[pygame.K_LEFT]:
            dx = -lateral_force
    if dx > 0:
        dx -= lateral_friction
    if dx < 0:
        dx += lateral_friction

    if abs(dx) < 0.001:
        dx = 0
    if do_keys and y + radius >= floor_y and keys[pygame.K_UP]:
        dy = jump_force
    elif y + radius >= floor_y:
        y = floor_y - radius
        dy = -dy * bounce
        if abs(dy) < gravity * 2:
            dy = 0
    if do_keys:
        dy += gravity
    x += dx
    y += dy

    if do_keys:
        if keys[pygame.K_d]:
            dx2 = lateral_force
        if keys[pygame.K_a]:
            dx2 = -lateral_force
    if dx2 > 0:
        dx2 -= lateral_friction
    if dx2 < 0:
        dx2 += lateral_friction

    if abs(dx2) < 0.001:
        dx2 = 0
    if do_keys and y2 + radius >= floor_y and keys[pygame.K_w]:
        dy2 = jump_force
    elif y2 + radius >= floor_y:
        y2 = floor_y - radius
        dy2 = -dy2 * bounce
        if abs(dy2) < gravity * 2:
            dy2 = 0

    if do_keys:
        dy2 += gravity
    x2 += dx2
    y2 += dy2

    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, floor_y, WIDTH, 50))
    pygame.draw.circle(screen, RED, (int(x), int(y)), radius)
    pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()