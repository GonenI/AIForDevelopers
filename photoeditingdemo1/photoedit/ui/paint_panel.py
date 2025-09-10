from __future__ import annotations

import tkinter as tk
from tkinter import colorchooser
from typing import Callable

COMMON_COLORS = [
    "#000000", "#FFFFFF", "#FF0000", "#00FF00",
    "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
]

class PaintPanel(tk.Frame):
    def __init__(self, parent: tk.Misc, on_brush: Callable[[str], None], on_color: Callable[[str], None], on_size: Callable[[int], None], on_alpha: Callable[[float], None], on_select: Callable[[bool], None] | None = None) -> None:
        super().__init__(parent, bg="#000000", padx=8, pady=8)
        self._brush = tk.StringVar(value="small")
        self._color = tk.StringVar(value="#000000")
        self._size = tk.IntVar(value=8)
        self._alpha = tk.DoubleVar(value=1.0)
        self._on_brush = on_brush
        self._on_color = on_color
        self._on_size = on_size
        self._on_alpha = on_alpha
        self._on_select = on_select
        self._select_active = False
        self._build()

    def _build(self) -> None:
        # Compact icon row: small brush, large brush, and current-color box
        icon_frame = tk.Frame(self, bg="#000000")
        icon_frame.pack(pady=(0, 8))
        from photoedit.ui import tool_icons
        # Small and large brush icons
        self._icon_small = tool_icons.brush_small_icon(size=28)
        self._icon_large = tool_icons.brush_large_icon(size=28)
        # Put each control inside a 1px white border frame so items are visually separated
        small_border = tk.Frame(icon_frame, bg="#FFFFFF", bd=0)
        small_border.grid(row=0, column=0, padx=2, pady=2)
        self._icon_btn_small = tk.Button(
            small_border,
            image=self._icon_small,
            width=36,
            height=36,
            bg="#222",
            relief=tk.FLAT,
            command=lambda: self._set_brush("small", 8),
        )
        self._icon_btn_small.pack(padx=1, pady=1)

        large_border = tk.Frame(icon_frame, bg="#FFFFFF", bd=0)
        large_border.grid(row=0, column=1, padx=2, pady=2)
        self._icon_btn_large = tk.Button(
            large_border,
            image=self._icon_large,
            width=36,
            height=36,
            bg="#222",
            relief=tk.FLAT,
            command=lambda: self._set_brush("large", 24),
        )
        self._icon_btn_large.pack(padx=1, pady=1)

        color_border = tk.Frame(icon_frame, bg="#FFFFFF", bd=0)
        color_border.grid(row=0, column=2, padx=(6, 2), pady=2)
        # Current color box (click to open color chooser) - make same size as icon buttons
        self._color_btn = tk.Button(
            color_border,
            bg=self._color.get(),
            width=36,
            height=36,
            relief=tk.FLAT,
            command=self._open_color_picker,
            bd=0,
            highlightthickness=0,
        )
        self._color_btn.pack(padx=1, pady=1)

    # Select tool button (dashed rectangle icon)
        select_border = tk.Frame(icon_frame, bg="#FFFFFF", bd=0)
        select_border.grid(row=0, column=3, padx=(6, 2), pady=2)
        self._icon_select = tool_icons.select_icon(size=28)
        self._select_btn = tk.Button(
            select_border,
            image=self._icon_select,
            width=36,
            height=36,
            bg="#222",
            relief=tk.FLAT,
            command=self._toggle_select_mode,
        )
        self._select_btn.pack(padx=1, pady=1)

        # Thin brush size slider with label on the left and shorter slider on the right
        size_row = tk.Frame(self, bg="#000000")
        size_row.pack(fill=tk.X, pady=(0, 8))
        lbl_size = tk.Label(size_row, text="Size", width=8, anchor=tk.W, bg="#000000", fg="#E6E6E6", font=("Arial", 9))
        lbl_size.pack(side=tk.LEFT)
        size_slider = tk.Scale(
            size_row,
            from_=2,
            to=64,
            variable=self._size,
            orient=tk.HORIZONTAL,
            length=64,
            command=self._on_size_slider,
            bg="#000000",
            fg="#E6E6E6",
            highlightthickness=0,
            troughcolor="#333333",
            activebackground="#555555",
            sliderrelief=tk.FLAT,
            width=6,
        )
        size_slider.pack(side=tk.RIGHT, padx=(4, 0))

        # Opacity/alpha slider below controls with label on the left and shorter slider
        alpha_row = tk.Frame(self, bg="#000000")
        alpha_row.pack(fill=tk.X, pady=(4, 0))
        lbl_op = tk.Label(alpha_row, text="Opacity", width=8, anchor=tk.W, bg="#000000", fg="#E6E6E6", font=("Arial", 9))
        lbl_op.pack(side=tk.LEFT)
        alpha_slider = tk.Scale(
            alpha_row,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            variable=self._alpha,
            orient=tk.HORIZONTAL,
            length=64,
            command=self._on_alpha_slider,
            bg="#000000",
            fg="#E6E6E6",
            highlightthickness=0,
            troughcolor="#333333",
            activebackground="#555555",
            sliderrelief=tk.FLAT,
            width=6,
        )
        alpha_slider.pack(side=tk.RIGHT, padx=(4, 0))

    def _set_brush(self, name: str, val: int) -> None:
        self._brush.set(name)
        self._size.set(val)
        self._on_brush(name)
        self._on_size(val)

    def _on_size_slider(self, _val: str) -> None:
        self._on_size(self._size.get())

    def _on_alpha_slider(self, _val: str) -> None:
        self._on_alpha(self._alpha.get())

    def _open_color_picker(self) -> None:
        color = colorchooser.askcolor(color=self._color.get(), title="Choose Color")
        if color[1]:  # color[1] is the hex string
            # Update internal and UI, then notify parent
            self.set_color(color[1])
            self._on_color(color[1])

    def _toggle_select_mode(self) -> None:
        # toggle selection mode and notify parent
        self._select_active = not self._select_active
        # visual feedback
        self._select_btn.config(relief=tk.SUNKEN if self._select_active else tk.FLAT)
        if self._on_select:
            self._on_select(self._select_active)

    def set_select_active(self, active: bool) -> None:
        """Called by parent to set select button visual state."""
        self._select_active = bool(active)
        try:
            self._select_btn.config(relief=tk.SUNKEN if self._select_active else tk.FLAT)
        except Exception:
            pass


    def set_color(self, hexcolor: str) -> None:
        """Externally-updatable color setter that updates the UI."""
        self._color.set(hexcolor)
        try:
            # update color button appearance
            self._color_btn.config(bg=hexcolor, activebackground=hexcolor)
        except Exception:
            pass
