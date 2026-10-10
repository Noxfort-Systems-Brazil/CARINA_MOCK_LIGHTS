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
# File: server/utmc_handlers.py
# Author: Gabriel Moraes
# Date: 2026-10-10

from typing import List, Callable, Dict
from core.traffic_light import TrafficLight, LightState
import logging
import os

_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from server.utmc_logger import _conn_logger, _cmd_logger, log_colors

try:
    from pysnmp.proto.api import v2c
except ImportError:
    v2c = None

class OIDHandlerRegistry:
    def __init__(self):
        self._set_handlers: Dict[str, Callable] = {}
        self._get_handlers: Dict[str, Callable] = {}

    def register_set(self, pattern: str, handler: Callable):
        self._set_handlers[pattern] = handler

    def register_get(self, pattern: str, handler: Callable):
        self._get_handlers[pattern] = handler

    def handle_set(self, oid_str: str, val_int: int, junction_id: str, lights: List[TrafficLight]):
        for pattern, handler in self._set_handlers.items():
            if pattern in oid_str:
                handler(val_int, junction_id, lights)
                return True
        return False

    def handle_get(self, oid_str: str, junction_id: str, lights: List[TrafficLight]):
        for pattern, handler in self._get_handlers.items():
            if pattern in oid_str:
                return handler(junction_id, lights)
        # Default fallback: return None to indicate the OID is not handled
        return None

registry = OIDHandlerRegistry()

# Protocol registry (maps junction_id to its active protocol: "NTCIP 1202" or "UTMC2")
junction_protocols = {}

# SET Helpers
def _get_phase_idx_by_stage_mask(junction_id: str, val_int: int) -> int:
    try:
        from server.api import manager
        junction = manager.junctions.get(junction_id)
        if not junction or not hasattr(junction, 'green_stages') or not junction.green_stages:
            return None
        
        stage_idx = -1
        # UTMC2 stage bitmask (1 << stage_idx)
        for j in range(len(junction.green_stages)):
            if val_int & (1 << j):
                stage_idx = j
                break
                    
        if stage_idx != -1 and stage_idx < len(junction.green_stages):
            return junction.green_stages[stage_idx]
    except Exception as e:
        print(f"Error mapping stage mask to phase index: {e}")
    return None

def _get_phase_state_by_stage_mask(junction_id: str, val_int: int) -> str:
    try:
        from server.api import manager
        junction = manager.junctions.get(junction_id)
        if not junction:
            return None
        phase_idx = _get_phase_idx_by_stage_mask(junction_id, val_int)
        if phase_idx is not None and phase_idx < len(junction.data.phases):
            return junction.data.phases[phase_idx].state
    except Exception as e:
        print(f"Error mapping stage mask to phase state: {e}")
    return None

def _apply_state_string(state_str: str, lights: List[TrafficLight]):
    for i, char in enumerate(state_str):
        if i < len(lights):
            char = char.lower()
            if char in ('g', 'G'):
                lights[i].set_state(LightState.GREEN)
            elif char in ('y', 'Y', 'u'):
                lights[i].set_state(LightState.YELLOW)
            else:
                lights[i].set_state(LightState.RED)

# SET Handlers
def handle_hold(val_int: int, junction_id: str, lights: List[TrafficLight]):
    _conn_logger.info(f"UTMC2 COMMAND: HOLD mask={val_int}")
    msg = f"[Junction {junction_id}] UTMC2 COMMAND: HOLD mask={val_int} (Binary: {bin(val_int)})"
    print(msg)
    _cmd_logger.info(msg)
    
    # Log the command state in SUMO format
    log_colors("HOLD", val_int, junction_id)
    
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction:
        return
        
    if getattr(junction, 'transition_lock', False):
        _conn_logger.info(f"[Junction {junction_id}] Received HOLD command mask={val_int} during active transition lock.")
        
    if val_int == 0:
        junction.set_target_phase(-1)
    else:
        phase_idx = _get_phase_idx_by_stage_mask(junction_id, val_int)
        if phase_idx is not None:
            junction.set_target_phase(phase_idx)

def handle_force_off(val_int: int, junction_id: str, lights: List[TrafficLight]):
    _conn_logger.info(f"UTMC2 COMMAND: FORCE_OFF mask={val_int}")
    msg = f"[Junction {junction_id}] UTMC2 COMMAND: FORCE_OFF mask={val_int} (Binary: {bin(val_int)})"
    print(msg)
    _cmd_logger.info(msg)
    
    # Log the command state in SUMO format (transitions to clearance/all-red)
    log_colors("FORCE_OFF", 0, junction_id)
    
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction:
        return
        
    if getattr(junction, 'transition_lock', False):
        _conn_logger.info(f"[Junction {junction_id}] Received FORCE_OFF command mask={val_int} during active transition lock.")
        
    # FORCE_OFF terminates current phase, requesting transition to clearance (all-red)
    junction.set_target_phase(-1)

def handle_omit(val_int: int, junction_id: str, lights: List[TrafficLight]):
    _conn_logger.info(f"UTMC2 COMMAND: OMIT mask={val_int}")
    msg = f"[Junction {junction_id}] UTMC2 COMMAND: OMIT mask={val_int} (Binary: {bin(val_int)})"
    print(msg)
    _cmd_logger.info(msg)
    
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction:
        return
        
    if getattr(junction, 'transition_lock', False):
        _conn_logger.info(f"[Junction {junction_id}] Received OMIT command mask={val_int} during active transition lock.")
        
    # OMIT blocks a stage, we can log it here. In our simple simulation we just proceed.

def handle_extend(val_int: int, junction_id: str, lights: List[TrafficLight]):
    msg = f"[Junction {junction_id}] UTMC2 COMMAND: EXTEND mask={val_int} (Binary: {bin(val_int)})"
    print(msg)
    _cmd_logger.info(msg)

def handle_demand(val_int: int, junction_id: str, lights: List[TrafficLight]):
    msg = f"[Junction {junction_id}] UTMC2 COMMAND: DEMAND mask={val_int} (Binary: {bin(val_int)})"
    print(msg)
    _cmd_logger.info(msg)

def handle_flash(val_int: int, junction_id: str, lights: List[TrafficLight]):
    _conn_logger.info(f"SNMP COMMAND: FLASH val={val_int}")
    msg = f"[Junction {junction_id}] SNMP COMMAND: FLASH val={val_int}"
    print(msg)
    _cmd_logger.info(msg)
    
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction:
        return
    
    log_colors("FLASH", val_int, junction_id)
    
    if val_int == 1:
        junction.override_state = "ALERT"
    else:
        if junction.override_state == "ALERT":
            junction.override_state = "NORMAL"
            import time
            if (time.time() - junction.last_utmc_activity) < 10.0:
                state_target = junction.data.phases[junction.current_phase_idx].state if junction.current_phase_idx >= 0 else 'r' * len(junction.lights)
                junction._apply_phase(state_target)

def handle_dark(val_int: int, junction_id: str, lights: List[TrafficLight]):
    _conn_logger.info(f"SNMP COMMAND: DARK val={val_int}")
    msg = f"[Junction {junction_id}] SNMP COMMAND: DARK val={val_int}"
    print(msg)
    _cmd_logger.info(msg)
    
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction:
        return
        
    log_colors("DARK", val_int, junction_id)
    
    if val_int == 1:
        junction.override_state = "OFF"
    else:
        if junction.override_state == "OFF":
            junction.override_state = "NORMAL"
            import time
            if (time.time() - junction.last_utmc_activity) < 10.0:
                state_target = junction.data.phases[junction.current_phase_idx].state if junction.current_phase_idx >= 0 else 'r' * len(junction.lights)
                junction._apply_phase(state_target)

# UTMC2 stage control OIDs registry
registry.register_set(".2825.4.2.1.1.4.1.2.1", handle_hold)
registry.register_set(".2825.4.2.1.1.4.1.3.1", handle_force_off)
registry.register_set(".2825.4.2.1.1.4.1.7.1", handle_omit)
registry.register_set(".2825.4.2.1.1.4.1.6.1", handle_extend)
registry.register_set(".2825.4.2.1.1.4.1.5.1", handle_demand)
registry.register_set(".2825.4.2.1.1.2.1.255.1", handle_flash)
registry.register_set(".1206.4.2.1.1.2.1.255.1", handle_flash)
registry.register_set(".2825.4.2.1.1.2.1.254.1", handle_dark)
registry.register_set(".1206.4.2.1.1.2.1.254.1", handle_dark)

# Protocol Discovery Handler
def handle_get_sysdescr(junction_id: str, lights: List[TrafficLight]):
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    val = junction.sys_descr if junction and hasattr(junction, 'sys_descr') else "CARINA UTMC2 Mock Traffic Controller"
    return v2c.OctetString(val) if v2c else val

registry.register_get("1.3.6.1.2.1.1.1.0", handle_get_sysdescr)
registry.register_get(".1.3.6.1.2.1.1.1.0", handle_get_sysdescr)

# GET Handlers
def handle_get_active(junction_id: str, lights: List[TrafficLight]):
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction or not hasattr(junction, 'green_stages'):
        return v2c.Integer32(0) if v2c else 0
    
    if getattr(junction, 'transition_state', 'GREEN') != 'GREEN':
        return v2c.Integer32(0) if v2c else 0
        
    curr_phase = getattr(junction, 'current_phase_idx', 0)
    if curr_phase in junction.green_stages:
        stage_idx = junction.green_stages.index(curr_phase)
        val = 1 << stage_idx
        return v2c.Integer32(val) if v2c else val
    return v2c.Integer32(0) if v2c else 0

def handle_get_leaving(junction_id: str, lights: List[TrafficLight]):
    from server.api import manager
    junction = manager.junctions.get(junction_id)
    if not junction or not hasattr(junction, 'green_stages'):
        return v2c.Integer32(0) if v2c else 0
        
    if getattr(junction, 'transition_state', 'GREEN') == 'YELLOW':
        curr_phase = getattr(junction, 'current_phase_idx', 0)
        if curr_phase in junction.green_stages:
            stage_idx = junction.green_stages.index(curr_phase)
            val = 1 << stage_idx
            return v2c.Integer32(val) if v2c else val
    return v2c.Integer32(0) if v2c else 0

def handle_get_ped_demand(junction_id: str, lights: List[TrafficLight]):
    return v2c.Integer32(0) if v2c else 0

def handle_get_demand(junction_id: str, lights: List[TrafficLight]):
    # Returns 255 by default to let Carina know vehicles are waiting, triggering phase changes.
    return v2c.Integer32(255) if v2c else 255

# UTMC2 telemetry OIDs registry
registry.register_get(".2825.4.2.1.1.4.1.4.1", handle_get_active)
registry.register_get(".2825.4.2.1.1.4.1.8.1", handle_get_leaving)
registry.register_get(".2825.4.2.1.1.4.1.9.1", handle_get_ped_demand)
registry.register_get(".2825.4.2.1.1.4.1.5.1", handle_get_demand)
