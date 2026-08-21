import sys
import os
import uuid
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime

# HARDCODE the absolute path to physics_engine
PHYSICS_PATH = r"D:\celestialab\physics_engine\src"
if PHYSICS_PATH not in sys.path:
    sys.path.insert(0, PHYSICS_PATH)

# Now import directly from src
from core.body import CelestialBody
from physics.simulation import Simulation
from physics.forces.custom import AnyForce

class SimulationManager:
    """Manages all active simulations (Singleton)"""
    
    _instance = None
    _simulations: Dict[str, Dict] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def create(self, config: dict) -> str:
        sim_id = str(uuid.uuid4())
        
        sim = Simulation(
            dt=config.get('dt', 3600.0),
            integrator=config.get('integrator', 'verlet'),
            use_gravity=config.get('use_gravity', True)
        )
        
        self._simulations[sim_id] = {
            'id': sim_id,
            'name': config.get('name', f'Sim_{sim_id[:8]}'),
            'simulation': sim,
            'is_running': False,
            'created_at': datetime.now(),
            'forces': []
        }
        
        return sim_id
    
    def get(self, sim_id: str) -> Optional[Simulation]:
        data = self._simulations.get(sim_id)
        return data['simulation'] if data else None
    
    def list(self) -> List[Dict]:
        return [
            {
                'id': sid,
                'name': data['name'],
                'created_at': data['created_at'],
                'body_count': len(data['simulation'].bodies),
                'time': data['simulation'].time,
                'is_running': data['is_running']
            }
            for sid, data in self._simulations.items()
        ]
    
    def delete(self, sim_id: str) -> bool:
        if sim_id in self._simulations:
            del self._simulations[sim_id]
            return True
        return False
    
    def add_body(self, sim_id: str, data: dict) -> bool:
        sim = self.get(sim_id)
        if not sim:
            return False
        
        body = CelestialBody(
            name=data['name'],
            mass=data['mass'],
            position=np.array(data['position']),
            velocity=np.array(data['velocity']),
            radius=data.get('radius', 1.0),
            color=data.get('color', '#ffffff')
        )
        sim.add_body(body)
        return True
    
    def remove_body(self, sim_id: str, body_id: str) -> bool:
        sim = self.get(sim_id)
        if not sim:
            return False
        return sim.remove_body(body_id)
    
    def add_force(self, sim_id: str, data: dict) -> bool:
        sim = self.get(sim_id)
        if not sim:
            return False
        
        def force_func(bodies, time, **kwargs):
            import numpy as np
            forces = []
            for body in bodies:
                locals_dict = {
                    'position': body.position,
                    'velocity': body.velocity,
                    'mass': body.mass,
                    'time': time,
                    'np': np,
                    **data.get('params', {})
                }
                force = eval(data['force_function'], {"__builtins__": {}}, locals_dict)
                forces.append(np.array(force))
            return forces
        
        force = AnyForce(force_func, name=data['name'], params=data.get('params', {}))
        sim.add_force(force)
        self._simulations[sim_id]['forces'].append(force)
        return True
    
    def start(self, sim_id: str) -> bool:
        data = self._simulations.get(sim_id)
        if not data:
            return False
        data['is_running'] = True
        return True
    
    def stop(self, sim_id: str) -> bool:
        data = self._simulations.get(sim_id)
        if not data:
            return False
        data['is_running'] = False
        return True
    
    def step(self, sim_id: str, steps: int = 1) -> bool:
        data = self._simulations.get(sim_id)
        if not data or not data['is_running']:
            return False
        data['simulation'].run(steps)
        return True
    
    def clear(self, sim_id: str) -> bool:
        sim = self.get(sim_id)
        if not sim:
            return False
        sim.clear_bodies()
        return True
    
    def get_state(self, sim_id: str) -> Optional[Dict]:
        data = self._simulations.get(sim_id)
        if not data:
            return None
        
        sim = data['simulation']
        state = sim.get_state()
        state['id'] = sim_id
        state['name'] = data['name']
        state['is_running'] = data['is_running']
        state['forces'] = [
            {'name': f.name, 'type': f.__class__.__name__}
            for f in data['forces']
        ]
        return state