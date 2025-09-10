from __future__ import annotations

import tkinter as tk
from typing import Optional, Any, Callable
from PIL import Image


class PaintingController:
    """Simple painting controller for the canvas.

    It mutates the host image via provided callbacks and keeps brush state.
    """

    def __init__(
        self,
        get_committed: Callable[[], Optional[Image.Image]],
        set_committed: Callable[[Image.Image], None],
        push_undo: Callable[[], None],
        clear_redo: Callable[[], None],
        compose_preview: Callable[[], None],
        canvas_to_image: Callable[[int, int], tuple[int, int]],
        paint_panel: Optional[Any] = None,
    ) -> None:
        self.get_committed = get_committed
        self.set_committed = set_committed
        self.push_undo = push_undo
        self.clear_redo = clear_redo
        self.compose_preview = compose_preview
        self.canvas_to_image = canvas_to_image
        self.paint_panel = paint_panel

        # brush state
        self.brush_size: int = 8
        self.brush_color: str = "#000000"
        self.brush_alpha: float = 1.0

        # runtime state
        self.painting: bool = False
        self.last_pos: Optional[tuple[int, int]] = None

    def bind_canvas(self, canvas: tk.Canvas) -> None:
        canvas.bind("<ButtonPress-1>", self._on_start)
        canvas.bind("<B1-Motion>", self._on_drag)
        canvas.bind("<ButtonRelease-1>", self._on_end)

    # External setters used by UI panels
    def set_brush(self, name: str) -> None:
        self.brush_size = 8 if name == "small" else 24
        if self.paint_panel is not None and getattr(self.paint_panel, "_size", None) is not None:
            try:
                self.paint_panel._size.set(self.brush_size)
            except Exception:
                pass

    def set_brush_size(self, size: int) -> None:
        self.brush_size = size

    def set_brush_alpha(self, alpha: float) -> None:
        self.brush_alpha = alpha

    def set_color(self, color: str) -> None:
        self.brush_color = color
        if self.paint_panel is not None and getattr(self.paint_panel, "set_color", None):
            try:
                self.paint_panel.set_color(color)
            except Exception:
                pass

    # Canvas event handlers
    def _on_drag(self, event: tk.Event) -> None:
        if not self.painting or self.get_committed() is None or self.last_pos is None:
            return
        ix0, iy0 = self.canvas_to_image(*self.last_pos)
        ix1, iy1 = self.canvas_to_image(event.x, event.y)
        overlay = Image.new("RGBA", self.get_committed().size, (0, 0, 0, 0))
        from PIL import ImageDraw

        draw = ImageDraw.Draw(overlay, "RGBA")
        r, g, b = self._hex_to_rgb(self.brush_color)
        a = int(self.brush_alpha * 255)
        draw.line([ix0, iy0, ix1, iy1], fill=(r, g, b, a), width=self.brush_size)
        img = Image.alpha_composite(self.get_committed().convert("RGBA"), overlay)
        self.set_committed(img)
        self.compose_preview()
        self.last_pos = (event.x, event.y)

    def _on_start(self, event: tk.Event) -> None:
        self.painting = True
        self.last_pos = (event.x, event.y)

    def _on_end(self, event: tk.Event) -> None:
        self.painting = False
        self.last_pos = None
        try:
            self.push_undo()
            self.clear_redo()
        except Exception:
            pass

    def _hex_to_rgb(self, hexstr: str) -> tuple[int, int, int]:
        hexstr = hexstr.lstrip("#")
        r = int(hexstr[0:2], 16)
        g = int(hexstr[2:4], 16)
        b = int(hexstr[4:6], 16)
        return (r, g, b)
