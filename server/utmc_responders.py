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
# File: server/utmc_responders.py
# Author: Gabriel Moraes
# Date: 2026-10-10

import logging
from server.utmc_handlers import registry

try:
    from pysnmp.entity.rfc3413 import cmdrsp
    from pysnmp.proto.api import v2c
except ImportError:
    cmdrsp = None
    v2c = None

from server.utmc_logger import _conn_logger, _cmd_logger

if cmdrsp:
    class MockSetCommandResponder(cmdrsp.SetCommandResponder):
        def _handle_request(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            if acInfo:
                transportDomain, transportAddress = acInfo
                source_ip = transportAddress[0]
            else:
                source_ip = "127.0.0.1"
            
            _conn_logger.info(f"Connection attempt (Set) from {source_ip} to junction {self.server_instance.junction_id}")

            if self.server_instance.simulate_failure:
                _conn_logger.warning(f"Connection failed (Simulated Failure) from {source_ip} to junction {self.server_instance.junction_id}")
                self._release_state(stateReference)
                return

            is_secure = source_ip.startswith("10.") or source_ip.startswith("127.") or source_ip.startswith("192.168") or source_ip.startswith("172.")
            if not is_secure:
                print(f"VPN Firewall: Blocked UTMC2 request from external IP {source_ip}")
                _conn_logger.warning(f"Connection blocked (VPN Firewall) from {source_ip} to junction {self.server_instance.junction_id}")
                self._release_state(stateReference)
                return

            _conn_logger.info(f"Connection successful (Set) from {source_ip} to junction {self.server_instance.junction_id}")

            if self.server_instance.on_activity:
                self.server_instance.on_activity()
                
            varBinds = v2c.apiPDU.getVarBinds(PDU) if hasattr(v2c.apiPDU, 'getVarBinds') else v2c.apiPDU.get_varbinds(PDU)
            
            for oid, val in varBinds:
                try:
                    val_int = int(val) 
                    oid_str = str(oid)
                    
                    if (".2.1.21." in oid_str or ".2.1.254." in oid_str or ".2.1.255." in oid_str) and not (".255.1" in oid_str or ".254.1" in oid_str):
                        continue

                    handled = registry.handle_set(oid_str, val_int, self.server_instance.junction_id, self._lights)
                    if not handled:
                        msg = f"[Junction {self.server_instance.junction_id}] Unknown UTMC2 Command -> OID: {oid_str}, Value: {val_int}"
                        print(msg)
                        _cmd_logger.warning(msg)

                except Exception as e:
                    _cmd_logger.error(f"UTMC2 parse err {oid}: {e}")
                    print(f"UTMC2 parse err {oid}: {e}")

            self._send_response(snmpEngine, stateReference, PDU, varBinds)
            self._release_state(stateReference)

        def _send_response(self, snmpEngine, stateReference, PDU, varBinds):
            if hasattr(v2c.apiPDU, 'getResponse'):
                responsePDU = v2c.apiPDU.getResponse(PDU)
                v2c.apiPDU.setErrorStatus(responsePDU, 0)
                v2c.apiPDU.setErrorIndex(responsePDU, 0)
                v2c.apiPDU.setVarBinds(responsePDU, varBinds)
            else:
                responsePDU = v2c.apiPDU.get_response(PDU)
                v2c.apiPDU.set_error_status(responsePDU, 0)
                v2c.apiPDU.set_error_index(responsePDU, 0)
                v2c.apiPDU.set_varbinds(responsePDU, varBinds)
            
            if hasattr(self, 'send_pdu'):
                self.send_pdu(snmpEngine, stateReference, responsePDU)
            else:
                self.sendPdu(snmpEngine, stateReference, responsePDU)

        def _release_state(self, stateReference):
            if hasattr(self, 'release_state_information'):
                self.release_state_information(stateReference)
            else:
                self.releaseStateInformation(stateReference)

        def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            self._handle_request(snmpEngine, stateReference, contextName, PDU, acInfo)

        def handle_management_operation(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            self._handle_request(snmpEngine, stateReference, contextName, PDU, acInfo)


    class MockGetCommandResponder(cmdrsp.GetCommandResponder):
        def _handle_request(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            try:
                if acInfo:
                    transportDomain, transportAddress = acInfo
                    source_ip = transportAddress[0]
                else:
                    source_ip = "127.0.0.1"
                    
                print(f"MockGetCommandResponder._handle_request called from {source_ip}")

                _conn_logger.info(f"Connection attempt (Get) from {source_ip} to junction {self.server_instance.junction_id}")

                if self.server_instance.simulate_failure:
                    _conn_logger.warning(f"Connection failed (Simulated Failure) from {source_ip} to junction {self.server_instance.junction_id}")
                    self._release_state(stateReference)
                    return
                    
                is_secure = source_ip.startswith("10.") or source_ip.startswith("127.") or source_ip.startswith("192.168") or source_ip.startswith("172.")
                if not is_secure:
                    print(f"VPN Firewall: Blocked UTMC2 request from external IP {source_ip}")
                    _conn_logger.warning(f"Connection blocked (VPN Firewall) from {source_ip} to junction {self.server_instance.junction_id}")
                    self._release_state(stateReference)
                    return

                _conn_logger.info(f"Connection successful (Get) from {source_ip} to junction {self.server_instance.junction_id}")
                
                varBinds = v2c.apiPDU.getVarBinds(PDU) if hasattr(v2c.apiPDU, 'getVarBinds') else v2c.apiPDU.get_varbinds(PDU)
                    
                newVarBinds = []
                error_status = 0
                error_index = 0
                for idx, (oid, val) in enumerate(varBinds):
                    oid_str = str(oid)
                    reply_val = registry.handle_get(oid_str, self.server_instance.junction_id, self.server_instance.lights)
                    if reply_val is None:
                        # OID not found or not supported -> return noSuchName (2)
                        error_status = 2
                        error_index = idx + 1
                        newVarBinds.append((oid, val))
                    else:
                        newVarBinds.append((oid, reply_val))

                self._send_response(snmpEngine, stateReference, PDU, newVarBinds, error_status, error_index)
                self._release_state(stateReference)
            except Exception as e:
                print(f"Exception in _handle_request: {e}")
                import traceback
                traceback.print_exc()

        def _send_response(self, snmpEngine, stateReference, PDU, newVarBinds, error_status=0, error_index=0):
            if hasattr(v2c.apiPDU, 'getResponse'):
                responsePDU = v2c.apiPDU.getResponse(PDU)
                v2c.apiPDU.setErrorStatus(responsePDU, error_status)
                v2c.apiPDU.setErrorIndex(responsePDU, error_index)
                v2c.apiPDU.setVarBinds(responsePDU, newVarBinds)
            else:
                responsePDU = v2c.apiPDU.get_response(PDU)
                v2c.apiPDU.set_error_status(responsePDU, error_status)
                v2c.apiPDU.set_error_index(responsePDU, error_index)
                v2c.apiPDU.set_varbinds(responsePDU, newVarBinds)
            
            if hasattr(self, 'send_pdu'):
                self.send_pdu(snmpEngine, stateReference, responsePDU)
            else:
                self.sendPdu(snmpEngine, stateReference, responsePDU)

        def _release_state(self, stateReference):
            if hasattr(self, 'release_state_information'):
                self.release_state_information(stateReference)
            else:
                self.releaseStateInformation(stateReference)

        def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            self._handle_request(snmpEngine, stateReference, contextName, PDU, acInfo)

        def handle_management_operation(self, snmpEngine, stateReference, contextName, PDU, acInfo=None):
            self._handle_request(snmpEngine, stateReference, contextName, PDU, acInfo)
else:
    MockSetCommandResponder = None
    MockGetCommandResponder = None
