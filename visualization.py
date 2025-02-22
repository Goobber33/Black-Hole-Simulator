import matplotlib.pyplot as plt
import numpy as np
from ray_tracing import compute_light_path, schwarzschild_radius

r_s = schwarzschild_radius(1.989e30)
r_vals, phi_vals = compute_light_path()

# Convert to Cartesian coordinates
x_vals = r_vals * np.cos(phi_vals)
y_vals = r_vals * np.sin(phi_vals)

# Plot light bending around the black hole
plt.figure(figsize=(6,6))
plt.plot(x_vals, y_vals, label="Light Path")
plt.scatter(0, 0, color="black", s=200, label="Black Hole")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()
plt.title("Simulated Light Bending Around a Black Hole")
plt.show()
