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
# File: core/traffic_light.py
# Author: Gabriel Moraes
# Date: 2026-10-10

from enum import Enum, auto
from typing import List, Protocol

class LightState(Enum):
    OFF = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class LightObserver(Protocol):
    def on_state_change(self, junction_id: str, light_id: int, state: LightState):
        ...

class TrafficLight:
    """Represents a single traffic light state machine for an O-D pair."""
    def __init__(self, light_id: int, junction_id: str = "", label: str = ""):
        self.id = light_id
        self.junction_id = junction_id
        self.label = label
        self.state = LightState.RED
        self._observers: List[LightObserver] = []

    def add_observer(self, observer: LightObserver):
        self._observers.append(observer)

    def set_state(self, new_state: LightState):
        if self.state != new_state:
            self.state = new_state
            self._notify_observers()

    def _notify_observers(self):
        for observer in self._observers:
            observer.on_state_change(self.junction_id, self.id, self.state)

    def next_state(self):
        """Transitions to the next logical state."""
        if self.state == LightState.RED:
            self.set_state(LightState.GREEN)
        elif self.state == LightState.GREEN:
            self.set_state(LightState.YELLOW)
        elif self.state == LightState.YELLOW:
            self.set_state(LightState.RED)

    def __str__(self):
        return f"Light {self.id}: {self.state.name}"
