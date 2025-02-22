import numpy as np
import pygame

# Constants
DISK_RADIUS = 6  # Outer edge in Schwarzschild radii
INNER_DISK = 2.5  # Inner edge of the disk
NUM_BANDS = 150  # Increased number of smooth bands for the disk
SPEED_OF_LIGHT = 3e8  # m/s

def doppler_shift_color(base_color, velocity, inclination):
    """Applies relativistic Doppler shift to colors element-wise."""
    beta = velocity / SPEED_OF_LIGHT  # v/c
    doppler_factor = np.sqrt((1 - beta) / (1 + beta))

    # Convert base color
    r, g, b = base_color

    # Apply Doppler effect based on inclination direction (element-wise)
    shifted_colors = np.zeros((len(inclination), 3), dtype=int)

    blueshift_mask = inclination > 0  # Moving toward observer
    redshift_mask = ~blueshift_mask   # Moving away

    shifted_colors[blueshift_mask, 0] = (r * doppler_factor).astype(int)
    shifted_colors[blueshift_mask, 1] = (g * doppler_factor).astype(int)
    shifted_colors[blueshift_mask, 2] = np.minimum(255, (b / doppler_factor)).astype(int)  # Enhance blue

    shifted_colors[redshift_mask, 0] = np.minimum(255, (r / doppler_factor)).astype(int)  # Enhance red
    shifted_colors[redshift_mask, 1] = (g * doppler_factor).astype(int)
    shifted_colors[redshift_mask, 2] = (b * doppler_factor).astype(int)

    return shifted_colors  # Now returns an array of colors

def rotate_points_3d(x, y, z, angle_x, angle_y):
    """Fixes 3D rotation to correctly tilt the accretion disk."""
    cos_x, sin_x = np.cos(angle_x), np.sin(angle_x)
    cos_y, sin_y = np.cos(angle_y), np.sin(angle_y)

    # Rotate around X-axis (tilt up/down)
    y_rot = y * cos_x - z * sin_x
    z_rot = y * sin_x + z * cos_x

    # Rotate around Y-axis (left/right rotation)
    x_final = x * cos_y + z_rot * sin_y
    z_final = -x * sin_y + z_rot * cos_y  # Fixes depth rotation

    return x_final, y_rot, z_final

def generate_disk_bands(black_hole_radius, screen_size, rotation_angle, camera_tilt, camera_rotation):
    """Creates a rotating accretion disk with a corrected 3D perspective."""
    bands = []
    for i in range(NUM_BANDS):
        # Radial positioning with smooth gradients
        r = INNER_DISK * black_hole_radius + (i / NUM_BANDS) * (DISK_RADIUS - INNER_DISK) * black_hole_radius
        theta = np.linspace(0, 2 * np.pi, 500)  # Smooth curve
        x = r * np.cos(theta)
        y = np.sin(theta) * 0.2 * r  # Add small vertical height to avoid flatness
        z = r * np.sin(theta)

        # Apply rotation for swirling motion
        x, y, z = rotate_points_3d(x, y, z, 0, rotation_angle)

        # Apply 3D camera perspective
        x, y, z = rotate_points_3d(x, y, z, camera_tilt, camera_rotation)

        # Convert to screen space (adjust scale for depth perspective)
        scale_factor = screen_size / (12 * black_hole_radius)
        screen_x = screen_size // 2 + x * scale_factor
        screen_y = screen_size // 2 - y * scale_factor  # Proper vertical scaling

        # Doppler shifting effect
        velocity = np.sqrt(6.67430e-11 * 1.989e30 / r)
        inclination = np.arctan2(z, x)  # Array of angles

        # Apply Doppler shifting per point
        colors = doppler_shift_color((255, 90, 50), velocity, inclination)

        bands.append((screen_x, screen_y, colors, int(2 + (i / NUM_BANDS) * 6)))  # Band thickness varies slightly

    return bands

def draw_accretion_disk(screen, bands):
    """Draws the rotating accretion disk with 3D camera perspective."""
    for x, y, colors, thickness in sorted(bands, key=lambda b: np.mean(b[1])):  # Sort bands for proper depth rendering
        for i in range(len(x) - 1):
            pygame.draw.line(screen, tuple(colors[i]), (int(x[i]), int(y[i])), (int(x[i + 1]), int(y[i + 1])), thickness)
