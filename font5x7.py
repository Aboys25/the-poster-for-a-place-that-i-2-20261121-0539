"""5x7 bitmap font for the poster's place name.

One glyph per capital letter, 7 rows of 5 bits, drawn as scaled blocks so
the name stays crisp and readable even when the poster is shrunk to a
thumbnail. Only A-Z and space are needed; the full alphabet is defined so
the name can change without touching the font.
"""

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}

GLYPH_W = 5
GLYPH_H = 7


def text_width(text, scale, gap):
    """Pixel width of text at the given glyph scale and inter-glyph gap."""
    if not text:
        return 0
    return len(text) * GLYPH_W * scale + (len(text) - 1) * gap


def draw_text(canvas, text, x, y, scale, rgb, gap=None, shadow=None,
              shadow_dx=0, shadow_dy=0):
    """Draw text with 5x7 glyphs; each set bit is a scale x scale block.

    When shadow is given, the same glyphs are drawn first in the shadow
    colour, offset by (shadow_dx, shadow_dy), so the letters lift off the
    sky instead of looking pasted on.
    """
    if gap is None:
        gap = scale
    if shadow is not None:
        _draw_glyphs(canvas, text, x + shadow_dx, y + shadow_dy, scale,
                     shadow, gap)
    _draw_glyphs(canvas, text, x, y, scale, rgb, gap)


def _draw_glyphs(canvas, text, x, y, scale, rgb, gap):
    cx = x
    for ch in text:
        glyph = FONT.get(ch)
        if glyph is None:
            raise ValueError("no glyph for %r" % (ch,))
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    canvas.fill_rect(cx + col * scale, y + row * scale,
                                     cx + (col + 1) * scale,
                                     y + (row + 1) * scale, rgb)
        cx += GLYPH_W * scale + gap
