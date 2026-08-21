// src/components/BodyManager/BodyForm.jsx
import React, { useState } from 'react'

const DEFAULT_BODY = {
  name: '',
  mass: 1e24,
  position: [0, 0, 0],
  velocity: [0, 0, 0],
  radius: 1e7,
  color: '#4a9eff',
}

export function BodyForm({ onAdd, loading }) {
  const [form, setForm] = useState(DEFAULT_BODY)
  const [show, setShow] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    if (name === 'position' || name === 'velocity') {
      const parts = value.split(',').map(Number)
      setForm((prev) => ({
        ...prev,
        [name]: parts.length === 3 ? parts : [0, 0, 0],
      }))
    } else if (name === 'mass' || name === 'radius') {
      setForm((prev) => ({ ...prev, [name]: parseFloat(value) || 0 }))
    } else {
      setForm((prev) => ({ ...prev, [name]: value }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.name) return
    onAdd(form)
    setForm(DEFAULT_BODY)
    setShow(false)
  }

  if (!show) {
    return (
      <button className="btn btn-primary" onClick={() => setShow(true)} disabled={loading}>
        + Add Body
      </button>
    )
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 4 }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
        <div className="form-group">
          <label style={{ fontSize: 11, color: '#6a8aaa' }}>Name</label>
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Earth"
            required
            style={{ padding: '4px 6px', background: '#0a0e1a', border: '1px solid #1a2744', borderRadius: 4, color: '#e8edf5' }}
          />
        </div>
        <div className="form-group">
          <label style={{ fontSize: 11, color: '#6a8aaa' }}>Mass (kg)</label>
          <input
            type="number"
            name="mass"
            value={form.mass}
            onChange={handleChange}
            style={{ padding: '4px 6px', background: '#0a0e1a', border: '1px solid #1a2744', borderRadius: 4, color: '#e8edf5' }}
          />
        </div>
        <div className="form-group" style={{ gridColumn: 'span 2' }}>
          <label style={{ fontSize: 11, color: '#6a8aaa' }}>Position (x, y, z)</label>
          <input
            type="text"
            name="position"
            value={form.position.join(', ')}
            onChange={handleChange}
            placeholder="1.496e11, 0, 0"
            style={{ padding: '4px 6px', background: '#0a0e1a', border: '1px solid #1a2744', borderRadius: 4, color: '#e8edf5' }}
          />
        </div>
        <div className="form-group" style={{ gridColumn: 'span 2' }}>
          <label style={{ fontSize: 11, color: '#6a8aaa' }}>Velocity (vx, vy, vz)</label>
          <input
            type="text"
            name="velocity"
            value={form.velocity.join(', ')}
            onChange={handleChange}
            placeholder="0, 2.978e4, 0"
            style={{ padding: '4px 6px', background: '#0a0e1a', border: '1px solid #1a2744', borderRadius: 4, color: '#e8edf5' }}
          />
        </div>
        <div className="form-group">
          <label style={{ fontSize: 11, color: '#6a8aaa' }}>Color</label>
          <input
            type="color"
            name="color"
            value={form.color}
            onChange={handleChange}
            style={{ padding: 2, height: 30, background: '#0a0e1a', border: '1px solid #1a2744', borderRadius: 4, cursor: 'pointer' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', gap: 4, alignItems: 'flex-end' }}>
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>
            Add
          </button>
          <button type="button" className="btn btn-secondary" onClick={() => setShow(false)}>
            Cancel
          </button>
        </div>
      </div>
    </form>
  )
}