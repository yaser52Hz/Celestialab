// src/App.jsx
import React from 'react'
import { useSimulation } from './hooks/useSimulation'
import { Scene } from './components/Scene/Scene'
import { InfoPanel } from './components/UI/InfoPanel'
import { HUD } from './components/UI/HUD'
import './styles/globals.css'

function App() {
  const {
    bodies,
    state,
    isRunning,
    time,
    loading,
    addBody,
    removeBody,
    start,
    stop,
    step,
    clear,
  } = useSimulation()

  const addEarth = () => {
    addBody({
      name: 'Earth',
      mass: 5.972e24,
      position: [1.496e11, 0, 0],
      velocity: [0, 2.978e4, 0],
      radius: 6.37e6,
      color: '#4B9CD3'
    })
  }

  const addSun = () => {
    addBody({
      name: 'Sun',
      mass: 1.989e30,
      position: [0, 0, 0],
      velocity: [0, 0, 0],
      radius: 6.96e8,
      color: '#FDB813'
    })
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <header>
          <h1>🌌 Celestial Engine</h1>
        </header>

        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          <button className="btn btn-success" onClick={addSun} disabled={loading}>
            ☀️ Sun
          </button>
          <button className="btn btn-primary" onClick={addEarth} disabled={loading}>
            🌍 Earth
          </button>
          <button className="btn btn-success" onClick={start} disabled={isRunning || loading}>
            ▶ Start
          </button>
          <button className="btn btn-danger" onClick={stop} disabled={!isRunning || loading}>
            ⏹ Stop
          </button>
          <button className="btn btn-secondary" onClick={() => step(1)} disabled={isRunning || loading}>
            ⏭ Step
          </button>
          <button className="btn btn-secondary" onClick={clear} disabled={loading}>
            🗑 Clear
          </button>
        </div>

        <div style={{ fontSize: 13, color: '#8ba0c4' }}>
          <div>Bodies: <span style={{ color: '#e8edf5' }}>{bodies.length}</span></div>
          <div>Time: <span style={{ color: '#e8edf5' }}>{time.toFixed(0)}s</span></div>
          <div>Status: <span style={{ color: isRunning ? '#00d4aa' : '#ff6b6b' }}>
            {isRunning ? '▶ Running' : '⏸ Paused'}
          </span></div>
        </div>

        <InfoPanel state={state} />
      </aside>

      <main className="scene-container">
        <Scene bodies={bodies} />
        <HUD bodyCount={bodies.length} time={time} isRunning={isRunning} />
      </main>
    </div>
  )
}

export default App