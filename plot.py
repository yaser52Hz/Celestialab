import matplotlib.pyplot as plt

from backend.physics.body import Body
from backend.physics.forces.gravity import NewtonianGravity
from backend.physics.integrators.verlet import VelocityVerlet
from simulation import Simulation


AU = 1.496e11


# -------------------------
# Create bodies
# -------------------------

sun = Body(
    "Sun",
    1.989e30,
    [0, 0, 0],
    [0, 0, 0],
)

earth = Body(
    "Earth",
    5.972e24,
    [AU, 0, 0],
    [0, 29780, 0],
)


# -------------------------
# Create simulation
# -------------------------

simulation = Simulation(
    bodies=[sun, earth],
    forces=[NewtonianGravity()],
    integrator=VelocityVerlet(),
)


# -------------------------
# Run simulation
# -------------------------

dt = 3600  # seconds

for _ in range(8766):
    simulation.step(dt)


# -------------------------
# Get Earth trajectory
# -------------------------

trajectory = simulation.trajectory["Earth"]

positions = trajectory.position


# -------------------------
# Convert to AU
# -------------------------

x = [position[0] / AU for position in positions]
y = [position[1] / AU for position in positions]


# -------------------------
# Plot
# -------------------------

plt.figure(figsize=(8, 8))

plt.plot(
    x,
    y,
    label="Earth trajectory",
)

plt.scatter(
    [0],
    [0],
    label="Sun",
)

plt.scatter(
    [x[0]],
    [y[0]],
    label="Initial position",
)

plt.scatter(
    [x[-1]],
    [y[-1]],
    label="Final position",
)

plt.xlabel("x [AU]")
plt.ylabel("y [AU]")

plt.title("Earth Orbit")

plt.axis("equal")
plt.grid()

plt.legend()

plt.show()