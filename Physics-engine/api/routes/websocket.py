# api/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio

from ..services.simulation_manager import SimulationManager

router = APIRouter()
manager = SimulationManager()


@router.websocket("/ws/simulation/{sim_id}")
async def websocket_endpoint(websocket: WebSocket, sim_id: str):
    """WebSocket endpoint for real-time simulation updates"""
    await websocket.accept()
    
    try:
        while True:
            # Check if simulation exists
            sim_data = manager._simulations.get(sim_id)
            if not sim_data:
                await websocket.send_json({
                    "error": "Simulation not found"
                })
                break
            
            # If running, execute one step and send state
            if sim_data['is_running']:
                sim_data['simulation'].step()
                state = manager.get_state(sim_id)
                await websocket.send_json(state)
            
            await asyncio.sleep(0.1)  # 10 FPS
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for simulation {sim_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")