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
# File: main.py
# Author: Gabriel Moraes
# Date: 2026-10-10

import sys
import os

# Add the project directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import subprocess
import re

def ensure_node_env():
    """Ensure Node.js >= 20 is available in PATH, resolving via NVM if needed."""
    def get_node_version(node_bin="node"):
        try:
            out = subprocess.check_output([node_bin, "-v"], text=True, stderr=subprocess.DEVNULL).strip()
            match = re.search(r"v(\d+)", out)
            if match:
                return int(match.group(1))
        except Exception:
            return 0
        return 0

    if get_node_version("node") >= 20:
        return

    nvm_dir = os.environ.get("NVM_DIR", os.path.expanduser("~/.nvm"))
    versions_dir = os.path.join(nvm_dir, "versions", "node")
    if os.path.isdir(versions_dir):
        try:
            versions = sorted(os.listdir(versions_dir), reverse=True)
            for v in versions:
                bin_path = os.path.join(versions_dir, v, "bin")
                node_bin = os.path.join(bin_path, "node")
                if os.path.isfile(node_bin) and get_node_version(node_bin) >= 20:
                    current_path = os.environ.get("PATH", "")
                    os.environ["PATH"] = f"{bin_path}:{current_path}"
                    return
        except Exception:
            pass

def main():
    if "--server" in sys.argv:
        from server.api import run_server
        try:
            print("Simulator Manager and API initializing...")
            run_server()
        except Exception as e:
            print(f"Error starting application: {e}")
            sys.exit(1)
    else:
        # Start Electron UI
        print("Iniciando interface gráfica...")
        ensure_node_env()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
        try:
            subprocess.run(["npm", "start"], cwd=ui_path)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
