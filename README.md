# Celestialab
A modular web-based platform for celestial mechanics simulation, orbital dynamics, trajectory analysis, and scientific visualization.

## 🌌 Celestial Mechanics Engine (CME)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Three.js](https://img.shields.io/badge/Three.js-r152-black.svg)](https://threejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

### 📖 Overview

**Celestial Mechanics Engine (CME)** is a full-stack computational framework designed for simulating and visualizing N-body gravitational systems. Unlike traditional tools that are either purely analytical or limited to pre-rendered animations, CME provides a **real-time, interactive environment** for exploring celestial dynamics.

#### Key Features

- 🧠 **N-body Simulation Engine** — Simulates up to 100+ bodies with Newtonian gravity
- ⚡ **Multiple Integrators** — Euler, Verlet, RK4 (with pluggable architecture)
- 🎯 **Custom Force Fields** — Define arbitrary forces via Python expressions or function hooks
- 🌐 **REST API & WebSocket** — Full programmatic control with real-time state streaming
- 🎨 **3D Visualization** — Interactive Three.js frontend with orbit trails and body selection
- 🧩 **Modular Architecture** — Physics engine, API, and frontend are completely decoupled
- 📊 **Scientific Analysis** — Energy conservation, momentum tracking, orbital parameter extraction

#### Use Cases

- Academic research in celestial mechanics and orbital dynamics
- Interactive classroom demonstrations
- Prototyping custom force models (e.g., modified gravity, solar wind)
- Visualization of many-body systems (star clusters, planetary systems)
- Potential and Density profiles in galactic dynamics