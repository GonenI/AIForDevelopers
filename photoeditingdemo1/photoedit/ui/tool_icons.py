from __future__ import annotations
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

FG = "#E6E6E6"
BG = (0, 0, 0, 0)  # transparent
STROKE = 2


def _make_icon(draw_fn, size=24):
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)
    draw_fn(draw, size)
    return ImageTk.PhotoImage(img)


def open_icon(size=24, color: str = FG):
    def draw_open(d: ImageDraw.ImageDraw, s: int):
        # Folder: tab + body outline
        d.rectangle((4, 9, s - 4, s - 5), outline=color, width=STROKE)
        d.rectangle((4, 6, s // 2, 11), outline=color, width=STROKE)
    return _make_icon(draw_open, size)


def save_icon(size=24, color: str = FG):
    def draw_save(d: ImageDraw.ImageDraw, s: int):
        # Floppy disk
        d.rectangle((4, 4, s - 4, s - 4), outline=color, width=STROKE)
        d.rectangle((7, 7, s - 7, 11), outline=color, width=STROKE)  # label area
        d.rectangle((s - 10, 7, s - 7, 12), outline=color, width=STROKE)  # notch
    return _make_icon(draw_save, size)


def undo_icon(size=24, color: str = FG):
    def draw_undo(d: ImageDraw.ImageDraw, s: int):
        d.arc((5, 5, s - 5, s - 5), start=45, end=225, fill=color, width=STROKE)
        # arrowhead left
        d.polygon([(6, s // 2), (11, s // 2 - 4), (11, s // 2 + 4)], outline=color, fill=color)
    return _make_icon(draw_undo, size)


def redo_icon(size=24, color: str = FG):
    def draw_redo(d: ImageDraw.ImageDraw, s: int):
        d.arc((5, 5, s - 5, s - 5), start=315, end=135, fill=color, width=STROKE)
        # arrowhead right
        d.polygon([(s - 6, s // 2), (s - 11, s // 2 - 4), (s - 11, s // 2 + 4)], outline=color, fill=color)
    return _make_icon(draw_redo, size)


def rotate_left_icon(size=24, color: str = FG):
    def draw_rot_l(d: ImageDraw.ImageDraw, s: int):
        d.arc((4, 4, s - 4, s - 4), start=0, end=270, fill=color, width=STROKE)
        d.polygon([(8, 8), (14, 8), (8, 14)], outline=color, fill=color)  # arrowhead to indicate left
    return _make_icon(draw_rot_l, size)


def rotate_right_icon(size=24, color: str = FG):
    def draw_rot_r(d: ImageDraw.ImageDraw, s: int):
        d.arc((4, 4, s - 4, s - 4), start=180, end=90, fill=color, width=STROKE)
        d.polygon([(s - 8, 8), (s - 14, 8), (s - 8, 14)], outline=color, fill=color)
    return _make_icon(draw_rot_r, size)


def flip_h_icon(size=24, color: str = FG):
    def draw_fh(d: ImageDraw.ImageDraw, s: int):
        mid = s // 2
        d.line((mid, 4, mid, s - 4), fill=color, width=STROKE)
        # left arrow
        d.polygon([(4, mid), (10, mid - 4), (10, mid + 4)], outline=color, fill=color)
        # right arrow
        d.polygon([(s - 4, mid), (s - 10, mid - 4), (s - 10, mid + 4)], outline=color, fill=color)
    return _make_icon(draw_fh, size)


def flip_v_icon(size=24, color: str = FG):
    def draw_fv(d: ImageDraw.ImageDraw, s: int):
        mid = s // 2
        d.line((4, mid, s - 4, mid), fill=color, width=STROKE)
        # up arrow
        d.polygon([(mid, 4), (mid - 4, 10), (mid + 4, 10)], outline=color, fill=color)
        # down arrow
        d.polygon([(mid, s - 4), (mid - 4, s - 10), (mid + 4, s - 10)], outline=color, fill=color)
    return _make_icon(draw_fv, size)


def resize_icon(size=24, color: str = FG):
    def draw_resize(d: ImageDraw.ImageDraw, s: int):
        # diagonal arrows
        d.line((5, s - 5, s - 5, 5), fill=color, width=STROKE)
        d.polygon([(5, s - 9), (9, s - 9), (5, s - 5)], outline=color, fill=color)
        d.polygon([(s - 5, 5), (s - 9, 5), (s - 5, 9)], outline=color, fill=color)
    return _make_icon(draw_resize, size)


def brush_small_icon(size=24, color: str = FG):
    def draw_small(d: ImageDraw.ImageDraw, s: int):
        r = 3
        d.ellipse((s // 2 - r, s // 2 - r, s // 2 + r, s // 2 + r), outline=color, fill=color)
    return _make_icon(draw_small, size)


def brush_large_icon(size=24, color: str = FG):
    def draw_large(d: ImageDraw.ImageDraw, s: int):
        r = 7
        d.ellipse((s // 2 - r, s // 2 - r, s // 2 + r, s // 2 + r), outline=color, fill=color)
    return _make_icon(draw_large, size)


def text_icon(size=24, color: str = FG):
    def draw_text(d: ImageDraw.ImageDraw, s: int):
        try:
            font = ImageFont.truetype("arial.ttf", s // 2 + 4)
        except Exception:
            font = ImageFont.load_default()
        bbox = d.textbbox((0, 0), "T", font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((s - w) // 2, (s - h) // 2), "T", fill=color, font=font)
    return _make_icon(draw_text, size)


def rect_icon(size=24, color: str = FG):
    def draw_rect(d: ImageDraw.ImageDraw, s: int):
        d.rectangle((4, 4, s - 4, s - 4), outline=color, width=STROKE)
    return _make_icon(draw_rect, size)


def ellipse_icon(size=24, color: str = FG):
    def draw_ellipse(d: ImageDraw.ImageDraw, s: int):
        d.ellipse((4, 4, s - 4, s - 4), outline=color, width=STROKE)
    return _make_icon(draw_ellipse, size)


def select_icon(size=24, color: str = FG):
    def draw_select(d: ImageDraw.ImageDraw, s: int):
        # draw a dashed rectangle (simulate dashes by short lines)
        pad = 4
        dash_len = 3
        gap = 2
        # top and bottom
        x0, y0, x1, y1 = pad, pad, s - pad, s - pad
        x = x0
        while x < x1:
            d.line((x, y0, min(x + dash_len, x1), y0), fill=color, width=STROKE)
            d.line((x, y1, min(x + dash_len, x1), y1), fill=color, width=STROKE)
            x += dash_len + gap
        y = y0
        while y < y1:
            d.line((x0, y, x0, min(y + dash_len, y1)), fill=color, width=STROKE)
            d.line((x1, y, x1, min(y + dash_len, y1)), fill=color, width=STROKE)
            y += dash_len + gap
    return _make_icon(draw_select, size)
