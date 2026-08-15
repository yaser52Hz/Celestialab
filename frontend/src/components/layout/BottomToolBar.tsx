interface BottomToolbarProps {
  activeTool: string | null
  onToolSelect: (tool: string) => void
}

const tools = [
  {
    id: 'objects',
    icon: '◉',
    label: 'Objects',
  },
  {
    id: 'forces',
    icon: '⚡',
    label: 'Forces',
  },
  {
    id: 'tools',
    icon: '⌁',
    label: 'Tools',
  },
  {
    id: 'analysis',
    icon: '◒',
    label: 'Analysis',
  },
]

function BottomToolbar({
  activeTool,
  onToolSelect,
}: BottomToolbarProps) {
  return (
    <nav className="bottom-toolbar">
      <div className="tool-group">
        {tools.map((tool) => (
          <button
            type="button"
            key={tool.id}
            className={`tool-button ${
              activeTool === tool.id
                ? 'active'
                : ''
            }`}
            onClick={() => onToolSelect(tool.id)}
          >
            <span className="tool-icon">
              {tool.icon}
            </span>

            <span className="tool-label">
              {tool.label}
            </span>
          </button>
        ))}
      </div>

      <button
        type="button"
        className={`tool-button ${
          activeTool === 'more'
            ? 'active'
            : ''
        }`}
        onClick={() => onToolSelect('more')}
      >
        <span className="tool-icon">⋯</span>

        <span className="tool-label">
          More
        </span>
      </button>
    </nav>
  )
}

export default BottomToolbar