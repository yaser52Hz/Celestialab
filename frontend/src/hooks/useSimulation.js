// src/hooks/useSimulation.js
import { useState, useEffect, useCallback } from 'react'
import { simulationApi } from '../api/endpoints'

export function useSimulation() {
  const [simId, setSimId] = useState(null)
  const [bodies, setBodies] = useState([])
  const [state, setState] = useState(null)
  const [isRunning, setIsRunning] = useState(false)
  const [time, setTime] = useState(0)
  const [loading, setLoading] = useState(false)
  const [ws, setWs] = useState(null)

  const fetchState = useCallback(async (id) => {
    if (!id) return
    try {
      const res = await simulationApi.get(id)
      setBodies(res.data.bodies || [])
      setState(res.data)
      setIsRunning(res.data.is_running || false)
      setTime(res.data.time || 0)
    } catch (err) {
      console.error('Fetch state error:', err)
    }
  }, [])

  const createSimulation = useCallback(async () => {
    setLoading(true)
    try {
      const res = await simulationApi.create({
        name: 'Celestial Simulation',
        dt: 60,
        integrator: 'verlet'
      })
      const id = res.data.id
      setSimId(id)
      await fetchState(id)
    } catch (err) {
      console.error('Create simulation error:', err)
    }
    setLoading(false)
  }, [fetchState])

  const addBody = useCallback(async (bodyData) => {
    if (!simId) return
    setLoading(true)
    try {
      await simulationApi.addBody(simId, bodyData)
      await fetchState(simId)
    } catch (err) {
      console.error('Add body error:', err)
    }
    setLoading(false)
  }, [simId, fetchState])

  const removeBody = useCallback(async (bodyId) => {
    if (!simId) return
    try {
      await simulationApi.removeBody(simId, bodyId)
      await fetchState(simId)
    } catch (err) {
      console.error('Remove body error:', err)
    }
  }, [simId, fetchState])

  const start = useCallback(async () => {
    if (!simId) return
    try {
      await simulationApi.start(simId)
      setIsRunning(true)
    } catch (err) {
      console.error('Start error:', err)
    }
  }, [simId])

  const stop = useCallback(async () => {
    if (!simId) return
    try {
      await simulationApi.stop(simId)
      setIsRunning(false)
    } catch (err) {
      console.error('Stop error:', err)
    }
  }, [simId])

  const step = useCallback(async (steps = 1) => {
    if (!simId) return
    setLoading(true)
    try {
      await simulationApi.step(simId, steps)
      await fetchState(simId)
    } catch (err) {
      console.error('Step error:', err)
    }
    setLoading(false)
  }, [simId, fetchState])

  const clear = useCallback(async () => {
    if (!simId) return
    setLoading(true)
    try {
      await simulationApi.clear(simId)
      await fetchState(simId)
    } catch (err) {
      console.error('Clear error:', err)
    }
    setLoading(false)
  }, [simId, fetchState])

  // Auto-create simulation on mount
  useEffect(() => {
    createSimulation()
  }, [])

  // WebSocket connection for real-time updates
  useEffect(() => {
    if (!simId) return

    const ws = new WebSocket(`ws://localhost:8000/ws/simulation/${simId}`)
    setWs(ws)

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setBodies(data.bodies || [])
        setState(data)
        setTime(data.time || 0)
        setIsRunning(data.is_running || false)
      } catch (err) {
        console.error('WebSocket parse error:', err)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    return () => {
      ws.close()
    }
  }, [simId])

  return {
    simId,
    bodies,
    state,
    isRunning,
    time,
    loading,
    createSimulation,
    addBody,
    removeBody,
    start,
    stop,
    step,
    clear,
    fetchState,
  }
}