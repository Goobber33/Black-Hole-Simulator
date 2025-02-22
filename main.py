import pygame
import numpy as np
from ray_tracing import compute_light_path, schwarzschild_radius
from accretion_disk import generate_disk_particles, draw_accretion_disk

# Pygame Setup
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Image Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initial Black Hole Parameters
M = 1.989e30  # Mass of black hole
r_s = schwarzschild_radius(M)

# Generate Accretion Disk Particles
disk_particles = generate_disk_particles(r_s, WIDTH)

# Simulation Loop
running = True
light_path = compute_light_path(r0=5*r_s, dr_dt0=-3e8, dphi_dt0=0.001)

# Convert to screen coordinates
def to_screen_coords(x, y):
    scale = 150 / r_s  # Scale factor for visualization
    return int(WIDTH // 2 + x * scale), int(HEIGHT // 2 - y * scale)

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

            # Recalculate Schwarzschild radius and light path
            r_s = schwarzschild_radius(M)
            light_path = compute_light_path(r0=5*r_s, dr_dt0=-3e8, dphi_dt0=0.001)
            disk_particles = generate_disk_particles(r_s, WIDTH)  # Update accretion disk

    # Draw Accretion Disk with Doppler Effect
    draw_accretion_disk(screen, disk_particles)

    # Draw Black Hole (Event Horizon)
    pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), int(2 * r_s * 150 / r_s))

    # Draw Light Path
    x_vals, y_vals = light_path[0], light_path[1]
    for i in range(len(x_vals) - 1):
        x1, y1 = to_screen_coords(x_vals[i], y_vals[i])
        x2, y2 = to_screen_coords(x_vals[i + 1], y_vals[i + 1])
        pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 1)

    # Update Screen
    pygame.display.flip()

pygame.quit()
