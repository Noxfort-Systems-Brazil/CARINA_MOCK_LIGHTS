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
# File: tests/test_core.py
# Author: Gabriel Moraes
# Date: 2026-10-10

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from core.traffic_light import TrafficLight, LightState
from core.manager import TrafficLightManager

class TestTrafficLight(unittest.TestCase):
    def test_state_transition(self):
        light = TrafficLight(1)
        self.assertEqual(light.state, LightState.RED)
        light.next_state()
        self.assertEqual(light.state, LightState.GREEN)
        light.next_state()
        self.assertEqual(light.state, LightState.YELLOW)
        light.next_state()
        self.assertEqual(light.state, LightState.RED)

if __name__ == '__main__':
    unittest.main()
