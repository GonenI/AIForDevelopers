from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict


class ColorAdjustDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk | tk.Toplevel,
        initial: Dict[str, float],
        on_change: Callable[[str, float], None],
        on_apply: Callable[[Dict[str, float]], None],
        on_cancel: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self.title("Color Correction")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._on_change = on_change
        self._on_apply = on_apply
        self._on_cancel = on_cancel

        self._vars: Dict[str, tk.DoubleVar] = {
            "brightness": tk.DoubleVar(value=initial.get("brightness", 1.0)),
            "contrast": tk.DoubleVar(value=initial.get("contrast", 1.0)),
            "saturation": tk.DoubleVar(value=initial.get("saturation", 1.0)),
            "sharpness": tk.DoubleVar(value=initial.get("sharpness", 1.0)),
        }

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        def add_slider(name: str, label: str) -> None:
            row = ttk.Frame(frm)
            row.pack(fill=tk.X, pady=6)
            ttk.Label(row, text=label, width=12).pack(side=tk.LEFT)
            scale = ttk.Scale(row, from_=0.0, to=2.0, variable=self._vars[name], orient=tk.HORIZONTAL, length=260)
            scale.pack(side=tk.LEFT, padx=8)
            ttk.Label(row, textvariable=self._vars[name], width=5).pack(side=tk.LEFT)

            def on_release(_e: tk.Event) -> None:
                self._on_change(name, float(self._vars[name].get()))

            scale.bind("<ButtonRelease-1>", on_release)

        add_slider("brightness", "Brightness")
        add_slider("contrast", "Contrast")
        add_slider("saturation", "Saturation")
        add_slider("sharpness", "Sharpness")

        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(btns, text="Reset", command=self._reset).pack(side=tk.LEFT)
        ttk.Button(btns, text="Cancel", command=self._cancel).pack(side=tk.RIGHT)
        ttk.Button(btns, text="Apply", command=self._apply).pack(side=tk.RIGHT, padx=(0, 6))

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.wait_visibility()
        self.focus_set()

    def _reset(self) -> None:
        for k, var in self._vars.items():
            var.set(1.0)
            self._on_change(k, 1.0)

    def _apply(self) -> None:
        values = {k: float(v.get()) for k, v in self._vars.items()}
        self._on_apply(values)
        self.destroy()

    def _cancel(self) -> None:
        self._on_cancel()
        self.destroy()
