// src/components/Controls/Toolbar.jsx
import React from 'react'

export function Toolbar({ isRunning, onStart, onStop, onStep, onClear, loading }) {
  return (
    <div>
      <h2 style={{ fontSize: 12, color: '#6a8aaa', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
        Controls
      </h2>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {!isRunning ? (
          <button className="btn btn-success" onClick={onStart} disabled={loading}>
            Start
          </button>
        ) : (
          <button className="btn btn-danger" onClick={onStop} disabled={loading}>
            Stop
          </button>
        )}
        <button className="btn btn-primary" onClick={() => onStep(1)} disabled={loading || isRunning}>
          Step
        </button>
        <button className="btn btn-secondary" onClick={onClear} disabled={loading}>
          Clear
        </button>
      </div>
    </div>
  )
}