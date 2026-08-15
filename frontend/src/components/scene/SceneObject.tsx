import type { SimulationObject } from '../../types/simulation'

interface SceneObjectProps {
  object: SimulationObject
  selected: boolean
  onSelect: (id: string) => void
}

function SceneObject({
  object,
  selected,
  onSelect,
}: SceneObjectProps) {
  return (
    <button
      type="button"
      className={`scene-object ${
        selected ? 'selected' : ''
      }`}
      style={{
        left: `calc(50% + ${object.x}px)`,
        top: `calc(50% - ${object.y}px)`,
      }}
      onPointerDown={(event) => {
        event.stopPropagation()
        onSelect(object.id)
      }}
      title={object.name}
    >
      <span className="scene-object-dot" />
    </button>
  )
}

export default SceneObject