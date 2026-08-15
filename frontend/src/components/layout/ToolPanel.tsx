interface ToolPanelProps {
  tool: string
  onClose: () => void
}

const titles: Record<string, string> = {
  objects: 'Objects',
  forces: 'Forces',
  tools: 'Tools',
  analysis: 'Analysis',
  more: 'More',
}

function ToolPanel({
  tool,
  onClose,
}: ToolPanelProps) {
  return (
    <aside className="tool-panel">
      <div className="panel-header">
        <h2>
          {titles[tool] ?? tool}
        </h2>

        <button
          type="button"
          className="panel-close"
          onClick={onClose}
          aria-label="Close panel"
        >
          ×
        </button>
      </div>

      <div className="panel-content">
        {tool === 'objects' && (
          <>
            <button
              type="button"
              className="panel-action"
            >
              <span>＋</span>
              Add body
            </button>

            <div className="empty-state">
              No objects in the scene.
            </div>
          </>
        )}

        {tool === 'forces' && (
          <>
            <button
              type="button"
              className="panel-action"
            >
              <span>＋</span>
              Add force
            </button>

            <div className="empty-state">
              No forces defined.
            </div>
          </>
        )}

        {tool === 'tools' && (
          <div className="tool-list">
            <button type="button">
              Measure
            </button>

            <button type="button">
              Coordinate system
            </button>

            <button type="button">
              Grid
            </button>
          </div>
        )}

        {tool === 'analysis' && (
          <div className="tool-list">
            <button type="button">
              Charts
            </button>

            <button type="button">
              Trajectory
            </button>

            <button type="button">
              Vectors
            </button>
          </div>
        )}

        {tool === 'more' && (
          <div className="tool-list">
            <button type="button">
              Import
            </button>

            <button type="button">
              Export
            </button>

            <button type="button">
              Settings
            </button>
          </div>
        )}
      </div>
    </aside>
  )
}

export default ToolPanel