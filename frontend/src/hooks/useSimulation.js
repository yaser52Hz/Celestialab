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
        dt: 3600,
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
    try {
      await simulationApi.step(simId, steps)
      await fetchState(simId)
    } catch (err) {
      console.error('Step error:', err)
    }
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

  // Auto-step when running
  useEffect(() => {
    if (!isRunning) return
    const interval = setInterval(() => {
      step(1)
    }, 100)
    return () => clearInterval(interval)
  }, [isRunning, step])

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