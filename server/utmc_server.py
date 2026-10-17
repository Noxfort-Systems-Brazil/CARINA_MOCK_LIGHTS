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
# File: server/utmc_server.py
# Author: Gabriel Moraes
# Date: October 2026

import threading
import asyncio
from typing import List
from core.traffic_light import TrafficLight
from server.utmc_utils import get_local_ip

try:
    from pysnmp.entity import engine, config
    from pysnmp.entity.rfc3413 import context
    from pysnmp.carrier.asyncio.dgram import udp
except ImportError:
    engine = None

from server.utmc_responders import MockSetCommandResponder, MockGetCommandResponder

class UTMCServer:
    def __init__(self, junction_id: str, lights: List[TrafficLight], port: int, on_activity=None):
        self.junction_id = junction_id
        self.lights = lights
        self.port = port
        self.on_activity = on_activity
        self.simulate_failure = False
        self.thread = None
        self.running = False
        self.loop = None

    def start(self):
        if not engine:
            print(f"Warning: pysnmp is not installed! Run 'pip install pysnmp' to enable UTMC2 on UDP {self.port}.")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)

    def get_utmc_info(self) -> str:
        ip = get_local_ip()
        return f"udp://{ip}:{self.port}"

    def _run_server(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        snmp_engine = engine.SnmpEngine()

        while True:
            try:
                config.addTransport(
                    snmp_engine,
                    udp.domainName,
                    udp.UdpTransport().openServerMode(('0.0.0.0', self.port))
                )
                break
            except Exception as e:
                self.port += 1
                if self.port > 65535:
                    print(f"Failed to bind any UDP port for UTMC2!")
                    return

        try:
            config.addV1System(snmp_engine, 'my-area', 'public')
            config.addV1System(snmp_engine, 'my-area-2', 'private')
            config.addV1System(snmp_engine, 'my-area-3', 'carina')
            config.addVacmView(snmp_engine, 'my-view', 'included', (1, 3, 6))
            config.addVacmUser(snmp_engine, 1, 'my-area', 'noAuthNoPriv', 'my-view', 'my-view')
            config.addVacmUser(snmp_engine, 2, 'my-area', 'noAuthNoPriv', 'my-view', 'my-view')
            config.addVacmUser(snmp_engine, 1, 'my-area-2', 'noAuthNoPriv', 'my-view', 'my-view')
            config.addVacmUser(snmp_engine, 2, 'my-area-2', 'noAuthNoPriv', 'my-view', 'my-view')
            config.addVacmUser(snmp_engine, 1, 'my-area-3', 'noAuthNoPriv', 'my-view', 'my-view')
            config.addVacmUser(snmp_engine, 2, 'my-area-3', 'noAuthNoPriv', 'my-view', 'my-view')
        except AttributeError:
            config.add_v1_system(snmp_engine, 'my-area', 'public')
            config.add_v1_system(snmp_engine, 'my-area-2', 'private')
            config.add_v1_system(snmp_engine, 'my-area-3', 'carina')
            config.add_vacm_user(snmp_engine, 1, 'my-area', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))
            config.add_vacm_user(snmp_engine, 2, 'my-area', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))
            config.add_vacm_user(snmp_engine, 1, 'my-area-2', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))
            config.add_vacm_user(snmp_engine, 2, 'my-area-2', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))
            config.add_vacm_user(snmp_engine, 1, 'my-area-3', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))
            config.add_vacm_user(snmp_engine, 2, 'my-area-3', 'noAuthNoPriv', readSubTree=(1, 3, 6), writeSubTree=(1, 3, 6))

        sz = context.SnmpContext(snmp_engine)

        if MockSetCommandResponder and MockGetCommandResponder:
            responder = MockSetCommandResponder(snmp_engine, sz)
            responder.server_instance = self
            responder._lights = self.lights
            
            get_responder = MockGetCommandResponder(snmp_engine, sz)
            get_responder.server_instance = self
            
            self._responders = [responder, get_responder]
        
        print(f"UTMC2 Server (UDP) started for junction {self.junction_id} on port {self.port}")
        
        try:
            self.loop.run_forever()
        except BaseException:
            pass
        finally:
            try:
                snmp_engine.transportDispatcher.closeDispatcher()
            except Exception:
                pass
            try:
                self.loop.close()
            except Exception:
                pass
