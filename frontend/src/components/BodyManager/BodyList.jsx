// src/components/BodyManager/BodyList.jsx
import React from 'react'

export function BodyList({ bodies, onRemove, loading }) {
  if (bodies.length === 0) {
    return (
      <div>
        <h2 style={{ fontSize: 12, color: '#6a8aaa', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
          Bodies (0)
        </h2>
        <div style={{ color: '#4a6080', fontSize: 13 }}>No bodies yet. Add one below.</div>
      </div>
    )
  }

  return (
    <div>
      <h2 style={{ fontSize: 12, color: '#6a8aaa', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
        Bodies ({bodies.length})
      </h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        {bodies.map((body) => (
          <div
            key={body.id}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '4px 8px',
              background: '#0a0e1a',
              borderRadius: 4,
              borderLeft: `3px solid ${body.color || '#4a9eff'}`,
              fontSize: 13,
            }}
          >
            <span>{body.name}</span>
            <button
              className="btn btn-secondary"
              style={{ padding: '2px 6px', fontSize: 12 }}
              onClick={() => onRemove(body.id)}
              disabled={loading}
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}