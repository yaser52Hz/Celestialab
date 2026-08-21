import React from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars, Grid } from '@react-three/drei'

export function Scene({ bodies }) {
  return (
    <Canvas
      camera={{ position: [5, 4, 6], fov: 45 }}
      style={{ background: '#0a0e1a', height: '100vh' }}
      gl={{ antialias: true }}
    >
      <ambientLight intensity={0.5} color="#4a9eff" />
      <directionalLight position={[30, 50, 30]} intensity={1.2} />

      <Stars radius={400} depth={80} count={4000} factor={4} saturation={0.1} fade />

      <Grid
        args={[20, 20]}  // ← به جای 120
        cellColor="#0f1a2a"
        sectionColor="#1a2a44"
        position={[0, -0.5, 0]}
      />

      {bodies.map((body) => (
        <mesh key={body.id} position={body.position}>
          <sphereGeometry args={[0.5, 16, 16]} />
          <meshStandardMaterial color={body.color || '#4a9eff'} />
        </mesh>
      ))}

      <OrbitControls
        enableDamping
        dampingFactor={0.08}
        minDistance={5}
        maxDistance={500}
        makeDefault
      />
    </Canvas>
  )
}