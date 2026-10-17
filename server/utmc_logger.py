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
# File: server/utmc_logger.py
# Author: Gabriel Moraes
# Date: October 2026

import logging
import os

_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_carina_output_dir() -> str:
    """Returns the base output directory (~/Documentos/Carina or ~/Documents/Carina)."""
    import subprocess
    documents_dir = None
    try:
        output = subprocess.check_output(['xdg-user-dir', 'DOCUMENTS'], stderr=subprocess.DEVNULL)
        documents_dir = output.decode('utf-8').strip()
    except Exception:
        pass
    if not documents_dir or not os.path.isdir(documents_dir):
        for candidate in [os.path.expanduser("~/Documentos"), os.path.expanduser("~/Documents"), os.path.expanduser("~")]:
            if os.path.isdir(candidate):
                documents_dir = candidate
                break
    carina_dir = os.path.join(documents_dir or os.path.expanduser("~"), "Carina")
    return carina_dir

def get_connection_logger():
    logger = logging.getLogger("connections")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_file = os.path.join(_root_dir, "connections.log")
        fh = logging.FileHandler(log_file)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)
    return logger

def get_command_logger():
    logger = logging.getLogger("commands")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_dir = os.path.join(get_carina_output_dir(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        cmd_log_file = os.path.join(log_dir, "commands.log")
        cfh = logging.FileHandler(cmd_log_file)
        cfh.setFormatter(logging.Formatter('%(asctime)s - [Junction] - %(message)s'))
        logger.addHandler(cfh)
    return logger

_conn_logger = get_connection_logger()
_cmd_logger = get_command_logger()

def log_colors(cmd_name: str, val_int: int, junction_id: str):
    try:
        from server.api import manager
        junction = manager.junctions.get(junction_id)
        if not junction:
            return
        
        stage_num = None
        state_str = None
        
        if cmd_name == "FLASH":
            if val_int == 1:
                stage_num = "piscante"
                state_str = 'y' * len(junction.lights)
            else:
                stage_num = "normal"
                phase_idx = junction.current_phase_idx
                if phase_idx >= 0 and phase_idx < len(junction.data.phases):
                    state_str = junction.data.phases[phase_idx].state
                else:
                    state_str = 'r' * len(junction.lights)
        elif cmd_name == "DARK":
            if val_int == 1:
                stage_num = "desligado"
                state_str = 'o' * len(junction.lights)
            else:
                stage_num = "normal"
                phase_idx = junction.current_phase_idx
                if phase_idx >= 0 and phase_idx < len(junction.data.phases):
                    state_str = junction.data.phases[phase_idx].state
                else:
                    state_str = 'r' * len(junction.lights)
        elif val_int == 0:
            stage_num = 0
            state_str = 'r' * len(junction.lights)
        else:
            for j in range(len(junction.green_stages)):
                if val_int & (1 << j):
                    stage_idx = j
                    phase_idx = junction.green_stages[stage_idx]
                    if phase_idx < len(junction.data.phases):
                        stage_num = stage_idx + 1
                        state_str = junction.data.phases[phase_idx].state
                    break
        
        if stage_num is not None and state_str is not None:
            colors_log_file = os.path.join(_root_dir, "colors.log")
            line = f"estágio {stage_num}: {state_str}\n"
            with open(colors_log_file, "a", encoding="utf-8") as f:
                f.write(line)
    except Exception as e:
        print(f"Error logging to colors.log: {e}")