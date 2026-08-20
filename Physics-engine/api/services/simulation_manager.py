# api/services/simulation_manager.py
import uuid
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.physics.forces.custom import AnyForce
from src.physics.forces.base import Force


class SimulationManager:
    """
    Manages all active simulations
    Singleton pattern
    """
    
    _instance = None
    _simulations: Dict[str, Dict] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def create_simulation(self, config: dict) -> str:
        """Create a new simulation"""
        sim_id = str(uuid.uuid4())
        
        sim = Simulation(
            dt=config.get('dt', 3600.0),
            integrator=config.get('integrator', 'verlet'),
            use_gravity=config.get('use_gravity', True)
        )
        
        self._simulations[sim_id] = {
            'id': sim_id,
            'name': config.get('name', f'Simulation_{sim_id[:8]}'),
            'simulation': sim,
            'is_running': False,
            'created_at': datetime.now(),
            'forces': []
        }
        
        return sim_id
    
    def get_simulation(self, sim_id: str) -> Optional[Simulation]:
        """Get simulation instance"""
        sim_data = self._simulations.get(sim_id)
        if sim_data:
            return sim_data['simulation']
        return None
    
    def get_simulations(self) -> List[Dict]:
        """List all simulations"""
        return [
            {
                'id': sim_id,
                'name': data['name'],
                'created_at': data['created_at'],
                'body_count': len(data['simulation'].bodies),
                'time': data['simulation'].time,
                'is_running': data['is_running']
            }
            for sim_id, data in self._simulations.items()
        ]
    
    def delete_simulation(self, sim_id: str) -> bool:
        """Delete a simulation"""
        if sim_id in self._simulations:
            del self._simulations[sim_id]
            return True
        return False
    
    def add_body(self, sim_id: str, body_data: dict) -> bool:
        """Add body to simulation"""
        sim = self.get_simulation(sim_id)
        if not sim:
            return False
        
        body = CelestialBody(
            name=body_data['name'],
            mass=body_data['mass'],
            position=np.array(body_data['position']),
            velocity=np.array(body_data['velocity']),
            radius=body_data.get('radius', 1.0),
            color=body_data.get('color', '#ffffff')
        )
        
        sim.add_body(body)
        return True
    
    def remove_body(self, sim_id: str, body_id: str) -> bool:
        """Remove body from simulation"""
        sim = self.get_simulation(sim_id)
        if not sim:
            return False
        return sim.remove_body(body_id)
    
    def add_force(self, sim_id: str, force_data: dict) -> bool:
        """Add custom force to simulation"""
        sim = self.get_simulation(sim_id)
        if not sim:
            return False
        
        # Parse force function from string
        force_function = self._parse_force_function(
            force_data['force_function'],
            force_data.get('params', {})
        )
        
        force = AnyForce(
            force_function=force_function,
            name=force_data['name'],
            params=force_data.get('params', {}),
            description=force_data.get('description', '')
        )
        
        sim.add_force(force)
        self._simulations[sim_id]['forces'].append(force)
        return True
    
    def _parse_force_function(self, func_str: str, params: dict):
        """
        Parse user-defined force function
        Supports expressions like: "a * position + b * velocity"
        """
        import numpy as np
        from typing import List
        
        def force_func(bodies, time, **kwargs):
            forces = []
            for body in bodies:
                # Create local variables for evaluation
                locals_dict = {
                    'position': body.position,
                    'velocity': body.velocity,
                    'mass': body.mass,
                    'time': time,
                    'np': np,
                    **params
                }
                # Evaluate the function string
                force = eval(func_str, {"__builtins__": {}}, locals_dict)
                forces.append(np.array(force))
            return forces
        
        return force_func
    
    def start_simulation(self, sim_id: str) -> bool:
        """Start the simulation"""
        sim_data = self._simulations.get(sim_id)
        if not sim_data:
            return False
        sim_data['is_running'] = True
        return True
    
    def stop_simulation(self, sim_id: str) -> bool:
        """Stop the simulation"""
        sim_data = self._simulations.get(sim_id)
        if not sim_data:
            return False
        sim_data['is_running'] = False
        return True
    
    def step_simulation(self, sim_id: str, steps: int = 1) -> bool:
        """Execute simulation steps"""
        sim_data = self._simulations.get(sim_id)
        if not sim_data or not sim_data['is_running']:
            return False
        
        sim = sim_data['simulation']
        sim.run(steps)
        return True
    
    def get_state(self, sim_id: str) -> Optional[Dict]:
        """Get simulation state"""
        sim_data = self._simulations.get(sim_id)
        if not sim_data:
            return None
        
        sim = sim_data['simulation']
        state = sim.get_state()
        
        state['id'] = sim_id
        state['name'] = sim_data['name']
        state['is_running'] = sim_data['is_running']
        state['forces'] = [
            {'name': f.name, 'type': f.__class__.__name__}
            for f in sim_data['forces']
        ]
        
        return state
    
    def clear_simulation(self, sim_id: str) -> bool:
        """Clear all bodies from simulation"""
        sim = self.get_simulation(sim_id)
        if not sim:
            return False
        sim.clear_bodies()
        return True