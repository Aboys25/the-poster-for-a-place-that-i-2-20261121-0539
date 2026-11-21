"""Minimal standard-library PNG encoder (zlib + struct + crc32).

Writes a true-colour (colour type 2, bit depth 8) PNG. Every scanline
uses filter 1 (Sub): with smooth gradients and flat shapes the horizontal
differences are near zero, so the deflate stream stays small. Deterministic:
same pixels always produce the same bytes.
"""

import struct
import zlib


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(width, height, rgb_bytes):
    """Encode row-major RGB bytes (length width*height*3) as a PNG."""
    if len(rgb_bytes) != width * height * 3:
        raise ValueError("rgb buffer has the wrong length")
    stride = width * 3
    raw = bytearray()
    for y in range(height):
        row = rgb_bytes[y * stride:(y + 1) * stride]
        filtered = bytearray(stride)
        for i in range(stride):
            left = row[i - 3] if i >= 3 else 0
            filtered[i] = (row[i] - left) & 0xFF
        raw.append(1)
        raw += filtered
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))
