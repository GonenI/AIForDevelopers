from __future__ import annotations

from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def _ensure_rgba(img: Image.Image) -> Image.Image:
    return img if img.mode == "RGBA" else img.convert("RGBA")


def grayscale(img: Image.Image) -> Image.Image:
    base = _ensure_rgba(img)
    rgb = base.convert("RGB").convert("L").convert("RGB")
    return Image.merge("RGBA", (*rgb.split(), base.split()[-1]))


def sepia(img: Image.Image) -> Image.Image:
    base = _ensure_rgba(img)
    r, g, b, a = base.split()
    rgb = Image.merge("RGB", (r, g, b))
    sep = rgb.convert("RGB")
    pixels = sep.load()
    assert pixels is not None
    w, h = sep.size
    for y in range(h):
        for x in range(w):
            pr, pg, pb = pixels[x, y]
            tr = int(0.393 * pr + 0.769 * pg + 0.189 * pb)
            tg = int(0.349 * pr + 0.686 * pg + 0.168 * pb)
            tb = int(0.272 * pr + 0.534 * pg + 0.131 * pb)
            pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
    return Image.merge("RGBA", (*sep.split(), a))


def invert(img: Image.Image) -> Image.Image:
    base = _ensure_rgba(img)
    r, g, b, a = base.split()
    inv_rgb = ImageOps.invert(Image.merge("RGB", (r, g, b)))
    return Image.merge("RGBA", (*inv_rgb.split(), a))


def blur(img: Image.Image, radius: float = 2.0) -> Image.Image:
    base = _ensure_rgba(img)
    return base.filter(ImageFilter.GaussianBlur(radius))


def sharpen(img: Image.Image) -> Image.Image:
    base = _ensure_rgba(img)
    return base.filter(ImageFilter.SHARPEN)


def brightness(img: Image.Image, factor: float) -> Image.Image:
    base = _ensure_rgba(img)
    return ImageEnhance.Brightness(base).enhance(factor)


def contrast(img: Image.Image, factor: float) -> Image.Image:
    base = _ensure_rgba(img)
    return ImageEnhance.Contrast(base).enhance(factor)


def saturation(img: Image.Image, factor: float) -> Image.Image:
    base = _ensure_rgba(img)
    return ImageEnhance.Color(base).enhance(factor)


def sharpness(img: Image.Image, factor: float) -> Image.Image:
    base = _ensure_rgba(img)
    return ImageEnhance.Sharpness(base).enhance(factor)
