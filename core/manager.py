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
# File: core/manager.py
# Author: Gabriel Moraes
# Date: 2026-10-10

import threading
import time
import sys
import os
import logging
from typing import List, Dict, Any
from core.traffic_light import TrafficLight, LightState, LightObserver
from core.sumo_parser import SumoNetParser, JunctionData
from server.utmc_server import UTMCServer

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
mock_log_file = os.path.join(log_dir, "mock_lights_events.log")

mock_logger = logging.getLogger("CARINA_MOCK_LIGHTS")
mock_logger.setLevel(logging.INFO)
if not mock_logger.handlers:
    file_handler = logging.FileHandler(mock_log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    mock_logger.addHandler(file_handler)

BRAZILIAN_CONTROLLER_PRESETS = [
    {"brand": "Dataprom", "model": "DP-2000", "descr": "Dataprom DP-2000 Traffic Light Controller UTMC2 v3.1"},
    {"brand": "Siemens", "model": "ST950", "descr": "Siemens ST950 UTMC Traffic Controller v4.2"},
    {"brand": "Digicon", "model": "CD-300", "descr": "Digicon CD-300 Smart Traffic Controller UTMC2"},
    {"brand": "Swarco", "model": "ITC-3", "descr": "Swarco ITC-3 UTMC2 Traffic Controller"},
    {"brand": "Dataprom", "model": "DP-SMART", "descr": "Dataprom DP-SMART Traffic Controller UTMC2"},
    {"brand": "Kapsch", "model": "EcoController", "descr": "Kapsch EcoController UTMC2 Traffic Light System"},
]

HARDWARE_ERRORS_POOL = [
    {
        "category": "HARDWARE",
        "type": "LAMP_FAILURE",
        "level": "CRITICAL",
        "oid": "1.3.6.1.4.1.2825.4.1.1",
        "name": "Falha de Lâmpada/LED",
        "message": "Falha no foco vermelho / LED queimado no grupo focal 2"
    },
    {
        "category": "HARDWARE",
        "type": "GREEN_CONFLICT",
        "level": "CRITICAL",
        "oid": "1.3.6.1.4.1.2825.4.1.2",
        "name": "Conflito de Verdes",
        "message": "Intervenção da placa de segurança: Conflito de fases verdes detectado"
    },
    {
        "category": "HARDWARE",
        "type": "DETECTOR_FAILURE",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.1.3",
        "name": "Falha de Sensor/Laço",
        "message": "Laço indutivo de presença com corte ou falha de sinal"
    },
    {
        "category": "HARDWARE",
        "type": "POWER_ALARM",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.1.4",
        "name": "Alerta de Energia",
        "message": "Oscilação de rede elétrica externa, operando em No-Break"
    },
    {
        "category": "HARDWARE",
        "type": "CABINET_DOOR",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.1.5",
        "name": "Alerta de Armário Aberto",
        "message": "Alerta de segurança: Porta do gabinete do controlador aberta"
    }
]

SOFTWARE_ERRORS_POOL = [
    {
        "category": "SOFTWARE",
        "type": "COMMAND_REJECTED",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.2.1",
        "name": "Comando Rejeitado pelo Firmware",
        "message": "Solicitação de transição rejeitada: Sequência de fases incompatível"
    },
    {
        "category": "SOFTWARE",
        "type": "SAFETY_TIME_VIOLATION",
        "level": "CRITICAL",
        "oid": "1.3.6.1.4.1.2825.4.2.2",
        "name": "Violação de Tempo de Segurança",
        "message": "Solicitação de alteração de fase negada por tempo mínimo de amarelo/interverde"
    },
    {
        "category": "SOFTWARE",
        "type": "RTC_DRIFT",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.2.3",
        "name": "Desincronização de Relógio (RTC)",
        "message": "Relógio interno do controlador desincronizado em relação ao tempo central NTP"
    },
    {
        "category": "SOFTWARE",
        "type": "PLAN_EXECUTION_ERROR",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.2.4",
        "name": "Erro na Tabela de Planos Locais",
        "message": "Falha na alternância de plano horário pré-programado na matriz local"
    },
    {
        "category": "SOFTWARE",
        "type": "QUEUE_OVERFLOW",
        "level": "WARNING",
        "oid": "1.3.6.1.4.1.2825.4.2.5",
        "name": "Estouro de Fila de Comunicação",
        "message": "Buffer de requisições SNMP temporariamente sobrecarregado pelo controlador"
    }
]

class Junction:
    """Represents a SUMO crossing with its OD-based signal groups and server."""
    def __init__(self, data: JunctionData, port: int):
        self.id = data.id
        self.data = data
        self.lights = [
            TrafficLight(i, junction_id=str(self.id), label=f"Link {i}") 
            for i in range(data.num_lights)
        ]
        # Assign realistic Brazilian controller brand and model
        preset_idx = abs(hash(str(self.id))) % len(BRAZILIAN_CONTROLLER_PRESETS)
        preset = BRAZILIAN_CONTROLLER_PRESETS[preset_idx]
        self.brand = preset["brand"]
        self.model = preset["model"]
        self.sys_descr = preset["descr"]

        # UTMC SNMP typically runs on port 161. In a mock with multiple junctions, we offset base_port
        # e.g., if HTTP port is 8080, UTMC port could be 1610 (offsetting 8080 to 1610 + index)
        # Here we will just use port - 8080 + 1610
        self.utmc_port = 1610 + (port - 8080)
        
        self.last_utmc_activity = 0.0
        self.utmc_server = UTMCServer(str(self.id), self.lights, self.utmc_port, on_activity=self._on_utmc_activity)
        self.port = port
        
        self._running = False
        self._thread = None
        self.status_observers = []
        self.disable_fixed_plans = False
        
        # Protocol configuration
        self.protocol = "UTMC2"
        self.override_state = "NORMAL"

        # Treat all phases as stages (no filtering)
        self.green_stages = list(range(len(self.data.phases)))

        # Remote control transition state machine
        self.current_phase_idx = 0
        self.target_phase_idx = 0
        self.transition_state = "GREEN"
        self.transition_timer = 0.0
        self.transition_lock = False
        self._yellow_lights = []

    def send_simulated_error(self, category: str = "HARDWARE", target_ip: str = "127.0.0.1", trap_port: int = 162) -> dict:
        """
        Sends a random simulated error (HARDWARE or SOFTWARE) excluding Watchdog and Config Corruption via SNMP Trap UDP packet to CARINA.
        """
        import random
        import socket
        
        cat_upper = str(category).upper()
        if cat_upper == "HARDWARE":
            pool = HARDWARE_ERRORS_POOL
        elif cat_upper == "SOFTWARE":
            pool = SOFTWARE_ERRORS_POOL
        else:
            pool = HARDWARE_ERRORS_POOL + SOFTWARE_ERRORS_POOL

        error_info = random.choice(pool)
        
        community = b"public"
        message_str = f"TRAP|{error_info['oid']}|{error_info['level']}|[{error_info['category']}] {error_info['name']}: {error_info['message']}".encode('utf-8')
        
        def pack_tlv(tag: int, value: bytes) -> bytes:
            length = len(value)
            if length < 128:
                len_bytes = bytes([length])
            else:
                len_bytes = bytes([0x81, length])
            return bytes([tag]) + len_bytes + value

        varbind = pack_tlv(0x30, pack_tlv(0x06, b"\x2b\x06\x01\x04\x01\x96\x09\x04\x01") + pack_tlv(0x04, message_str))
        varbind_seq = pack_tlv(0x30, varbind)
        pdu = pack_tlv(0xa7, pack_tlv(0x02, b"\x01") + pack_tlv(0x02, b"\x00") + pack_tlv(0x02, b"\x00") + varbind_seq)
        snmp_msg = pack_tlv(0x30, pack_tlv(0x02, b"\x01") + pack_tlv(0x04, community) + pdu)

        ports_to_send = [trap_port] if trap_port != 162 else [162, 1620]
        for p in ports_to_send:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(snmp_msg, (target_ip, p))
                sock.close()
                log_entry = f"[Junction {self.id}] [{error_info['category']}] SNMP TRAP DISPATCHED -> IP: {target_ip}:{p} | OID: {error_info['oid']} | Level: {error_info['level']} | Name: {error_info['name']} | Message: {error_info['message']}"
                print(log_entry)
                mock_logger.info(log_entry)
            except Exception as e:
                err_entry = f"[Junction {self.id}] Failed to send SNMP Trap to port {p}: {e}"
                print(err_entry)
                mock_logger.error(err_entry)

        return error_info

    def send_random_hardware_error(self, target_ip: str = "127.0.0.1", trap_port: int = 162) -> dict:
        return self.send_simulated_error(category="HARDWARE", target_ip=target_ip, trap_port=trap_port)




    def _on_utmc_activity(self):
        self.last_utmc_activity = time.time()

    def add_status_observer(self, observer):
        self.status_observers.append(observer)
        
    def _notify_status(self, connected: bool):
        for obs in self.status_observers:
            obs(self.id, connected)

    def set_target_phase(self, phase_idx: int):
        if phase_idx != self.target_phase_idx:
            self.target_phase_idx = phase_idx

    def _tick_remote_transition(self, dt: float):
        if self.transition_state == "GREEN":
            if self.target_phase_idx != self.current_phase_idx:
                # Initiate transition
                state_current = self.data.phases[self.current_phase_idx].state if self.current_phase_idx >= 0 else 'r' * len(self.lights)
                if self.target_phase_idx == -1:
                    state_target = 'r' * len(self.lights)
                else:
                    state_target = self.data.phases[self.target_phase_idx].state
                
                # Identify transitioning lights (Green to non-Green)
                self._yellow_lights = []
                for i in range(len(self.lights)):
                    char_curr = state_current[i].lower() if i < len(state_current) else 'r'
                    char_targ = state_target[i].lower() if i < len(state_target) else 'r'
                    if char_curr == 'g' and char_targ != 'g':
                        self._yellow_lights.append(i)
                
                if self._yellow_lights:
                    self.transition_state = "YELLOW"
                    self.transition_timer = 3.0  # 3 seconds yellow transition
                    self.transition_lock = True
                    for idx in self._yellow_lights:
                        if idx < len(self.lights):
                            self.lights[idx].set_state(LightState.YELLOW)
                    print(f"[Junction {self.id}] Safety Transition: GREEN -> YELLOW for lights {self._yellow_lights}")
                else:
                    # Direct to ALL_RED clearance if no yellow transition needed
                    self.transition_state = "ALL_RED"
                    self.transition_timer = 1.0  # 1 second clearance
                    self.transition_lock = True
                    for l in self.lights:
                        l.set_state(LightState.RED)
                    print(f"[Junction {self.id}] Safety Transition: Direct to ALL_RED clearance")
            
        elif self.transition_state == "YELLOW":
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.transition_state = "ALL_RED"
                self.transition_timer = 1.0  # 1 second clearance
                for idx in self._yellow_lights:
                    if idx < len(self.lights):
                        self.lights[idx].set_state(LightState.RED)
                print(f"[Junction {self.id}] Safety Transition: YELLOW -> ALL_RED clearance")
                
        elif self.transition_state == "ALL_RED":
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.transition_state = "GREEN"
                self.transition_lock = False
                self.current_phase_idx = self.target_phase_idx
                
                if self.current_phase_idx == -1:
                    for l in self.lights:
                        l.set_state(LightState.RED)
                    print(f"[Junction {self.id}] Safety Transition complete: ALL_RED held.")
                else:
                    state_target = self.data.phases[self.current_phase_idx].state
                    self._apply_phase(state_target)
                    print(f"[Junction {self.id}] Safety Transition complete: GREEN applied for phase {self.current_phase_idx} ({state_target})")

    def start(self):
        self.utmc_server.start()
        self._running = True
        self._thread = threading.Thread(target=self._run_phases, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        self.utmc_server.stop()

    def set_failure(self, state: bool):
        self.utmc_server.simulate_failure = state
        if state:
            # immediately pretend we lost connection so UI updates and simulator takes over
            self.last_utmc_activity = 0.0
            self._notify_status(False)

    def toggle_fixed_plans(self, state: bool):
        self.disable_fixed_plans = state
        if state:
            is_connected = (time.time() - self.last_utmc_activity) < 10.0
            if not is_connected:
                for light in self.lights:
                    light.set_state(LightState.OFF)

    def _apply_phase(self, state_str: str):
        for i, char in enumerate(state_str):
            if i < len(self.lights):
                char = char.lower()
                if char in ('g', 'G'):
                    self.lights[i].set_state(LightState.GREEN)
                elif char in ('y', 'Y', 'u'):
                    self.lights[i].set_state(LightState.YELLOW)
                else:
                    self.lights[i].set_state(LightState.RED)

    def _run_phases(self):
        try:
            was_connected = False
            while self._running:
                if self.override_state == "ALERT":
                    # Flashing yellow: toggle between YELLOW and OFF
                    current_blink = getattr(self, '_blink_toggle', False)
                    self._blink_toggle = not current_blink
                    target_state = LightState.YELLOW if self._blink_toggle else LightState.OFF
                    for light in self.lights:
                        light.set_state(target_state)
                    time.sleep(0.5)
                    continue
                elif self.override_state == "OFF":
                    for light in self.lights:
                        light.set_state(LightState.OFF)
                    time.sleep(0.5)
                    continue

                # Consider connected if activity in the last 10 seconds
                is_connected = (time.time() - self.last_utmc_activity) < 10.0
                
                if is_connected != was_connected:
                    self._notify_status(is_connected)
                    was_connected = is_connected
                    if is_connected:
                        self.transition_state = "GREEN"
                        self.transition_timer = 0.0
                        self.transition_lock = False
                        self._apply_phase(self.data.phases[self.current_phase_idx].state)

                if is_connected:
                    self._tick_remote_transition(0.1)
                    time.sleep(0.1)
                else:
                    if self.disable_fixed_plans:
                        # Keep all lights OFF while waiting for connection
                        for light in self.lights:
                            if light.state != LightState.OFF:
                                light.set_state(LightState.OFF)
                        time.sleep(1.0)
                        continue

                    if not self.data.phases:
                        time.sleep(1.0)
                        continue
                        
                    for phase in self.data.phases:
                        if not self._running or (time.time() - self.last_utmc_activity) < 10.0 or self.disable_fixed_plans:
                            break
                            
                        self._apply_phase(phase.state)
                        
                        # Sleep for phase duration in smaller steps to be responsive to UTMC2 interrupts
                        duration = phase.duration
                        elapsed = 0
                        while elapsed < duration and self._running and (time.time() - self.last_utmc_activity) >= 10.0 and not self.disable_fixed_plans:
                            time.sleep(0.5)
                            elapsed += 0.5
        except Exception as e:
            print(f"Error in Junction {self.id} thread: {e}")

class TrafficLightManager:
    """Manages all junctions and their servers."""
    def __init__(self, base_port: int = 8080):
        self.junctions: Dict[str, Junction] = {}
        self.base_port = base_port
        self._running = False
        self._thread = None
        self._observers: List[LightObserver] = []

    def add_observer(self, observer: LightObserver):
        self._observers.append(observer)
        # Re-attach to all lights in all junctions
        for junc in self.junctions.values():
            for light in junc.lights:
                light.add_observer(observer)

    def load_sumo_network(self, file_path: str):
        self.stop()
        self.junctions = {}
        
        junction_data_list = SumoNetParser.parse(file_path)
        
        for i, data in enumerate(junction_data_list):
            port = self.base_port + i
            junc = Junction(data, port)
            
            # Attach existing observers
            for observer in self._observers:
                for light in junc.lights:
                    light.add_observer(observer)
            
            self.junctions[str(junc.id)] = junc
            junc.start()
        
        if self.junctions:
            self.start()

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_logic, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        for junc in self.junctions.values():
            junc.stop()

    def _run_logic(self):
        # SNMP Mode: Do not automatically switch states.
        # State transitions will be handled by incoming UTMC2 SNMP commands.
        while self._running:
            time.sleep(1.0)

    def get_junction_list(self) -> List[Junction]:
        return list(self.junctions.values())
