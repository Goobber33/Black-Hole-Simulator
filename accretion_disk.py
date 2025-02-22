import numpy as np
import pygame

# Constants
DISK_RADIUS = 6  # Outer edge (multiples of Schwarzschild radius)
NUM_PARTICLES = 800  # Number of gas particles
SPEED_OF_LIGHT = 3e8  # m/s

def doppler_shift_color(base_color, velocity, inclination):
    """Applies Doppler shift to color based on velocity and inclination angle."""
    beta = velocity / SPEED_OF_LIGHT  # v/c
    cos_i = np.cos(inclination)

    # Relativistic Doppler Shift Factor
    doppler_factor = np.sqrt((1 - beta) / (1 + beta))

    # Adjust color intensity for redshift (away) or blueshift (toward)
    r, g, b = base_color
    if cos_i > 0:  # Moving toward observer (blueshift)
        r *= doppler_factor
        g *= doppler_factor
        b = min(255, b / doppler_factor)  # Enhance blue
    else:  # Moving away (redshift)
        r = min(255, r / doppler_factor)  # Enhance red
        g *= doppler_factor
        b *= doppler_factor

    return (int(r), int(g), int(b))

def generate_disk_particles(black_hole_radius, screen_size):
    """Generate accretion disk particles with Doppler shift applied."""
    particles = []
    for _ in range(NUM_PARTICLES):
        # Randomly position particles in the disk
        r = np.random.uniform(3 * black_hole_radius, DISK_RADIUS * black_hole_radius)
        theta = np.random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Convert to screen space
        scale_factor = screen_size / (12 * black_hole_radius)
        screen_x = int(screen_size / 2 + x * scale_factor)
        screen_y = int(screen_size / 2 - y * scale_factor)

        # Compute velocity at this radius (Keplerian rotation)
        velocity = np.sqrt(6.67430e-11 * 1.989e30 / r)  # v = sqrt(GM/r)

        # Compute Doppler Shift based on inclination (edge-on disk = max effect)
        inclination_angle = np.arctan2(y, x)  # Angle relative to observer
        color = doppler_shift_color((255, 50, 50), velocity, inclination_angle)

        particles.append((screen_x, screen_y, color))

    return particles

def draw_accretion_disk(screen, particles):
    """Draws the accretion disk on the Pygame screen."""
    for x, y, color in particles:
        pygame.draw.circle(screen, color, (x, y), 2)  # Small glowing particles
