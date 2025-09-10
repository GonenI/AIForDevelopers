from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Optional, Any, Callable

from PIL import Image, ImageTk, ImageOps
from photoedit import filters as F
from photoedit.ui.color_dialog import ColorAdjustDialog
from photoedit.ui.paint_panel import PaintPanel
from photoedit.ui import tool_icons
from photoedit import ocr
from photoedit.ui import ocr_ui
from photoedit.ui.painting import PaintingController


def _resolve_resample() -> int:
    resampling = getattr(Image, "Resampling", None)
    if resampling is not None:
        return getattr(
            resampling,
            "LANCZOS",
            getattr(resampling, "BICUBIC", getattr(resampling, "BILINEAR", 0)),
        )
    return getattr(Image, "LANCZOS", getattr(Image, "BICUBIC", getattr(Image, "BILINEAR", 0)))


RESAMPLE: Any = _resolve_resample()


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Photo Editor - Stage 3")
        self.minsize(1000, 680)
        self._init_styles()

        # Image state
        self._image: Optional[Image.Image] = None  # preview/display image
        self._committed: Optional[Image.Image] = None  # original unmodified image
        self._photo: Optional[ImageTk.PhotoImage] = None
        self._image_path: Optional[str] = None
        self._dirty: bool = False

        # Undo/redo stacks
        self._undo_stack: list[Image.Image] = []
        self._redo_stack: list[Image.Image] = []

        # Track adjustment values
        self._adjust = {
            "brightness": 1.0,
            "contrast": 1.0,
            "saturation": 1.0,
            "sharpness": 1.0,
        }
        self._adj_vars: dict[str, tk.DoubleVar] = {}

        # Painting controller (encapsulates brush state & canvas handlers)
        self._painting_controller: Optional[PaintingController] = None

        # Selection state (rubber-band selection)
        self._selecting: bool = False
        self._selection_start: Optional[tuple[int, int]] = None  # canvas coords
        self._selection_rect_id: Optional[int] = None
        self._selection_image: Optional[Any] = None  # copied PIL image
        self._clipboard_image: Optional[Any] = None

        # Build UI
        self._build_menu()
        self._build_toolbar()
        self._build_layout()

        # keyboard bindings for copy/paste
        self.bind_all('<Control-c>', self._copy_selection)
        self.bind_all('<Control-C>', self._copy_selection)
        self.bind_all('<Control-v>', self._paste_selection)
        self.bind_all('<Control-V>', self._paste_selection)

        self._update_actions_enabled(False)
        self._update_title()
        self._update_undo_redo_buttons()

    def _init_styles(self) -> None:
        try:
            style = ttk.Style(self)
            # Ensure a theme is active
            current = style.theme_use()
            style.theme_use(current)
            # Dark base colors
            style.configure("Dark.TFrame", background="#1E1E1E")
            style.configure("Dark.TLabelframe", background="#1E1E1E", foreground="#E6E6E6")
            style.configure("Dark.TLabelframe.Label", background="#1E1E1E", foreground="#E6E6E6")
            style.configure("Dark.TLabel", background="#1E1E1E", foreground="#C8C8C8")
            style.configure("Dark.TRadiobutton", background="#1E1E1E", foreground="#E6E6E6")
            style.configure("Dark.Horizontal.TScale", background="#1E1E1E")
        except Exception:
            pass

    # Painting is handled by PaintingController bound to the canvas.


    # UI BUILDERS
    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._new_image)
        file_menu.add_command(label="Open...", command=self._open_image)
        file_menu.add_command(label="Save", command=self._save_image)
        file_menu.add_command(label="Save As...", command=self._save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Rotate Left 90°", command=self._rotate_left)
        edit_menu.add_command(label="Rotate Right 90°", command=self._rotate_right)
        edit_menu.add_separator()
        edit_menu.add_command(label="Flip Horizontal", command=self._flip_horizontal)
        edit_menu.add_command(label="Flip Vertical", command=self._flip_vertical)
        edit_menu.add_separator()
        edit_menu.add_command(label="Resize...", command=self._resize_image)
        edit_menu.add_separator()
        edit_menu.add_command(label="Color Correction...", command=self._open_color_correction)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Grayscale", command=lambda: self._apply_filter(F.grayscale))
        filters_menu.add_command(label="Sepia", command=lambda: self._apply_filter(F.sepia))
        filters_menu.add_command(label="Invert", command=lambda: self._apply_filter(F.invert))
        filters_menu.add_separator()
        filters_menu.add_command(label="Blur...", command=self._blur_dialog)
        menubar.add_cascade(label="Filters", menu=filters_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        if ocr_ui.is_ocr_available():
            tools_menu.add_command(label="Text Recognition (OCR)...", command=self._extract_text)
        else:
            tools_menu.add_command(label="Text Recognition (OCR)... [Unavailable]", state=tk.DISABLED)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        self.config(menu=menubar)

    def _build_toolbar(self) -> None:
        bar = tk.Frame(self, bd=1, relief=tk.FLAT, bg="#222222")
        bar.pack(side=tk.TOP, fill=tk.X)
        btn = tk.Button
        # Create icons using improved tool_icons
        self._icon_open = tool_icons.open_icon()
        self._icon_save = tool_icons.save_icon()
        self._icon_undo = tool_icons.undo_icon()
        self._icon_redo = tool_icons.redo_icon()
        self._icon_rl = tool_icons.rotate_left_icon()
        self._icon_rr = tool_icons.rotate_right_icon()
        self._icon_fh = tool_icons.flip_h_icon()
        self._icon_fv = tool_icons.flip_v_icon()
        self._icon_resize = tool_icons.resize_icon()
        # Buttons
        self._btn_open = btn(bar, image=self._icon_open, command=self._open_image, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_save = btn(bar, image=self._icon_save, command=self._save_image, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_save_as = btn(bar, image=self._icon_save, command=self._save_image_as, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_undo = btn(bar, image=self._icon_undo, command=self._undo, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_redo = btn(bar, image=self._icon_redo, command=self._redo, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_rl = btn(bar, image=self._icon_rl, command=self._rotate_left, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_rr = btn(bar, image=self._icon_rr, command=self._rotate_right, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_fh = btn(bar, image=self._icon_fh, command=self._flip_horizontal, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_fv = btn(bar, image=self._icon_fv, command=self._flip_vertical, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        self._btn_resize = btn(bar, image=self._icon_resize, command=self._resize_image, bg="#222222", relief=tk.FLAT, activebackground="#333333")
        for b in (
            self._btn_open,
            self._btn_save,
            self._btn_save_as,
            self._btn_undo,
            self._btn_redo,
            self._btn_rl,
            self._btn_rr,
            self._btn_fh,
            self._btn_fv,
            self._btn_resize,
        ):
            b.pack(side=tk.LEFT, padx=4, pady=4)

    def _build_layout(self) -> None:
        # Paned layout: left sidebar for controls, right canvas area
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6, bg="#000000")
        paned.pack(fill=tk.BOTH, expand=True)

        # Slim left sidebar (compact tools) - keep to ~80px max
        self._sidebar = tk.Frame(paned, bg="#000000", width=80)
        paned.add(self._sidebar, minsize=80)

        # Canvas container on the right
        canvas_container = tk.Frame(paned, bg="#111111")
        paned.add(canvas_container)
        self._canvas = tk.Canvas(canvas_container, bg="#222222", highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Configure>", self._on_resize)

        # Build the sidebar controls (paint panel will be created inside)
        self._build_sidebar(self._sidebar)

        # Instantiate painting controller and wire it with callbacks.
        try:
            self._painting_controller = PaintingController(
                get_committed=lambda: self._committed,
                set_committed=lambda img: setattr(self, "_committed", img),
                push_undo=self._push_undo,
                clear_redo=self._clear_redo,
                compose_preview=self._compose_preview,
                canvas_to_image=self._canvas_to_image,
                paint_panel=getattr(self, "_paint_panel", None),
            )
            if self._painting_controller is not None:
                self._painting_controller.bind_canvas(self._canvas)
        except Exception:
            self._painting_controller = None

    def _build_sidebar(self, parent: tk.Misc) -> None:
        parent.columnconfigure(0, weight=1)
        # Paint panel (brush + color grid + size + alpha)
        self._paint_panel = PaintPanel(
            parent,
            on_brush=lambda name: self._painting_controller.set_brush(name) if self._painting_controller else None,
            on_color=lambda color: self._painting_controller.set_color(color) if self._painting_controller else None,
            on_size=lambda size: self._painting_controller.set_brush_size(size) if self._painting_controller else None,
            on_alpha=lambda a: self._painting_controller.set_brush_alpha(a) if self._painting_controller else None,
            on_select=self._enter_select_mode,
        )
        self._paint_panel.pack(fill=tk.X, pady=8)

        # Removed quick filter and blur shortcut buttons for a cleaner UI

    # Color Correction dialog orchestration
    def _open_color_correction(self) -> None:
        if self._committed is None:
            return
        # snapshot current adjustment state so Cancel can revert
        snapshot = dict(self._adjust)

        def on_change(name: str, value: float) -> None:
            self._adjust[name] = float(value)
            self._compose_preview()

        def on_apply(values: dict[str, float]) -> None:
            # commit adjustments into base
            if any(v != 1.0 for v in values.values()):
                self._commit_current()
            self._dirty = True
            self._update_title()
            self._compose_preview()

        def on_cancel() -> None:
            # restore previous adjustment values and rebuild preview
            self._adjust.update(snapshot)
            self._compose_preview()

        ColorAdjustDialog(self, initial=self._adjust, on_change=on_change, on_apply=on_apply, on_cancel=on_cancel)

    # STATE MANAGEMENT
    def _update_actions_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for b in (
            self._btn_save,
            self._btn_save_as,
            self._btn_rl,
            self._btn_rr,
            self._btn_fh,
            self._btn_fv,
            self._btn_resize,
        ):
            b.config(state=state)

    def _update_title(self) -> None:
        name = self._image_path if self._image_path else "Untitled"
        star = "*" if self._dirty else ""
        self.title(f"Photo Editor - Stage 3 | {name}{star}")

    def _compose_preview(self) -> None:
        """Apply all current adjustments to committed image to create preview."""
        if self._committed is None:
            return
        
        img = self._committed
        adj = self._adjust
        
        # Apply adjustments in a fixed order
        if adj["brightness"] != 1.0:
            img = F.brightness(img, adj["brightness"])
        if adj["contrast"] != 1.0:
            img = F.contrast(img, adj["contrast"])
        if adj["saturation"] != 1.0:
            img = F.saturation(img, adj["saturation"])
        if adj["sharpness"] != 1.0:
            img = F.sharpness(img, adj["sharpness"])
        
        self._image = img
        self._render_image()

    def _push_undo(self) -> None:
        if self._committed is not None:
            self._undo_stack.append(self._committed.copy())
            self._update_undo_redo_buttons()

    def _clear_redo(self) -> None:
        self._redo_stack.clear()
        self._update_undo_redo_buttons()

    def _undo(self) -> None:
        if not self._undo_stack:
            return
        if self._committed is not None:
            self._redo_stack.append(self._committed.copy())
        self._committed = self._undo_stack.pop()
        self._compose_preview()
        self._update_undo_redo_buttons()
        self._dirty = True
        self._update_title()

    def _redo(self) -> None:
        if not self._redo_stack:
            return
        if self._committed is not None:
            self._undo_stack.append(self._committed.copy())
        self._committed = self._redo_stack.pop()
        self._compose_preview()
        self._update_undo_redo_buttons()
        self._dirty = True
        self._update_title()

    def _update_undo_redo_buttons(self) -> None:
        self._btn_undo.config(state=tk.NORMAL if self._undo_stack else tk.DISABLED)
        self._btn_redo.config(state=tk.NORMAL if self._redo_stack else tk.DISABLED)

    # FILE OPS
    def _open_image(self) -> None:
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
        if not path:
            return
        try:
            img = Image.open(path).convert("RGBA")
        except (OSError, ValueError) as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")
            return
            
        self._image_path = path
        self._dirty = False
        self._committed = img
        # Reset adjustments on new image
        for k in self._adjust:
            self._adjust[k] = 1.0
            if k in self._adj_vars:
                self._adj_vars[k].set(1.0)
        self._update_title()
        self._update_actions_enabled(True)
        self._compose_preview()

    def _save_image(self) -> None:
        if self._image is None:
            return
        if not self._image_path:
            self._save_image_as()
            return
        self._save_to_path(self._image_path)

    def _save_image_as(self) -> None:
        if self._image is None:
            return
        filetypes = [("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp")]
        path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".png", filetypes=filetypes)
        if not path:
            return
        self._image_path = path
        self._save_to_path(path)

    def _save_to_path(self, path: str) -> None:
        if self._committed is None:
            return
        try:
            # Ensure we save with current adjustments applied
            if any(v != 1.0 for v in self._adjust.values()):
                self._commit_current()
                
            ext = (path.rsplit(".", 1)[-1] or "").lower()
            img_to_save = self._committed
            if ext in {"jpg", "jpeg"}:
                # JPEG doesn't support alpha
                img_to_save = img_to_save.convert("RGB")
                img_to_save.save(path, format="JPEG", quality=95)
            elif ext == "bmp":
                img_to_save.save(path, format="BMP")
            else:
                img_to_save.save(path, format="PNG")
        except OSError as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")
            return
        self._dirty = False
        self._update_title()

    # RENDERING
    def _on_resize(self, _event: tk.Event) -> None:
        if self._image is None:
            return
        self._render_image()

    def _render_image(self) -> None:
        if self._image is None:
            return
        canvas_w = max(1, self._canvas.winfo_width())
        canvas_h = max(1, self._canvas.winfo_height())
        img_w, img_h = self._image.size
        scale = min(canvas_w / img_w, canvas_h / img_h)
        new_size = (max(1, int(img_w * scale)), max(1, int(img_h * scale)))
        resized = self._image.resize(new_size, RESAMPLE)
        self._photo = ImageTk.PhotoImage(resized)
        self._canvas.delete("all")
        x = (canvas_w - new_size[0]) // 2
        y = (canvas_h - new_size[1]) // 2
        self._canvas.create_image(x, y, anchor=tk.NW, image=self._photo)

    # EDIT ACTIONS
    def _rotate_left(self) -> None:
        if self._committed is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = self._committed.rotate(90, expand=True, resample=RESAMPLE)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _rotate_right(self) -> None:
        if self._committed is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = self._committed.rotate(-90, expand=True, resample=RESAMPLE)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _flip_horizontal(self) -> None:
        if self._committed is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = ImageOps.mirror(self._committed)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _flip_vertical(self) -> None:
        if self._committed is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = ImageOps.flip(self._committed)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _resize_image(self) -> None:
        if self._committed is None:
            return
        percent = simpledialog.askinteger(
            "Resize",
            "Scale percentage (10-400):",
            parent=self,
            minvalue=10,
            maxvalue=400,
        )
        if percent is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        w, h = self._committed.size
        new_size = (max(1, w * percent // 100), max(1, h * percent // 100))
        self._committed = self._committed.resize(new_size, RESAMPLE)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _apply_filter(self, func: Callable[[Image.Image], Image.Image]) -> None:
        if self._committed is None:
            return
        # Commit adjustments before filter
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = func(self._committed)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _apply_adjust(self, kind: str, factor: float) -> None:
        if self._committed is None or kind not in self._adjust:
            return
        self._adjust[kind] = float(factor)
        self._dirty = True
        self._update_title()
        self._compose_preview()

    def _reset_adjustments(self) -> None:
        """Reset all adjustments to neutral values."""
        if self._committed is None:
            return
            
        for k in self._adjust:
            self._adjust[k] = 1.0
            if k in self._adj_vars:
                self._adj_vars[k].set(1.0)
        self._compose_preview()

    def _blur_dialog(self) -> None:
        if self._committed is None:
            return
        val = simpledialog.askfloat(
            "Gaussian Blur",
            "Radius (0.1 - 20.0):",
            parent=self,
            minvalue=0.1,
            maxvalue=20.0,
        )
        if val is None:
            return
        if any(v != 1.0 for v in self._adjust.values()):
            self._commit_current()
        self._push_undo()
        self._clear_redo()
        self._committed = F.blur(self._committed, float(val))
        self._dirty = True
        self._update_title()
        self._compose_preview()

    # STATE MANAGEMENT
    def _commit_current(self) -> None:
        if self._image is None:
            return
        self._push_undo()
        self._committed = self._image
        self._clear_redo()
        for k in self._adjust:
            self._adjust[k] = 1.0
            if k in self._adj_vars:
                self._adj_vars[k].set(1.0)

    # Selection helpers
    def _enter_select_mode(self, _flag: bool = True) -> None:
        # activate selecting; UI panel already requested select mode
        self._selecting = True

    def _exit_select_mode(self) -> None:
        self._selecting = False
        self._selection_start = None
        if self._selection_rect_id is not None:
            try:
                self._canvas.delete(self._selection_rect_id)
            except Exception:
                pass
            self._selection_rect_id = None

    def _update_selection_rectangle(self, cx: int, cy: int) -> None:
        if self._selection_start is None:
            return
        x0, y0 = self._selection_start
        # create or update a dashed rectangle on the canvas overlay
        if self._selection_rect_id is not None:
            self._canvas.delete(self._selection_rect_id)
            self._selection_rect_id = None
        # use create_rectangle with dash pattern
        self._selection_rect_id = self._canvas.create_rectangle(x0, y0, cx, cy, outline="#FFFFFF", dash=(4, 3))

    def _finalize_selection(self, x0: int, y0: int, x1: int, y1: int) -> None:
        # Convert to image coords and store copied image
        if self._committed is None:
            self._exit_select_mode()
            return
        ix0, iy0 = self._canvas_to_image(x0, y0)
        ix1, iy1 = self._canvas_to_image(x1, y1)
        left, top = min(ix0, ix1), min(iy0, iy1)
        right, bottom = max(ix0, ix1), max(iy0, iy1)
        if left == right or top == bottom:
            self._exit_select_mode()
            return
        self._selection_image = self._committed.crop((left, top, right, bottom)).convert("RGBA")
        # keep the visual rectangle until user exits or copies
        self._exit_select_mode()

    def _copy_selection(self, _evt: tk.Event | None = None) -> None:
        # Copies selected image to internal clipboard (self._selection_image)
        if self._selection_image is None:
            return
        # Put on system clipboard as image if possible, else keep internal copy
        try:
            # Tkinter image clipboard tends to be platform dependent; keep internal copy
            self._clipboard_image = self._selection_image.copy()
        except Exception:
            self._clipboard_image = self._selection_image

    def _paste_selection(self, event: tk.Event | None = None) -> None:
        # Paste clipboard image at mouse position (canvas coords -> image coords)
        if not hasattr(self, "_clipboard_image") or self._clipboard_image is None or self._committed is None:
            return
        # determine mouse position
        mx, my = 0, 0
        try:
            if event is not None:
                mx, my = event.x, event.y
            else:
                # fallback: current mouse on canvas
                mx = self._canvas.winfo_pointerx() - self._canvas.winfo_rootx()
                my = self._canvas.winfo_pointery() - self._canvas.winfo_rooty()
        except Exception:
            pass
        ix, iy = self._canvas_to_image(mx, my)
        # Composite clipboard image onto committed at (ix, iy)
        overlay = Image.new("RGBA", self._committed.size, (0, 0, 0, 0))
        overlay.paste(self._clipboard_image, (ix, iy), self._clipboard_image)
        self._push_undo()
        self._clear_redo()
        self._committed = Image.alpha_composite(self._committed.convert("RGBA"), overlay)
        self._dirty = True
        self._compose_preview()

    def _canvas_to_image(self, x: int, y: int) -> tuple[int, int]:
        if self._image is None:
            return (0, 0)
        canvas_w = max(1, self._canvas.winfo_width())
        canvas_h = max(1, self._canvas.winfo_height())
        img_w, img_h = self._image.size
        scale = min(canvas_w / img_w, canvas_h / img_h)
        x_img = int((x - (canvas_w - img_w * scale) / 2) / scale)
        y_img = int((y - (canvas_h - img_h * scale) / 2) / scale)
        return (x_img, y_img)

    def _hex_to_rgb(self, hexstr: str) -> tuple[int, int, int]:
        hexstr = hexstr.lstrip('#')
        r = int(hexstr[0:2], 16)
        g = int(hexstr[2:4], 16)
        b = int(hexstr[4:6], 16)
        return (r, g, b)

    def _extract_text(self) -> None:
        """Delegate OCR extraction and display to the UI helper module."""
        ocr_ui.extract_and_show(self, self._committed, lang="en")

    def _new_image(self) -> None:
        """
        Date: 2024-01-20
        Creates a new black RGB image with dimensions 1024x1024 pixels.

        The method initializes both the working and committed image copies,
        clears the file path, marks the image as dirty, updates the UI title,
        refreshes the preview, enables relevant actions, and clears the undo/redo stacks.

        Returns:
            None
        """
        from PIL import Image
        img = Image.new("RGB", (1024, 1024), "black")
        self._image = img.copy()
        self._committed = img.copy()
        self._image_path = None
        self._dirty = True
        self._update_title()
        self._compose_preview()
        self._update_actions_enabled(True)
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._update_undo_redo_buttons()
     
