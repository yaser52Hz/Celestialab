import { useEffect, useRef, useState } from 'react'
import TopBar from './components/layout/TopBar'
import BottomToolbar from './components/layout/BottomToolbar'
import ToolPanel from './components/layout/ToolPanel'
import SimulationScene from './components/scene/SimulationScene'
import './App.css'

function App() {
  const appRef = useRef<HTMLElement>(null)

  const [activeTool, setActiveTool] = useState<string | null>(null)
  const [isFullscreen, setIsFullscreen] = useState(false)

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(
        document.fullscreenElement !== null,
      )
    }

    document.addEventListener(
      'fullscreenchange',
      handleFullscreenChange,
    )

    return () => {
      document.removeEventListener(
        'fullscreenchange',
        handleFullscreenChange,
      )
    }
  }, [])

  const toggleFullscreen = async () => {
    try {
      if (!document.fullscreenElement) {
        await appRef.current?.requestFullscreen()
      } else {
        await document.exitFullscreen()
      }
    } catch (error) {
      console.error(
        'Fullscreen error:',
        error,
      )
    }
  }

  const handleToolSelect = (tool: string) => {
    setActiveTool((current) =>
      current === tool ? null : tool,
    )
  }

  return (
    <main
      ref={appRef}
      className="app"
    >
      <TopBar
        isFullscreen={isFullscreen}
        onFullscreen={toggleFullscreen}
      />

      <section className="workspace">
        <SimulationScene />

        {activeTool && (
          <ToolPanel
            tool={activeTool}
            onClose={() => setActiveTool(null)}
          />
        )}
      </section>

      <BottomToolbar
        activeTool={activeTool}
        onToolSelect={handleToolSelect}
      />
    </main>
  )
}

export default App