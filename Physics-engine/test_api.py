# test_api.py
import requests
import json
import time

# ============================================
# 1. CREATE NEW SIMULATION (GET NEW ID)
# ============================================
print("1. Creating new simulation...")
create_data = {
    "name": "Solar System Test",
    "dt": 3600,
    "integrator": "verlet",
    "use_gravity": True
}

response = requests.post(
    "http://localhost:8000/api/v1/simulations",
    json=create_data
)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()

result = response.json()
SIM_ID = result['id']
print(f"   Simulation created with ID: {SIM_ID}")

# ============================================
# 2. ADD SUN
# ============================================
print("\n2. Adding Sun...")
sun = {
    "name": "Sun",
    "mass": 1.989e30,
    "position": [0, 0, 0],
    "velocity": [0, 0, 0],
    "radius": 6.96e8,
    "color": "#FDB813"
}

response = requests.post(
    f"http://localhost:8000/api/v1/simulations/{SIM_ID}/bodies",
    json=sun
)
print("   Sun added:", response.json())

# ============================================
# 3. ADD EARTH
# ============================================
print("\n3. Adding Earth...")
earth = {
    "name": "Earth",
    "mass": 5.972e24,
    "position": [1.496e11, 0, 0],
    "velocity": [0, 2.978e4, 0],
    "radius": 6.37e6,
    "color": "#4B9CD3"
}

response = requests.post(
    f"http://localhost:8000/api/v1/simulations/{SIM_ID}/bodies",
    json=earth
)
print("   Earth added:", response.json())

# ============================================
# 4. GET STATE
# ============================================
print("\n4. Getting state...")
response = requests.get(f"http://localhost:8000/api/v1/simulations/{SIM_ID}")
state = response.json()

print(f"   Name: {state.get('name')}")
print(f"   Time: {state.get('time')}")
print(f"   Bodies: {len(state.get('bodies', []))}")

for body in state.get('bodies', []):
    print(f"   - {body.get('name')}: {body.get('position')}")

# ============================================
# 5. START SIMULATION
# ============================================
print("\n5. Starting simulation...")
response = requests.post(
    f"http://localhost:8000/api/v1/simulations/{SIM_ID}/start"
)
print("   Start:", response.json())

# ============================================
# 6. RUN 100 STEPS
# ============================================
print("\n6. Running 100 steps...")
response = requests.post(
    f"http://localhost:8000/api/v1/simulations/{SIM_ID}/step",
    params={"steps": 100}
)
print("   Step result:", response.json())

# ============================================
# 7. GET STATE AFTER STEPS
# ============================================
print("\n7. State after 100 steps:")
response = requests.get(f"http://localhost:8000/api/v1/simulations/{SIM_ID}")
state = response.json()

if state.get('time') is not None:
    print(f"   Time: {state['time']:.0f} seconds")
else:
    print("   Time: None")

print(f"   Bodies: {len(state.get('bodies', []))}")

for body in state.get('bodies', []):
    pos = body.get('position', [0, 0, 0])
    print(f"   - {body.get('name')}: [{pos[0]/1e9:.2f}, {pos[1]/1e9:.2f}, {pos[2]/1e9:.2f}] million km")

# ============================================
# 8. RUN MORE
# ============================================
print("\n8. Running 1000 more steps...")
response = requests.post(
    f"http://localhost:8000/api/v1/simulations/{SIM_ID}/step",
    params={"steps": 1000}
)
print("   Done")

# ============================================
# 9. FINAL STATE
# ============================================
print("\n9. Final state:")
response = requests.get(f"http://localhost:8000/api/v1/simulations/{SIM_ID}")
state = response.json()

if state.get('time') is not None:
    print(f"   Time: {state['time']:.0f} seconds ({state['time']/365.25/24/3600:.2f} years)")
else:
    print("   Time: None")

energy = state.get('total_energy', {})
print(f"   Energy: {energy.get('total', 0):.2e} J")

for body in state.get('bodies', []):
    pos = body.get('position', [0, 0, 0])
    print(f"   - {body.get('name')}: [{pos[0]/1e9:.2f}, {pos[1]/1e9:.2f}] million km")

print(f"\n✅ Test complete! Simulation ID: {SIM_ID}")