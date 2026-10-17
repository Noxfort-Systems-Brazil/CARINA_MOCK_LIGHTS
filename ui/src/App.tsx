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
 * File: ui/src/App.tsx
 * Author: Gabriel Moraes
 * Date: October 2026
 */

import { useEffect, useState, useRef } from 'react'
import { 
  ThemeProvider, createTheme, CssBaseline, 
  AppBar, Toolbar, Typography, Button, Container, Grid, 
  Card, CardContent, CardHeader, Switch, FormControlLabel,
  Box, Chip, Tooltip, IconButton
} from '@mui/material'
import { FolderOpen, SignalCellularAlt, SignalCellularConnectedNoInternet0Bar, Traffic, ContentCopy, ReportProblem, BugReport } from '@mui/icons-material'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00e5ff',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#0a0e17',
      paper: '#111827',
    },
    success: {
      main: '#00e676',
    },
    error: {
      main: '#ff1744',
    },
    warning: {
      main: '#ffab00',
    }
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h6: {
      fontWeight: 600,
    }
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
          backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0))',
        }
      }
    }
  }
})

interface Light {
  id: number
  state: string
  label: string
}

interface Junction {
  id: string
  utmc_port: number
  utmc_address: string
  brand?: string
  model?: string
  lights: Light[]
  failure: boolean
  disable_fixed_plans: boolean
  connected: boolean
  protocol: string
}

const getApiUrl = (path: string) => {
  const host = window.location.hostname || 'localhost';
  return `http://${host}:8000${path}`;
};

const getWsUrl = (path: string) => {
  const host = window.location.hostname || 'localhost';
  return `ws://${host}:8000${path}`;
};

export default function App() {
  const [junctions, setJunctions] = useState<Junction[]>([])
  const [statusText, setStatusText] = useState('Nenhum mapa carregado')
  const ws = useRef<WebSocket | null>(null)

  const handleSimulateError = async (id: string, category: 'HARDWARE' | 'SOFTWARE' = 'HARDWARE') => {
    try {
      const res = await fetch(getApiUrl(`/api/junctions/${id}/simulate-error`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category })
      })
      const data = await res.json()
      if (data.status === 'success') {
        const info = data.error_info
        alert(`🚨 [Cruzamento ${id}] Erro de ${info.category} Simulado!\n\n• Alerta enviado via SNMP Trap para a CARINA!\n• Categoria: ${info.category}\n• Tipo: ${info.name}\n• Nível: ${info.level}\n• Mensagem: ${info.message}`)
      } else {
        alert('Erro ao simular falha: ' + data.message)
      }
    } catch (e) {
      console.error(e)
      alert('Falha ao conectar à API para simular erro.')
    }
  }

  const fetchJunctions = async () => {
    try {
      const res = await fetch(getApiUrl('/api/junctions'))
      const data = await res.json()
      setJunctions(data.junctions || [])
      if (data.junctions && data.junctions.length > 0) {
        setStatusText(`${data.junctions.length} Cruzamentos Ativos`)
      }
    } catch (e) {
      console.error(e)
    }
  }

  useEffect(() => {
    fetchJunctions()
    
    let reconnectTimer: number
    const connectWS = () => {
      const socket = new WebSocket(getWsUrl('/ws'))
      ws.current = socket

      socket.onmessage = (event) => {
        const msg = JSON.parse(event.data)
        if (msg.type === 'state_change') {
          setJunctions(prev => prev.map(j => {
            if (j.id === msg.junction_id) {
              return {
                ...j,
                lights: j.lights.map(l => l.id === msg.light_id ? { ...l, state: msg.state } : l)
              }
            }
            return j
          }))
        } else if (msg.type === 'status_change') {
          setJunctions(prev => prev.map(j => {
            if (j.id === msg.junction_id) {
              return { ...j, connected: msg.connected }
            }
            return j
          }))
        }
      }

      socket.onclose = () => {
        console.log('WS connection lost. Reconnecting...')
        reconnectTimer = window.setTimeout(connectWS, 2000)
      }
    }

    connectWS()

    return () => {
      window.clearTimeout(reconnectTimer)
      if (ws.current) {
        ws.current.onclose = null
        ws.current.close()
      }
    }
  }, [])

  const handleOpenMap = async () => {
    if ((window as any).require) {
      const { ipcRenderer } = (window as any).require('electron')
      const filePath = await ipcRenderer.invoke('dialog:openFile')
      if (filePath) {
        try {
          const res = await fetch(getApiUrl('/api/load'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: filePath })
          })
          const data = await res.json()
          if (data.status === 'success') {
            await fetchJunctions()
          } else {
            alert('Erro ao carregar: ' + data.message)
          }
        } catch (e) {
          console.error(e)
        }
      }
    } else {
      alert("Ambiente Electron não detectado.")
    }
  }

  const toggleFailure = async (id: string, current: boolean) => {
    await fetch(getApiUrl(`/api/junctions/${id}/failure`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: !current })
    })
    setJunctions(prev => prev.map(j => j.id === id ? { ...j, failure: !current } : j))
  }

  const togglePlans = async (id: string, current: boolean) => {
    await fetch(getApiUrl(`/api/junctions/${id}/fixed-plans`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: !current })
    })
    setJunctions(prev => prev.map(j => j.id === id ? { ...j, disable_fixed_plans: !current } : j))
  }




  const getLightColor = (state: string) => {
    if (state === 'GREEN') return '#00e676'
    if (state === 'YELLOW') return '#ffab00'
    if (state === 'RED') return '#ff1744'
    return '#111111'
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <AppBar position="static" elevation={0} sx={{ background: 'rgba(17, 24, 39, 0.8)', backdropFilter: 'blur(10px)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
          <Toolbar>
            <Traffic sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 700, letterSpacing: 1 }}>
              CARINA MOCK LIGHTS
            </Typography>
            <Chip 
              label={statusText} 
              color={junctions.length > 0 ? "success" : "default"} 
              variant="outlined" 
              sx={{ mr: 3 }}
            />
            <Button 
              variant="contained" 
              color="primary" 
              startIcon={<FolderOpen />}
              onClick={handleOpenMap}
              sx={{ borderRadius: 8, textTransform: 'none', px: 3 }}
            >
              Abrir Mapa SUMO
            </Button>
          </Toolbar>
        </AppBar>

        <Container maxWidth={false} sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <Grid container spacing={3}>
            {junctions.map((j) => (
              <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={j.id}>
                <Card>
                  <CardHeader
                    title={`Cruzamento ${j.id}`}
                    subheader={j.brand ? `${j.brand} ${j.model}` : "Não informado"}
                    subheaderTypographyProps={{ variant: 'caption', color: 'primary.main', fontWeight: 600 }}
                    titleTypographyProps={{ variant: 'h6', fontSize: '1.1rem' }}
                    action={
                      <Tooltip title={j.connected ? "Conectado (UTMC2)" : "Desconectado"}>
                        <IconButton size="small">
                          {j.connected ? 
                            <SignalCellularAlt color="success" /> : 
                            <SignalCellularConnectedNoInternet0Bar color="error" />
                          }
                        </IconButton>
                      </Tooltip>
                    }
                    sx={{ pb: 0 }}
                  />
                  <CardContent>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
                        Server Address:
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace', bgcolor: 'rgba(0,0,0,0.2)', p: 1, borderRadius: 1, flexGrow: 1, fontSize: '0.85rem' }}>
                          {j.utmc_address}
                        </Typography>
                        <Tooltip title="Copiar completo (udp://...)">
                          <IconButton onClick={() => navigator.clipboard.writeText(j.utmc_address)} size="small" sx={{ bgcolor: 'rgba(255,255,255,0.05)' }}>
                            <ContentCopy fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                        <Button 
                          size="small" 
                          variant="outlined" 
                          onClick={() => {
                            const clean = j.utmc_address.replace('udp://', '');
                            navigator.clipboard.writeText(clean);
                          }}
                          sx={{ textTransform: 'none', fontSize: '0.7rem', py: 0.2, px: 1, borderRadius: 4 }}
                        >
                          IP:Porta
                        </Button>
                        <Button 
                          size="small" 
                          variant="outlined" 
                          onClick={() => {
                            const clean = j.utmc_address.replace('udp://', '').split(':')[0];
                            navigator.clipboard.writeText(clean);
                          }}
                          sx={{ textTransform: 'none', fontSize: '0.7rem', py: 0.2, px: 1, borderRadius: 4 }}
                        >
                          Apenas IP
                        </Button>
                        <Button 
                          size="small" 
                          variant="outlined" 
                          onClick={() => {
                            const clean = j.utmc_address.replace('udp://', '').split(':')[1];
                            navigator.clipboard.writeText(clean);
                          }}
                          sx={{ textTransform: 'none', fontSize: '0.7rem', py: 0.2, px: 1, borderRadius: 4 }}
                        >
                          Porta
                        </Button>
                      </Box>
                    </Box>

                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mb: 2 }}>
                      <FormControlLabel
                        control={<Switch checked={j.failure} onChange={() => toggleFailure(j.id, j.failure)} color="error" />}
                        label="Simular Falha de Conexão"
                      />
                      <FormControlLabel
                        control={<Switch checked={j.disable_fixed_plans} onChange={() => togglePlans(j.id, j.disable_fixed_plans)} color="warning" />}
                        label="Desativar Planos Fixos"
                      />
                      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                        <Button
                          variant="contained"
                          color="secondary"
                          size="small"
                          fullWidth
                          startIcon={<ReportProblem />}
                          onClick={() => handleSimulateError(j.id, 'HARDWARE')}
                          sx={{ borderRadius: 3, textTransform: 'none', fontWeight: 600, fontSize: '0.75rem' }}
                        >
                          Erro Hardware
                        </Button>
                        <Button
                          variant="contained"
                          color="warning"
                          size="small"
                          fullWidth
                          startIcon={<BugReport />}
                          onClick={() => handleSimulateError(j.id, 'SOFTWARE')}
                          sx={{ borderRadius: 3, textTransform: 'none', fontWeight: 600, fontSize: '0.75rem' }}
                        >
                          Erro Software
                        </Button>
                      </Box>
                    </Box>

                    <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                      Semáforos ({j.lights.length})
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, maxHeight: 150, overflowY: 'auto', p: 1, bgcolor: 'rgba(0,0,0,0.1)', borderRadius: 2 }}>
                      {j.lights.map(l => (
                        <Tooltip key={l.id} title={`${l.label} - ${l.state}`}>
                          <Box
                            sx={{
                              width: 24,
                              height: 24,
                              borderRadius: '50%',
                              bgcolor: getLightColor(l.state),
                              boxShadow: l.state !== 'OFF' ? `0 0 10px ${getLightColor(l.state)}` : 'none',
                              border: '1px solid rgba(255,255,255,0.2)',
                              transition: 'all 0.3s ease'
                            }}
                          />
                        </Tooltip>
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  )
}
