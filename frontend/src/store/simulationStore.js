import { create } from 'zustand'
import { simulationApi } from '../api/endpoints'

export const useSimulationStore = create((set, get) => ({
  simId: null,
  bodies: [],
  state: null,
  isRunning: false,
  time: 0,
  loading: false,

  createSimulation: async () => {
    set({ loading: true })
    try {
      const res = await simulationApi.create({
        name: 'Celestial Simulation',
        dt: 3600,
        integrator: 'verlet'
      })
      const simId = res.data.id
      set({ simId })
      await get().fetchState(simId)
    } finally {
      set({ loading: false })
    }
  },

  fetchState: async (id) => {
    try {
      const res = await simulationApi.get(id)
      set({
        bodies: res.data.bodies || [],
        state: res.data,
        isRunning: res.data.is_running || false,
        time: res.data.time || 0
      })
    } catch (err) {
      console.error('Fetch state error:', err)
    }
  },

  addBody: async (bodyData) => {
    const { simId } = get()
    if (!simId) return
    set({ loading: true })
    try {
      await simulationApi.addBody(simId, bodyData)
      await get().fetchState(simId)
    } finally {
      set({ loading: false })
    }
  },

  removeBody: async (bodyId) => {
    const { simId } = get()
    if (!simId) return
    try {
      await simulationApi.removeBody(simId, bodyId)
      await get().fetchState(simId)
    } catch (err) {
      console.error('Remove body error:', err)
    }
  },

  start: async () => {
    const { simId } = get()
    if (!simId) return
    await simulationApi.start(simId)
    set({ isRunning: true })
  },

  stop: async () => {
    const { simId } = get()
    if (!simId) return
    await simulationApi.stop(simId)
    set({ isRunning: false })
  },

  step: async (steps = 1) => {
    const { simId } = get()
    if (!simId) return
    await simulationApi.step(simId, steps)
    await get().fetchState(simId)
  },

  clear: async () => {
    const { simId } = get()
    if (!simId) return
    await simulationApi.clear(simId)
    await get().fetchState(simId)
  },
}))