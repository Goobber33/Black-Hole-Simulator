import pygame
import numpy as np
from ray_tracing import compute_light_path, schwarzschild_radius
from accretion_disk import generate_disk_bands, draw_accretion_disk

# Pygame Setup
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1300, 1300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Image Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initial Black Hole Parameters
M = 1.989e30  # Mass of black hole
r_s = schwarzschild_radius(M)

# Rotation angle (disk spin)
rotation_angle = 0

# Camera angles (tilt and rotation)
camera_tilt = 0  # Look up/down
camera_rotation = 0  # Rotate left/right

# Simulation Loop
running = True
clock = pygame.time.Clock()  # Control frame rate

while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                M *= 1.1
            elif event.key == pygame.K_DOWN:
                M *= 0.9
            elif event.key == pygame.K_LEFT:
                camera_rotation -= 0.1  # Rotate left
            elif event.key == pygame.K_RIGHT:
                camera_rotation += 0.1  # Rotate right
            elif event.key == pygame.K_w:
                camera_tilt -= 0.1  # Look up
            elif event.key == pygame.K_s:
                camera_tilt += 0.1  # Look down

            # Recalculate Schwarzschild radius and light path
            r_s = schwarzschild_radius(M)

    # Update rotation angle for animation
    rotation_angle += 0.01  # Adjust speed here

    # Generate rotating accretion disk bands with 3D perspective
    disk_bands = generate_disk_bands(r_s, WIDTH, rotation_angle, camera_tilt, camera_rotation)

    # Draw Accretion Disk
    draw_accretion_disk(screen, disk_bands)

    # Draw Black Hole (Event Horizon)
    pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), int(2 * r_s * 150 / r_s))

    # Update Screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)  # Limits FPS to 30 for smooth animation

pygame.quit()
