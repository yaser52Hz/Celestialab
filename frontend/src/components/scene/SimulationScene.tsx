import { useRef, useState } from 'react'
import type {
  PointerEvent,
  WheelEvent,
} from 'react'

import type { SimulationObject } from '../../types/simulation'

type Tool =
  | 'select'
  | 'body'
  | 'pan'
  | 'delete'

interface ViewState {
  x: number
  y: number
  zoom: number
}

interface Point {
  x: number
  y: number
}

function SimulationScene() {
  const sceneRef =
    useRef<HTMLDivElement>(null)

  const [view, setView] =
    useState<ViewState>({
      x: 0,
      y: 0,
      zoom: 1,
    })

  const [cursor, setCursor] =
    useState<Point>({
      x: 0,
      y: 0,
    })

  const [objects, setObjects] =
    useState<SimulationObject[]>([])

  const [selectedObjectId, setSelectedObjectId] =
    useState<string | null>(null)

  const [tool, setTool] =
    useState<Tool>('select')

  const [dragging, setDragging] =
    useState(false)

  const [draggingObjectId, setDraggingObjectId] =
    useState<string | null>(null)

  const lastPointer =
    useRef<Point>({
      x: 0,
      y: 0,
    })

  /*
   * ==========================================================
   * SCREEN → WORLD
   * ==========================================================
   */

  const screenToWorld = (
    clientX: number,
    clientY: number,
  ): Point | null => {
    const scene =
      sceneRef.current

    if (!scene) {
      return null
    }

    const rect =
      scene.getBoundingClientRect()

    const centerX =
      rect.left +
      rect.width / 2

    const centerY =
      rect.top +
      rect.height / 2

    return {
      x:
        (clientX -
          centerX -
          view.x) /
        view.zoom,

      y:
        (centerY -
          clientY +
          view.y) /
        view.zoom,
    }
  }

  /*
   * ==========================================================
   * CREATE BODY
   * ==========================================================
   */

  const createBody = (
    point: Point,
  ) => {
    const newObject: SimulationObject = {
      id: crypto.randomUUID(),

      name:
        `Object ${
          objects.length + 1
        }`,

      x: point.x,

      y: point.y,
    }

    setObjects(
      (current) => [
        ...current,
        newObject,
      ],
    )

    setSelectedObjectId(
      newObject.id,
    )
  }

  /*
   * ==========================================================
   * DELETE OBJECT
   * ==========================================================
   */

  const deleteObject = (
    objectId: string,
  ) => {
    setObjects(
      (current) =>
        current.filter(
          (object) =>
            object.id !==
            objectId,
        ),
    )

    setSelectedObjectId(
      (current) =>
        current === objectId
          ? null
          : current,
    )
  }

  /*
   * ==========================================================
   * SCENE POINTER DOWN
   * ==========================================================
   */

  const handleScenePointerDown = (
    event: PointerEvent<HTMLDivElement>,
  ) => {
    const point =
      screenToWorld(
        event.clientX,
        event.clientY,
      )

    if (!point) {
      return
    }

    setCursor(point)

    /*
     * BODY TOOL
     */

    if (tool === 'body') {
      createBody(point)

      return
    }

    /*
     * PAN TOOL
     */

    if (tool === 'pan') {
      event.currentTarget.setPointerCapture(
        event.pointerId,
      )

      setDragging(true)

      lastPointer.current = {
        x: event.clientX,
        y: event.clientY,
      }

      return
    }

    /*
     * SELECT TOOL
     *
     * Clicking empty space
     * deselects the current object.
     */

    if (tool === 'select') {
      setSelectedObjectId(null)
    }
  }

  /*
   * ==========================================================
   * SCENE POINTER MOVE
   * ==========================================================
   */

  const handleScenePointerMove = (
    event: PointerEvent<HTMLDivElement>,
  ) => {
    const point =
      screenToWorld(
        event.clientX,
        event.clientY,
      )

    if (point) {
      setCursor(point)
    }

    /*
     * DRAG OBJECT
     */

    if (draggingObjectId) {
      const dx =
        (event.clientX -
          lastPointer.current.x) /
        view.zoom

      const dy =
        (event.clientY -
          lastPointer.current.y) /
        view.zoom

      setObjects(
        (current) =>
          current.map(
            (object) => {
              if (
                object.id !==
                draggingObjectId
              ) {
                return object
              }

              return {
                ...object,

                x:
                  object.x + dx,

                y:
                  object.y - dy,
              }
            },
          ),
      )

      lastPointer.current = {
        x: event.clientX,
        y: event.clientY,
      }

      return
    }

    /*
     * PAN SCENE
     */

    if (!dragging) {
      return
    }

    const dx =
      event.clientX -
      lastPointer.current.x

    const dy =
      event.clientY -
      lastPointer.current.y

    setView(
      (current) => ({
        ...current,

        x:
          current.x + dx,

        y:
          current.y + dy,
      }),
    )

    lastPointer.current = {
      x: event.clientX,
      y: event.clientY,
    }
  }

  /*
   * ==========================================================
   * POINTER UP
   * ==========================================================
   */

  const handleScenePointerUp = (
    event: PointerEvent<HTMLDivElement>,
  ) => {
    try {
      event.currentTarget.releasePointerCapture(
        event.pointerId,
      )
    } catch {
      // Already released.
    }

    setDragging(false)

    setDraggingObjectId(null)
  }

  /*
   * ==========================================================
   * OBJECT POINTER DOWN
   * ==========================================================
   */

  const handleObjectPointerDown = (
    event: PointerEvent<HTMLDivElement>,
    objectId: string,
  ) => {
    event.stopPropagation()

    /*
     * DELETE
     */

    if (tool === 'delete') {
      deleteObject(objectId)

      return
    }

    /*
     * SELECT + DRAG
     */

    if (tool === 'select') {
      setSelectedObjectId(
        objectId,
      )

      event.currentTarget.setPointerCapture(
        event.pointerId,
      )

      setDraggingObjectId(
        objectId,
      )

      lastPointer.current = {
        x: event.clientX,
        y: event.clientY,
      }
    }
  }

  /*
   * ==========================================================
   * WHEEL / ZOOM
   * ==========================================================
   */

  const handleWheel = (
    event: WheelEvent<HTMLDivElement>,
  ) => {
    event.preventDefault()

    const factor =
      event.deltaY < 0
        ? 1.1
        : 0.9

    setView(
      (current) => ({
        ...current,

        zoom: Math.min(
          10,

          Math.max(
            0.1,

            current.zoom *
              factor,
          ),
        ),
      }),
    )
  }

  /*
   * ==========================================================
   * VIEW CONTROLS
   * ==========================================================
   */

  const resetView = () => {
    setView({
      x: 0,
      y: 0,
      zoom: 1,
    })

    setCursor({
      x: 0,
      y: 0,
    })
  }

  const zoomIn = () => {
    setView(
      (current) => ({
        ...current,

        zoom: Math.min(
          10,

          current.zoom *
            1.2,
        ),
      }),
    )
  }

  const zoomOut = () => {
    setView(
      (current) => ({
        ...current,

        zoom: Math.max(
          0.1,

          current.zoom *
            0.8,
        ),
      }),
    )
  }

  /*
   * ==========================================================
   * TOOL SELECTION
   * ==========================================================
   */

  const selectTool = (
    nextTool: Tool,
  ) => {
    setTool(nextTool)

    setDragging(false)

    setDraggingObjectId(null)

    if (nextTool !== 'select') {
      setSelectedObjectId(null)
    }
  }

  /*
   * ==========================================================
   * RENDER
   * ==========================================================
   */

  return (
    <div
      ref={sceneRef}
      className={[
        'simulation-scene',

        dragging
          ? 'dragging'
          : '',

        `tool-${tool}`,
      ].join(' ')}
      onPointerDown={
        handleScenePointerDown
      }
      onPointerMove={
        handleScenePointerMove
      }
      onPointerUp={
        handleScenePointerUp
      }
      onPointerCancel={
        handleScenePointerUp
      }
      onWheel={
        handleWheel
      }
    >
      {/* ====================================================
          WORLD
          ==================================================== */}

      <div
        className="scene-world"
        style={{
          transform: `
            translate(
              ${view.x}px,
              ${view.y}px
            )
            scale(${view.zoom})
          `,
        }}
      >
        {/* Grid */}

        <div className="scene-grid" />

        {/* Axes */}

        <div
          className="scene-axis axis-x"
        />

        <div
          className="scene-axis axis-y"
        />

        {/* Origin */}

        <div className="origin">
          <div className="origin-dot" />
        </div>

        {/* Axis labels */}

        <div className="axis-label axis-label-x">
          x
        </div>

        <div className="axis-label axis-label-y">
          y
        </div>

        {/* =================================================
            OBJECTS
            ================================================= */}

        {objects.map(
          (object) => (
            <div
              key={object.id}
              className={[
                'scene-object',

                selectedObjectId ===
                object.id
                  ? 'selected'
                  : '',
              ].join(' ')}
              style={{
                left:
                  `${object.x}px`,

                top:
                  `${-object.y}px`,
              }}
              onPointerDown={(
                event,
              ) =>
                handleObjectPointerDown(
                  event,
                  object.id,
                )
              }
              onPointerMove={
                handleScenePointerMove
              }
              onPointerUp={
                handleScenePointerUp
              }
              onPointerCancel={
                handleScenePointerUp
              }
              title={
                object.name
              }
            >
              <div className="scene-object-dot" />
            </div>
          ),
        )}
      </div>

      {/* ====================================================
          TOOLBAR
          ==================================================== */}

      <div
        className="scene-toolbar"
        onPointerDown={(event) =>
          event.stopPropagation()
        }
      >
        {/* Select */}

        <button
          type="button"
          className={
            tool === 'select'
              ? 'active'
              : ''
          }
          onClick={() =>
            selectTool(
              'select',
            )
          }
          title="Select"
        >
          ↖
        </button>

        {/* Body */}

        <button
          type="button"
          className={
            tool === 'body'
              ? 'active'
              : ''
          }
          onClick={() =>
            selectTool(
              'body',
            )
          }
          title="Add body"
        >
          ●
        </button>

        {/* Pan */}

        <button
          type="button"
          className={
            tool === 'pan'
              ? 'active'
              : ''
          }
          onClick={() =>
            selectTool(
              'pan',
            )
          }
          title="Pan"
        >
          ✋
        </button>

        {/* Delete */}

        <button
          type="button"
          className={
            tool === 'delete'
              ? 'active danger'
              : ''
          }
          onClick={() =>
            selectTool(
              'delete',
            )
          }
          title="Delete"
        >
          ×
        </button>
      </div>

      {/* ====================================================
          UI OVERLAY
          ==================================================== */}

      <div
        className="scene-overlay"
        onPointerDown={(event) =>
          event.stopPropagation()
        }
      >
        {/* Coordinates */}

        <div className="cursor-coordinates">
          <span>x:</span>

          <span>
            {cursor.x.toFixed(2)}
          </span>

          <span>y:</span>

          <span>
            {cursor.y.toFixed(2)}
          </span>
        </div>

        {/* Controls */}

        <div className="scene-controls">
          <button
            type="button"
            onClick={
              resetView
            }
            title="Reset view"
          >
            ↻
          </button>

          <button
            type="button"
            onClick={
              zoomIn
            }
            title="Zoom in"
          >
            +
          </button>

          <button
            type="button"
            onClick={
              zoomOut
            }
            title="Zoom out"
          >
            −
          </button>
        </div>

        {/* Zoom */}

        <div className="zoom-indicator">
          {Math.round(
            view.zoom * 100,
          )}
          %
        </div>
      </div>
    </div>
  )
}

export default SimulationScene