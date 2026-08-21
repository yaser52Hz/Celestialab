// src/components/Scene/BodyMesh.jsx
import React from 'react'
import { Sphere } from '@react-three/drei'

// مقیاس برای نمایش (1 واحد = 1 میلیون کیلومتر)
const SCALE = 1e9  // 1 میلیارد متر = 1 میلیون کیلومتر

export function BodyMesh({ body }) {
  const visualRadius = Math.max(Math.log10(body.radius || 1) * 0.3, 0.15)
  
  // تبدیل موقعیت از متر به واحد Three.js
  const position = body.position.map(p => p / SCALE)

  return (
    <mesh position={position}>
      <Sphere args={[visualRadius, 24, 24]} />
      <meshStandardMaterial
        color={body.color || '#ffffff'}
        emissive={body.color || '#ffffff'}
        emissiveIntensity={0.15}
        roughness={0.4}
        metalness={0.1}
      />
    </mesh>
  )
}