// src/components/Scene/BodyMesh.jsx
import React from 'react'
import { Sphere } from '@react-three/drei'

export function BodyMesh({ body }) {
  const visualRadius = Math.max(Math.log10(body.radius || 1) * 0.4, 0.3)

  return (
    <mesh position={body.position}>
      <Sphere args={[visualRadius, 32, 32]} />
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