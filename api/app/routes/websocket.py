# api/app/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from ..services.simulation_manager import SimulationManager

router = APIRouter()
manager = SimulationManager()


@router.websocket("/ws/simulation/{sim_id}")
async def websocket_endpoint(websocket: WebSocket, sim_id: str):
    await websocket.accept()
    
    try:
        while True:
            data = manager._simulations.get(sim_id)
            if not data:
                await websocket.send_json({"error": "Simulation not found"})
                break
            
            if data['is_running']:
                data['simulation'].step()
                state = manager.get_state(sim_id)
                await websocket.send_json(state)
            
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {sim_id}")