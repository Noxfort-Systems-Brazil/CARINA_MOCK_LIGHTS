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
# File: tests/test_parser.py
# Author: Gabriel Moraes
# Date: 2026-10-10

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.sumo_parser import SumoNetParser

def test_refined_parser():
    file_path = os.path.join(os.path.dirname(__file__), "mock_map.net.xml")
    
    # Create mock XML
    with open(file_path, "w") as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<net>
    <tlLogic id="J1" type="static" programID="0" offset="0">
        <phase duration="42" state="GggrrrGggrrr"/>
        <phase duration="3"  state="yyyrrryyyrrr"/>
    </tlLogic>
    <tlLogic id="J2" type="static" programID="0" offset="0">
        <phase duration="31" state="GGggrrrr"/>
    </tlLogic>
</net>
''')
    
    try:
        junctions = SumoNetParser.parse(file_path)
        
        print(f"Parsed {len(junctions)} junctions.")
        results = {j.id: j.num_lights for j in junctions}
        
        print(f"Results: {results}")
        
        assert results["J1"] == 12
        assert results["J2"] == 8
        
        print("Refined parser test passed!")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    test_refined_parser()
