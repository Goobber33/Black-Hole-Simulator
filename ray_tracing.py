from scipy.integrate import solve_ivp
import numpy as np

G = 6.67430e-11
c = 3.0e8
M = 1.989e30  # Black hole mass (Sun mass for now)

def schwarzschild_radius(M):
    return 2 * G * M / c**2

r_s = schwarzschild_radius(M)

# Define geodesic equations (light bending path)
def geodesic(t, y):
    r, phi, dr_dt, dphi_dt = y
    d2r_dt2 = -(G * M / r**2) + (r * dphi_dt**2)
    d2phi_dt2 = -2 * dr_dt * dphi_dt / r
    return [dr_dt, dphi_dt, d2r_dt2, d2phi_dt2]

# Function to compute light paths
def compute_light_path(r0=5*r_s, dr_dt0=-c, dphi_dt0=0.001):
    y0 = [r0, 0, dr_dt0, dphi_dt0]
    t_span = [0, 100]
    solution = solve_ivp(geodesic, t_span, y0, t_eval=np.linspace(0, 100, 1000))
    return solution.y
