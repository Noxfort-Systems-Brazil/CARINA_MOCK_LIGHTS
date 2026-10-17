# CARINA Mock Lights - SUMO Traffic Light Simulation & UTMC2/SNMP Server
# Copyright (C) 2026 Noxfort Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# File: server/api.py
# Author: Gabriel Moraes
# Date: October 2026

import sys
import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import time

from core.manager import TrafficLightManager
from core.traffic_light import LightState, LightObserver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = TrafficLightManager(base_port=8080)

# Store connected websockets
active_connections = []

# Store the main event loop to safely schedule tasks from background threads
main_loop = None

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()
    print("Captured main_loop!")

class WSObserver(LightObserver):
    def on_state_change(self, junction_id: str, light_id: int, state: LightState):
        msg = {
            "type": "state_change",
            "junction_id": junction_id,
            "light_id": light_id,
            "state": state.name
        }
        print(f"State change: {junction_id} L{light_id} -> {state.name} | Active WS: {len(active_connections)}")
        if main_loop and not main_loop.is_closed():
            for conn in active_connections:
                asyncio.run_coroutine_threadsafe(conn.send_json(msg), main_loop)

manager.add_observer(WSObserver())

def status_observer(junction_id: str, connected: bool):
    msg = {
        "type": "status_change",
        "junction_id": junction_id,
        "connected": connected
    }
    if main_loop and not main_loop.is_closed():
        for conn in active_connections:
            asyncio.run_coroutine_threadsafe(conn.send_json(msg), main_loop)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global main_loop
    if main_loop is None:
        main_loop = asyncio.get_running_loop()
        print(f"Captured main_loop from WS! {main_loop}")
        
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

class LoadRequest(BaseModel):
    file_path: str

@app.post("/api/load")
async def load_network(req: LoadRequest):
    try:
        manager.load_sumo_network(req.file_path)
        # Register status observers for new junctions
        for junc in manager.junctions.values():
            junc.add_status_observer(status_observer)
        
        return {"status": "success", "message": "Network loaded successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/junctions")
async def get_junctions():
    junctions = []
    for junc in manager.get_junction_list():
        junctions.append({
            "id": junc.id,
            "utmc_port": junc.utmc_port,
            "utmc_address": junc.utmc_server.get_utmc_info(),
            "brand": getattr(junc, 'brand', 'Não informado'),
            "model": getattr(junc, 'model', 'Não informado'),
            "lights": [
                {"id": l.id, "state": l.state.name, "label": l.label} for l in junc.lights
            ],
            "failure": junc.utmc_server.simulate_failure,
            "disable_fixed_plans": junc.disable_fixed_plans,
            "connected": (time.time() - junc.last_utmc_activity) < 10.0 if hasattr(junc, 'last_utmc_activity') else False,
            "protocol": getattr(junc, 'protocol', 'UTMC2')
        })
    return {"junctions": junctions}

class ToggleRequest(BaseModel):
    state: bool

class ProtocolRequest(BaseModel):
    protocol: str

@app.post("/api/junctions/{junction_id}/failure")
async def toggle_failure(junction_id: str, req: ToggleRequest):
    if junction_id in manager.junctions:
        manager.junctions[junction_id].set_failure(req.state)
        return {"status": "success"}
    return {"status": "error", "message": "Junction not found"}

@app.post("/api/junctions/{junction_id}/fixed-plans")
async def toggle_fixed_plans(junction_id: str, req: ToggleRequest):
    if junction_id in manager.junctions:
        manager.junctions[junction_id].toggle_fixed_plans(req.state)
        return {"status": "success"}
    return {"status": "error", "message": "Junction not found"}

class ErrorRequest(BaseModel):
    category: str = "HARDWARE"

@app.post("/api/junctions/{junction_id}/simulate-error")
async def simulate_error(junction_id: str, req: ErrorRequest = None):
    from core.manager import mock_logger
    category = req.category if req else "HARDWARE"
    mock_logger.info(f"[HTTP POST API] Received /simulate-error for Junction ID '{junction_id}' with category='{category}'")
    
    if junction_id in manager.junctions:
        error_info = manager.junctions[junction_id].send_simulated_error(category=category)
        mock_logger.info(f"[HTTP API SUCCESS] Error '{error_info.get('name')}' generated for Junction {junction_id}")
        return {"status": "success", "error_info": error_info}
    
    available_keys = list(manager.junctions.keys())
    mock_logger.warning(f"[HTTP API ERROR] Junction ID '{junction_id}' not found in active junctions. Available keys: {available_keys}")
    return {"status": "error", "message": f"Junction {junction_id} not found"}

@app.post("/api/junctions/{junction_id}/protocol")
async def set_junction_protocol(junction_id: str, req: ProtocolRequest):
    return {"status": "success"}

def run_server():
    # Changed host from "127.0.0.1" to "0.0.0.0" to allow external connections
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()