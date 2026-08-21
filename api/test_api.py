# test_api.py
import requests
import json

BASE = "http://localhost:8000/api/v1"

print("=" * 50)
print("TESTING API")
print("=" * 50)

# 1. Create simulation
print("\n1. Creating simulation...")
r = requests.post(f"{BASE}/simulations", json={
    "name": "Solar System",
    "dt": 3600,
    "integrator": "verlet"
})
sim_id = r.json()['id']
print(f"   ID: {sim_id}")

# 2. Add Sun
print("\n2. Adding Sun...")
r = requests.post(f"{BASE}/simulations/{sim_id}/bodies", json={
    "name": "Sun",
    "mass": 1.989e30,
    "position": [0, 0, 0],
    "velocity": [0, 0, 0],
    "radius": 6.96e8,
    "color": "#FDB813"
})
print(f"   {r.json()}")

# 3. Add Earth
print("\n3. Adding Earth...")
r = requests.post(f"{BASE}/simulations/{sim_id}/bodies", json={
    "name": "Earth",
    "mass": 5.972e24,
    "position": [1.496e11, 0, 0],
    "velocity": [0, 2.978e4, 0],
    "radius": 6.37e6,
    "color": "#4B9CD3"
})
print(f"   {r.json()}")

# 4. Get state
print("\n4. Getting state...")
r = requests.get(f"{BASE}/simulations/{sim_id}")
state = r.json()
print(f"   Bodies: {len(state['bodies'])}")
for body in state['bodies']:
    print(f"   - {body['name']}")

# 5. Start
print("\n5. Starting...")
r = requests.post(f"{BASE}/simulations/{sim_id}/start")
print(f"   {r.json()}")

# 6. Run steps
print("\n6. Running 100 steps...")
r = requests.post(f"{BASE}/simulations/{sim_id}/step", params={"steps": 100})
print(f"   {r.json()}")

# 7. Final state
print("\n7. Final state...")
r = requests.get(f"{BASE}/simulations/{sim_id}")
state = r.json()
print(f"   Time: {state['time']:.0f}s")

print("\n" + "=" * 50)
print("✅ DONE!")
print("=" * 50)