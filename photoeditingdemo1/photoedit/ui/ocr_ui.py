from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional
from PIL import Image

from photoedit import ocr as backend


def is_ocr_available() -> bool:
    """Return whether the OCR backend (easyocr) is available."""
    return backend.is_ocr_available()


def extract_and_show(parent: tk.Misc, img: Optional[Image.Image], lang: str = "en") -> None:
    """Run OCR on `img` using the backend and show a dialog with results.

    This function handles user-facing errors and builds the dialog UI.
    """
    if not backend.is_ocr_available():
        messagebox.showerror("Error", "easyocr is not installed. Please install it to use OCR functionality.", parent=parent)
        return
    if img is None:
        messagebox.showwarning("No Image", "Please open an image first.", parent=parent)
        return

    try:
        text = backend.extract_text(img, lang=lang)
        _show_extracted_text(parent, text)
    except Exception as e:
        messagebox.showerror("OCR Error", f"Failed to extract text from image:\n{str(e)}", parent=parent)


def _show_extracted_text(parent: tk.Misc, text: str) -> None:
    """Display the extracted text in a dialog window."""
    dialog = tk.Toplevel(parent)
    dialog.title("Extracted Text")
    dialog.geometry("600x400")
    dialog.resizable(True, True)
    dialog.configure(bg="#1E1E1E")

    text_frame = tk.Frame(dialog, bg="#1E1E1E")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    text_widget = tk.Text(
        text_frame,
        bg="#000000",
        fg="#E6E6E6",
        insertbackground="#E6E6E6",
        selectbackground="#333333",
        font=("Consolas", 11),
        wrap=tk.WORD,
    )
    scrollbar = tk.Scrollbar(text_frame, bg="#333333", troughcolor="#1E1E1E")

    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_widget.yview)

    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    if text.strip():
        text_widget.insert(tk.END, text)
    else:
        text_widget.insert(tk.END, "No text was detected in the image.")

    text_widget.config(state=tk.DISABLED)

    btn_frame = tk.Frame(dialog, bg="#1E1E1E")
    btn_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

    def copy_text() -> None:
        dialog.clipboard_clear()
        dialog.clipboard_append(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!", parent=dialog)

    copy_btn = tk.Button(
        btn_frame,
        text="Copy to Clipboard",
        command=copy_text,
        bg="#333333",
        fg="#E6E6E6",
        relief=tk.FLAT,
        padx=12,
        pady=6,
        activebackground="#555555",
        activeforeground="#FFFFFF",
    )
    copy_btn.pack(side=tk.LEFT, padx=(0, 8))

    close_btn = tk.Button(
        btn_frame,
        text="Close",
        command=dialog.destroy,
        bg="#333333",
        fg="#E6E6E6",
        relief=tk.FLAT,
        padx=12,
        pady=6,
        activebackground="#555555",
        activeforeground="#FFFFFF",
    )
    close_btn.pack(side=tk.RIGHT)

    dialog.transient(parent)
    dialog.grab_set()
    dialog.focus_set()
