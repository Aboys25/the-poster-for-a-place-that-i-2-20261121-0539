"""Assemble the Velmara poster and return its PNG bytes."""

from canvas import Canvas
from pngwrite import encode_png
from scene import W, H, draw_velmara


def build_poster_png():
    """Paint the scene on a 1024x1024 canvas and encode it as PNG."""
    canvas = Canvas(W, H)
    draw_velmara(canvas)
    return encode_png(W, H, bytes(canvas.buf))
