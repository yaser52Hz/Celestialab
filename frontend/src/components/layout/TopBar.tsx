interface TopBarProps {
  isFullscreen: boolean
  onFullscreen: () => void
}

function TopBar({
  isFullscreen,
  onFullscreen,
}: TopBarProps) {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-mark">
          ✦
        </span>

        <span>
          Celestialab
        </span>
      </div>

      <div className="topbar-actions">
        <button
          type="button"
          className="icon-button"
          title="Settings"
        >
          ⚙
        </button>

        <button
          type="button"
          className="run-button"
        >
          <span>▶</span>

          <span>
            Run
          </span>
        </button>

        <button
          type="button"
          className="icon-button"
          title={
            isFullscreen
              ? 'Exit fullscreen'
              : 'Fullscreen'
          }
          onClick={onFullscreen}
        >
          {isFullscreen ? '⛶' : '⛶'}
        </button>
      </div>
    </header>
  )
}

export default TopBar