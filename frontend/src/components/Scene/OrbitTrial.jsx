// src/components/Scene/OrbitTrail.jsx
import React from 'react'
import { Line } from '@react-three/drei'

const SCALE = 1e9

export function OrbitTrail({ trail, color }) {
  if (!trail || trail.length < 2) return null

  // نمونه‌گیری برای عملکرد بهتر
  const step = Math.max(1, Math.floor(trail.length / 200))
  const points = trail
    .filter((_, i) => i % step === 0)
    .map(p => p.map(v => v / SCALE))

  if (points.length < 2) return null

  return (
    <Line
      points={points}
      color={color || '#4a9eff'}
      lineWidth={1}
      transparent
      opacity={0.4}
    />
  )
}