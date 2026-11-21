"""Pixel canvas: an RGB bytearray with span-based drawing helpers.

Standard library only, no per-pixel Python loops on the hot paths:
fills work on whole rows, discs and polygons on row spans. Only small
translucent elements (glow, beams, clouds) blend per pixel.
"""

import math

from palette import lerp_stops


class Canvas:
    def __init__(self, width, height, rgb=(0, 0, 0)):
        self.width = width
        self.height = height
        self.buf = bytearray(bytes(rgb) * (width * height))

    def _off(self, x, y):
        return (y * self.width + x) * 3

    def set_pixel(self, x, y, rgb):
        if 0 <= x < self.width and 0 <= y < self.height:
            o = self._off(x, y)
            self.buf[o:o + 3] = bytes(rgb)

    def blend_pixel(self, x, y, rgb, alpha):
        """Alpha-composite rgb over the pixel; alpha 0..255."""
        if alpha <= 0 or not (0 <= x < self.width and 0 <= y < self.height):
            return
        if alpha >= 255:
            self.set_pixel(x, y, rgb)
            return
        o = self._off(x, y)
        inv = 255 - alpha
        self.buf[o] = (rgb[0] * alpha + self.buf[o] * inv) // 255
        self.buf[o + 1] = (rgb[1] * alpha + self.buf[o + 1] * inv) // 255
        self.buf[o + 2] = (rgb[2] * alpha + self.buf[o + 2] * inv) // 255

    def fill_rect(self, x0, y0, x1, y1, rgb):
        """Fill [x0, x1) x [y0, y1), clipped to the canvas."""
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.width, x1)
        y1 = min(self.height, y1)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(rgb) * (x1 - x0)
        for y in range(y0, y1):
            o = self._off(x0, y)
            self.buf[o:o + len(row)] = row

    def blend_rect(self, x0, y0, x1, y1, rgb, alpha):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.width, x1)
        y1 = min(self.height, y1)
        if x1 <= x0 or y1 <= y0:
            return
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.blend_pixel(x, y, rgb, alpha)

    def vgrad(self, y0, y1, stops):
        """Vertical gradient across the full width, rows y0..y1-1."""
        y1 = min(y1, self.height)
        span = max(1, y1 - 1 - y0)
        for y in range(max(0, y0), y1):
            rgb = lerp_stops(stops, (y - y0) / span)
            o = self._off(0, y)
            self.buf[o:o + self.width * 3] = bytes(rgb) * self.width

    def disc(self, cx, cy, r, rgb, alpha=255):
        """Filled circle, optionally translucent."""
        if r <= 0:
            return
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            dd = r * r - dy * dy
            if dd < 0:
                continue
            dx = int(math.isqrt(dd))
            x0, x1 = cx - dx, cx + dx + 1
            if alpha >= 255:
                self.fill_rect(x0, y, x1, y + 1, rgb)
            else:
                for x in range(max(0, x0), min(self.width, x1)):
                    self.blend_pixel(x, y, rgb, alpha)

    def radial_glow(self, cx, cy, r, rgb, peak_alpha):
        """Soft radial glow: alpha falls linearly from centre to edge."""
        for y in range(max(0, cy - r), min(self.height, cy + r + 1)):
            dy = y - cy
            dd = r * r - dy * dy
            if dd < 0:
                continue
            dx = int(math.isqrt(dd))
            for x in range(max(0, cx - dx), min(self.width, cx + dx + 1)):
                d = math.sqrt((x - cx) * (x - cx) + dy * dy)
                a = int(peak_alpha * (1.0 - d / r))
                if a > 0:
                    self.blend_pixel(x, y, rgb, a)

    def polygon(self, points, rgb, alpha=255):
        """Scanline-filled polygon (even-odd, pairs of crossings)."""
        if not points:
            return
        ys = [p[1] for p in points]
        y_lo = max(0, min(ys))
        y_hi = min(self.height - 1, max(ys))
        n = len(points)
        for y in range(y_lo, y_hi + 1):
            xs = []
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            if len(xs) < 2:
                continue
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                x0 = int(xs[k])
                x1 = int(xs[k + 1]) + 1
                if alpha >= 255:
                    self.fill_rect(x0, y, x1, y + 1, rgb)
                else:
                    for x in range(max(0, x0), min(self.width, x1)):
                        self.blend_pixel(x, y, rgb, alpha)

    def line(self, x0, y0, x1, y1, rgb, width=1):
        """Bresenham line; width 2 also fills the pixel below each step."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.fill_rect(x, y, x + width, y + width, rgb)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy
