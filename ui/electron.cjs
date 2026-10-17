/**
 * CARINA Mock Lights - SUMO Traffic Light Simulation & UTMC2/SNMP Server
 * Copyright (C) 2026 Noxfort Systems
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * File: ui/electron.cjs
 * Author: Gabriel Moraes
 * Date: October 2026
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');

let pythonProcess = null;

// Suppress verbose Chromium/X11 logs (like kAtomsToCache warnings)
app.commandLine.appendSwitch('log-level', '3');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    autoHideMenuBar: true,
    backgroundColor: '#121212'
  });

  win.loadURL(
    isDev
      ? 'http://localhost:5173'
      : `file://${path.join(__dirname, 'dist/index.html')}`
  );
  
  // if (isDev) {
  //   win.webContents.openDevTools({ mode: 'detach' });
  // }

  ipcMain.handle('dialog:openFile', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog(win, {
      title: 'Selecionar Mapa SUMO',
      properties: ['openFile'],
      filters: [
        { name: 'SUMO Network', extensions: ['net.xml', 'net.xml.gz'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    });
    if (canceled) {
      return null;
    } else {
      return filePaths[0];
    }
  });
}

app.whenReady().then(() => {
  // Start python backend
  const pythonExecutable = isDev 
    ? path.join(__dirname, '..', '.venv', 'bin', 'python')
    : 'python'; // or bundled executable

  pythonProcess = spawn(pythonExecutable, [path.join(__dirname, '..', 'main.py'), '--server']);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    // Uvicorn logs to stderr by default
    console.log(`Python Log: ${data}`);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});


