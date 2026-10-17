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
# File: core/sumo_parser.py
# Author: Gabriel Moraes
# Date: October 2026

import gzip
import xml.etree.ElementTree as ET
from typing import List, Dict, Set, Tuple

class PhaseData:
    def __init__(self, duration: int, state: str):
        self.duration = duration
        self.state = state
    
    def __repr__(self):
        return f"Phase(duration={self.duration}, state={self.state})"

class JunctionData:
    def __init__(self, junction_id: str, phases: List[PhaseData], num_lights: int):
        self.id = junction_id
        self.phases = phases
        self.num_lights = num_lights

class SumoNetParser:
    """Parses SUMO .net.xml files to extract traffic light phases and states."""
    
    @staticmethod
    def parse(file_path: str) -> List[JunctionData]:
        try:
            if file_path.endswith('.gz'):
                with gzip.open(file_path, 'rb') as f:
                    tree = ET.parse(f)
            else:
                tree = ET.parse(file_path)
            
            root = tree.getroot()
            
            tl_logics = root.findall(".//tlLogic")
            results = []
            
            for tl in tl_logics:
                j_id = tl.get('id')
                phases = []
                for phase in tl.findall("phase"):
                    duration = int(float(phase.get('duration', '0')))
                    state = phase.get('state', '')
                    phases.append(PhaseData(duration, state))
                
                num_lights = len(phases[0].state) if phases else 0
                results.append(JunctionData(j_id, phases, num_lights))
                
            return results
        except Exception as e:
            print(f"Error parsing SUMO file: {e}")
            return []
