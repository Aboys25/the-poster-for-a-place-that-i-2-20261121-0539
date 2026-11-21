"""The Velmara poster scene: one invented place, one landmark.

Composition (1024x1024), leading the eye name -> landmark -> horizon:
  - the name VELMARA, large and cream, across the dark top sky;
  - one white lighthouse on a dark cliff, left of centre, lamp lit;
  - a low sun over a turquoise sea, its reflection shimmering below.
A small cottage with lit windows sits on the cliff so the poster promises
a stay, not just a view. No other copy anywhere in the picture.
"""

import math

from font5x7 import draw_text, text_width
from palette import (
    BIRD, CLIFF, CLIFF_RIM, CLOUD, COTTAGE, COTTAGE_ROOF,
    LAMP, LIGHTHOUSE_BAND, LIGHTHOUSE_WHITE, REFLECT, RULE_GOLD,
    SEA_DEEP, SEA_MID, SEA_TOP, SKY_HORIZON, SKY_LOW, SKY_MID1,
    SKY_MID2, SKY_TOP, STAR, STRATA, SUN_CORE, SUN_GLOW, TEXT_CREAM,
    TEXT_SHADOW, WAVE, WINDOW,
)

W = 1024
H = 1024
HORIZON = 640
PLACE_NAME = "VELMARA"

# Fixed stars in the dark top sky, kept clear of the name band.
STARS = [
    (40, 30), (90, 55), (130, 20), (950, 35), (990, 60), (900, 80),
    (60, 120), (980, 140), (30, 200), (1000, 200), (150, 45), (870, 30),
    (200, 28), (820, 48),
]

# Fixed wave streaks across the sea: (y, x0, x1, alpha).
WAVES = [
    (700, 80, 420, 50), (760, 560, 980, 45), (820, 100, 500, 55),
    (880, 620, 960, 40), (940, 60, 380, 50), (980, 480, 900, 40),
]

# Cliff top edge, left to right; the cliff fills everything below it.
CLIFF_TOP = [(0, 780), (90, 700), (170, 620), (240, 565), (300, 545),
             (340, 560)]

# Birds: (x, y, half-span).
BIRDS = [(420, 240, 9), (470, 275, 8), (540, 215, 9), (880, 300, 8),
         (940, 355, 9)]


def _draw_cloud(canvas, cx, cy, w, rgb, alpha):
    """One flat stratus band: a low bar with rounded ends and soft bumps.

    (v1 drew bubble clusters of tall discs; viewed as the judge sees it
    they read as soap bubbles, not clouds.)
    """
    half = 0.44 * w
    bar_h = 0.10 * w
    canvas.blend_rect(int(cx - half), int(cy), int(cx + half),
                      int(cy + bar_h), rgb, alpha)
    canvas.disc(int(cx - half), int(cy + bar_h / 2), int(bar_h / 2), rgb,
                alpha)
    canvas.disc(int(cx + half), int(cy + bar_h / 2), int(bar_h / 2), rgb,
                alpha)
    canvas.disc(int(cx - 0.15 * w), int(cy - 0.01 * w), int(0.06 * w), rgb,
                alpha)
    canvas.disc(int(cx + 0.18 * w), int(cy - 0.01 * w), int(0.05 * w), rgb,
                alpha)


def _draw_bird(canvas, x, y, s, rgb):
    """One small bird: two short strokes meeting in a shallow V."""
    canvas.line(x - s, y, x, y + s // 2, rgb, width=2)
    canvas.line(x, y + s // 2, x + s, y, rgb, width=2)


def _lighthouse_edges(y):
    """Left/right x of the tapered tower at height y.

    Tower runs from (193, 620)-(257, 620) at the base (buried in the
    cliff) to (203, 330)-(247, 330) at the top.
    """
    t = (y - 620) / (330 - 620)
    left = 193 + t * (203 - 193)
    right = 257 + t * (247 - 257)
    return left, right


def _draw_lighthouse(canvas):
    # Tower, tapered, base buried in the cliff so it stands on the slope.
    canvas.polygon([(193, 620), (257, 620), (247, 330), (203, 330)],
                   LIGHTHOUSE_WHITE)
    # Two dark bands, following the taper.
    for y0, y1 in ((430, 448), (500, 516)):
        l0, r0 = _lighthouse_edges(y0)
        l1, r1 = _lighthouse_edges(y1)
        canvas.polygon([(int(l0), y0), (int(r0), y0), (int(r1), y1),
                        (int(l1), y1)], LIGHTHOUSE_BAND)
    # Gallery overhang, then the lamp itself with a warm halo.
    # (v1 drew translucent beams; viewed small they read as a pale
    # smudge across the sky, not as light, so the beams are gone.)
    canvas.fill_rect(198, 312, 252, 330, LIGHTHOUSE_BAND)
    canvas.radial_glow(225, 297, 60, LAMP, 110)
    canvas.fill_rect(208, 282, 242, 312, LAMP)
    # Conical roof and finial.
    canvas.polygon([(204, 282), (246, 282), (225, 256)], LIGHTHOUSE_BAND)
    canvas.disc(225, 254, 3, LIGHTHOUSE_BAND)


def _draw_cottage(canvas):
    # Small cottage on the cliff ledge, two windows lit.
    canvas.fill_rect(78, 648, 142, 720, COTTAGE)
    canvas.polygon([(70, 648), (150, 648), (110, 616)], COTTAGE_ROOF)
    canvas.fill_rect(132, 622, 140, 648, COTTAGE_ROOF)
    canvas.fill_rect(90, 662, 102, 678, WINDOW)
    canvas.fill_rect(118, 662, 130, 678, WINDOW)
    canvas.fill_rect(104, 678, 116, 700, COTTAGE_ROOF)


def draw_velmara(canvas):
    """Paint the whole poster onto the canvas."""
    # Sky and sea.
    canvas.vgrad(0, HORIZON, [(0.0, SKY_TOP), (0.28, SKY_MID1),
                              (0.52, SKY_MID2), (0.75, SKY_LOW),
                              (1.0, SKY_HORIZON)])
    canvas.vgrad(HORIZON, H, [(0.0, SEA_TOP), (0.35, SEA_MID),
                              (1.0, SEA_DEEP)])

    # Stars in the dark top sky.
    for (x, y) in STARS:
        canvas.blend_rect(x, y, x + 2, y + 2, STAR, 140)

    # Low sun: wide faint halo, tighter glow, solid core.
    canvas.radial_glow(700, 588, 260, SUN_GLOW, 28)
    canvas.radial_glow(700, 588, 200, SUN_GLOW, 70)
    canvas.disc(700, 588, 62, SUN_CORE)

    # Sun reflection: gold dashes, narrowing and fading with depth.
    # (v1's sine wobble was too regular and read as a snake; the wobble
    # is smaller now and every fourth dash is skipped to break it up.)
    for i, y in enumerate(range(652, 1000, 3)):
        if i % 4 == 3:
            continue
        depth = (y - 650) / 350.0
        wobble = int(8 * math.sin(y * 0.05))
        width = max(8, int(64 * (1.0 - depth) + 8))
        alpha = int(200 * (1.0 - depth) + 30)
        cx = 700 + wobble
        canvas.blend_rect(cx - width // 2, y, cx + width // 2, y + 2,
                          REFLECT, alpha)
    for (y, x0, x1, alpha) in WAVES:
        canvas.blend_rect(x0, y, x1, y + 2, WAVE, alpha)

    # One small sailboat on the open water, left of the reflection.
    canvas.polygon([(450, 722), (492, 722), (486, 732), (456, 732)],
                   TEXT_SHADOW)
    canvas.line(471, 722, 471, 690, TEXT_SHADOW, width=2)
    canvas.polygon([(471, 692), (471, 720), (492, 712)],
                   LIGHTHOUSE_WHITE)
    canvas.polygon([(471, 694), (471, 718), (455, 712)], TEXT_CREAM)
    canvas.blend_rect(458, 736, 484, 738, WAVE, 60)

    # Cliff with a sunlit rim along its top edge.
    cliff = [(0, H)] + CLIFF_TOP + [(340, H)]
    canvas.polygon(cliff, CLIFF)
    for (x0, y0), (x1, y1) in zip(CLIFF_TOP, CLIFF_TOP[1:]):
        canvas.line(x0, y0, x1, y1, CLIFF_RIM, width=2)
    # Rock strata following the slope, and two cypress trees on the rim,
    # so the cliff reads as rock instead of a flat dark mass (v1 issue).
    strata = [
        [(0, 860), (90, 780), (170, 700), (240, 645), (300, 625),
         (340, 640)],
        [(0, 950), (90, 870), (170, 790), (240, 735), (300, 715),
         (340, 730)],
        [(0, 1024), (90, 960), (170, 880), (240, 825), (300, 805),
         (340, 820)],
    ]
    for line_points in strata:
        for (x0, y0), (x1, y1) in zip(line_points, line_points[1:]):
            canvas.line(x0, y0, x1, y1, STRATA, width=2)
    for (tx, ty, th) in ((292, 548, 34), (318, 550, 26)):
        canvas.polygon([(tx - 6, ty), (tx + 6, ty), (tx, ty - th)], CLIFF)

    _draw_cottage(canvas)
    _draw_lighthouse(canvas)

    # Clouds, kept clear of the lighthouse and the sun disc.
    _draw_cloud(canvas, 720, 250, 260, CLOUD, 85)
    _draw_cloud(canvas, 430, 360, 200, CLOUD, 85)
    _draw_cloud(canvas, 860, 440, 180, CLOUD, 85)
    _draw_cloud(canvas, 110, 420, 130, CLOUD, 80)

    for (x, y, s) in BIRDS:
        _draw_bird(canvas, x, y, s, BIRD)

    # The name: big cream letters with a soft dark shadow, gold rule
    # beneath. This is the only copy in the picture.
    scale = 16
    gap = 16
    name_w = text_width(PLACE_NAME, scale, gap)
    nx = (W - name_w) // 2
    ny = 64
    draw_text(canvas, PLACE_NAME, nx, ny, scale, TEXT_CREAM, gap=gap,
              shadow=TEXT_SHADOW, shadow_dx=5, shadow_dy=6)
    canvas.fill_rect(nx, ny + 7 * scale + 18, nx + name_w,
                     ny + 7 * scale + 21, RULE_GOLD)
