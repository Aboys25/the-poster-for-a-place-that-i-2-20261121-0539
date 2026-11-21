"""The Velmara poster scene: one invented place, one landmark.

v5 — light and air (v4, rank 1275/1863 at rate 0.4928, was measured
flat: dead dark band at the bottom of the sea, a flat sky, a weak lamp
and a flat sun disc, a dead-straight horizon):
  - the lamp gets a real glow: a tight bright halo, a wide soft halo
    and a beam cone spilling right over the sea, so it reads as lit;
  - the sun gets a wide soft bloom that bleeds warm light into the sky;
  - a pale warm haze band with slight desaturation softens the horizon;
  - the sea gets a gentle lift toward the bottom plus fine deterministic
    wave streaks and sparkles across the whole open sea (kept clear of
    the cliff face), so the lowest band stops being a dark slab;
  - two more clouds at varied heights break the repeated thin bars.
  (A fine deterministic film grain, ±5, was prototyped and then
  dropped: at normal viewing distance it was indistinguishable from
  no grain, while it blew the PNG up 10x, 84 KB to 852 KB.)

Composition (1024x1024), leading the eye name -> landmark -> horizon:
  - the name VELMARA, large and cream, across the dark top sky;
  - one white lighthouse on a dark cliff, left of centre, lamp lit;
  - a low sun over a turquoise sea, its reflection shimmering below.
No other copy anywhere in the picture.
"""

import math

from font5x7 import draw_text, text_width
from palette import (
    BIRD, CLIFF, CLIFF_RIM, CLIFF_RIM_WARM, CLOUD, CLOUD_UNDER,
    COTTAGE, COTTAGE_ROOF, FAR_HEADLAND, FOAM, HAZE, LAMP, LAMP_HALO,
    LIGHTHOUSE_BAND, LIGHTHOUSE_WHITE, REFLECT, RULE_GOLD, SEA_DEEP,
    SEA_LIFT, SEA_LOW, SEA_MID, SEA_TOP, SKY_GOLD, SKY_HORIZON, SKY_LOW,
    SKY_MID1, SKY_MID2, SKY_TOP, STAR, STRATA, SUN_BLOOM, SUN_CORE,
    SUN_GLOW, SUN_RIM, TEXT_CREAM, TEXT_SHADOW, TOWER_SUN, WAVE, WINDOW,
)

W = 1024
H = 1024
HORIZON = 640
PLACE_NAME = "VELMARA"
FEATURE_LINE = "THE LIGHTHOUSE AT THE EDGE OF THE SEA"

# Fixed stars in the dark top sky, kept clear of the name band.
STARS = [
    (40, 30), (90, 55), (130, 20), (950, 35), (990, 60), (900, 80),
    (60, 120), (980, 140), (30, 200), (1000, 200), (150, 45), (870, 30),
    (200, 28), (820, 48),
]

# Fixed wave streaks across the sea: (y, x0, x1, alpha).
WAVES = [
    (700, 90, 430, 50), (745, 560, 980, 45), (790, 120, 480, 55),
    (840, 640, 970, 40), (890, 80, 400, 50), (930, 500, 900, 40),
    (975, 100, 420, 45), (720, 880, 990, 35), (860, 60, 260, 40),
    (1010, 560, 950, 35), (750, 950, 1010, 30), (960, 430, 560, 35),
]

# Gold wave streaks inside the sun's reflection path.
GOLD_WAVES = [
    (700, 610, 820, 60), (780, 630, 800, 55), (860, 650, 790, 50),
    (920, 660, 770, 45),
]

# Fixed sparkles on the water: (x, y, half-width, alpha).
SPARKLES = [
    (640, 690, 13, 90), (790, 720, 15, 80), (660, 780, 11, 70),
    (770, 830, 13, 60), (690, 900, 10, 55), (750, 950, 9, 45),
    (300, 760, 9, 40), (920, 700, 10, 45), (560, 700, 12, 50),
    (850, 760, 11, 40),
]

# Reflection dash width factors, cycled deterministically so the sun
# path shimmers instead of reading as one regular snake (v3 issue).
DASH_FACTORS = (1.0, 0.75, 1.15, 0.9, 1.25, 0.65, 1.05, 0.8, 1.2, 0.7,
                1.0, 0.85)

# Cliff top edge, left to right; the cliff fills everything below it.
# Narrower headland than v3: the tower stands on a plateau, the face
# drops to the sea at x ~ 400 instead of a flat wall at x 340. The
# small flat ledge at x 55-112 is where the cottage sits.
CLIFF_TOP = [(0, 905), (55, 832), (112, 828), (150, 735), (215, 708),
             (300, 698), (365, 712), (395, 745)]
CLIFF_FACE = [(410, 830), (405, 940), (415, 1024)]

# Foam where the sea meets the cliff face: (y, x0, x1, alpha).
FOAM_LINES = [
    (742, 398, 430, 110), (800, 404, 438, 90), (862, 400, 428, 80),
    (920, 412, 436, 70), (980, 408, 430, 60),
]

# Birds: (x, y, half-span).
BIRDS = [(430, 260, 9), (480, 300, 8), (560, 235, 9), (900, 320, 8),
         (950, 380, 9)]


def _lcg(state):
    """One step of the fixed-seed LCG used for deterministic texture:
    every run draws the same streaks and sparkles."""
    return (1103515245 * state + 12345) % (2 ** 31)


def _sea_texture(canvas):
    """Fine wave streaks and sparkles across the whole open sea, from
    the LCG above. Kept to x >= 445 so nothing lands on the cliff face
    or the foam at its foot; low alpha so the sea stays calm, not busy.
    """
    state = 20261121
    for y in range(660, 1020, 18):
        count = 2 + state % 3
        state = _lcg(state)
        for _ in range(count):
            x0 = 445 + state % 470
            state = _lcg(state)
            length = 30 + state % 100
            state = _lcg(state)
            alpha = 15 + state % 24
            state = _lcg(state)
            canvas.blend_rect(x0, y, x0 + length, y + 2, WAVE, alpha)
    for _ in range(50):
        x = 450 + state % 560
        state = _lcg(state)
        y = 660 + state % 350
        state = _lcg(state)
        hw = 4 + state % 11
        state = _lcg(state)
        alpha = 25 + state % 46
        state = _lcg(state)
        canvas.blend_rect(x - hw, y, x + hw, y + 2, REFLECT, alpha)


def _draw_cloud(canvas, cx, cy, w, rgb, alpha):
    """One flat stratus band: a low bar with rounded ends and soft bumps,
    plus a warm-lit underside line so it reads as sunset cloud, not a
    flat pink bar (v3 issue)."""
    half = 0.44 * w
    bar_h = 0.10 * w
    canvas.blend_rect(int(cx - half), int(cy), int(cx + half),
                      int(cy + bar_h), rgb, alpha)
    canvas.disc(int(cx - half), int(cy + bar_h / 2), int(bar_h / 2), rgb,
                alpha)
    canvas.disc(int(cx + half), int(cy + bar_h / 2), int(bar_h / 2), rgb,
                alpha)
    canvas.disc(int(cx - 0.15 * w), int(cy + 0.01 * w), int(0.05 * w), rgb,
                alpha)
    canvas.disc(int(cx + 0.18 * w), int(cy + 0.01 * w), int(0.045 * w), rgb,
                alpha)
    # Warm underside: the sun catches the bottom edge.
    canvas.blend_rect(int(cx - half), int(cy + bar_h - 2),
                      int(cx + half), int(cy + bar_h + 1), CLOUD_UNDER,
                      110)


def _draw_bird(canvas, x, y, s, rgb):
    """One small bird: two short strokes meeting in a shallow V."""
    canvas.line(x - s, y, x, y + s // 2, rgb, width=2)
    canvas.line(x, y + s // 2, x + s, y, rgb, width=2)


def _lighthouse_edges(y):
    """Left/right x of the tapered tower at height y.

    Tower runs from (210, 760)-(330, 760) at the base (buried in the
    cliff) to (238, 330)-(302, 330) at the top: ~1.5x the v3 tower.
    """
    t = (y - 760) / (330 - 760)
    left = 210 + t * (238 - 210)
    right = 330 + t * (302 - 330)
    return left, right


def _draw_lighthouse(canvas):
    # Tower, tapered, base buried in the cliff so it stands on the slope.
    canvas.polygon([(210, 760), (330, 760), (302, 330), (238, 330)],
                   LIGHTHOUSE_WHITE)
    # Volume: cool shadow strip on the left edge, warm sunlit strip on
    # the right edge (the sun is to the right), both following the taper.
    canvas.polygon([(210, 760), (226, 760), (246, 330), (238, 330)],
                   LIGHTHOUSE_BAND, alpha=45)
    canvas.polygon([(314, 760), (330, 760), (302, 330), (294, 330)],
                   TOWER_SUN, alpha=70)
    # Three dark bands, following the taper.
    for y0, y1 in ((400, 420), (490, 508), (580, 596)):
        l0, r0 = _lighthouse_edges(y0)
        l1, r1 = _lighthouse_edges(y1)
        canvas.polygon([(int(l0), y0), (int(r0), y0), (int(r1), y1),
                        (int(l1), y1)], LIGHTHOUSE_BAND)
    # Gallery overhang with railing posts, then the lamp room.
    canvas.fill_rect(232, 312, 308, 330, LIGHTHOUSE_BAND)
    for px in (236, 252, 268, 284, 300):
        canvas.fill_rect(px, 300, px + 3, 312, LIGHTHOUSE_BAND)
    # Lamp: tight bright halo, wide soft halo, beam cone to the right,
    # bright room, dark mullions, cap. (v5: the v4 lamp was flat yellow
    # with almost no halo; the glow is now the brightest thing on the
    # poster after the sun.)
    canvas.radial_glow_soft(270, 292, 90, LAMP_HALO, 140, 1.5)
    canvas.radial_glow_soft(270, 292, 220, LAMP, 55, 2.0)
    canvas.light_beam(270, 292, 292, 720, LAMP, 76)
    canvas.fill_rect(248, 264, 292, 268, LIGHTHOUSE_BAND)
    canvas.fill_rect(252, 268, 288, 312, LAMP)
    for mx in (262, 270, 278):
        canvas.fill_rect(mx, 268, mx + 2, 312, LIGHTHOUSE_BAND)
    # Conical roof and finial. (v4 first cut had a pennant flag here,
    # but it poked into the feature line above; the finial alone keeps
    # the silhouette clean.)
    canvas.polygon([(246, 264), (294, 264), (270, 234)], LIGHTHOUSE_BAND)
    canvas.disc(270, 236, 3, LIGHTHOUSE_BAND)


def _draw_cottage(canvas):
    # Small cottage on the flat ledge, two windows lit: an accent that
    # promises a stay, not a second hero (v3 had it bigger and higher).
    canvas.fill_rect(58, 828, 114, 880, COTTAGE)
    canvas.polygon([(50, 828), (122, 828), (86, 796)], COTTAGE_ROOF)
    canvas.fill_rect(104, 802, 112, 828, COTTAGE_ROOF)
    canvas.fill_rect(68, 842, 80, 856, WINDOW)
    canvas.fill_rect(94, 842, 106, 856, WINDOW)
    canvas.fill_rect(84, 860, 96, 880, COTTAGE_ROOF)


def draw_velmara(canvas):
    """Paint the whole poster onto the canvas."""
    # Sky and sea, richer than v3: deeper dusk top, warmer horizon,
    # deeper sea bottom.
    canvas.vgrad(0, HORIZON, [(0.0, SKY_TOP), (0.22, SKY_MID1),
                              (0.45, SKY_MID2), (0.68, SKY_LOW),
                              (0.85, SKY_GOLD), (1.0, SKY_HORIZON)])
    canvas.vgrad(HORIZON, H, [(0.0, SEA_TOP), (0.30, SEA_MID),
                              (0.65, SEA_LOW), (1.0, SEA_DEEP)])

    # Stars in the dark top sky.
    for (x, y) in STARS:
        canvas.blend_rect(x, y, x + 2, y + 2, STAR, 140)

    # Hazy far headland on the right horizon, for depth.
    canvas.polygon([(860, 640), (900, 622), (950, 628), (1024, 618),
                    (1024, 640)], FAR_HEADLAND, alpha=110)

    # Low sun: wide soft bloom that bleeds warm light into the sky,
    # tighter glow, warm rim, solid core. (v5: the v4 sun was a flat
    # cream disc with an orange ring and no bloom into the sky.)
    canvas.radial_glow_soft(715, 582, 430, SUN_BLOOM, 76, 2.0)
    canvas.radial_glow_soft(715, 582, 200, SUN_GLOW, 71, 1.5)
    canvas.disc(715, 582, 86, SUN_RIM)
    canvas.disc(715, 582, 74, SUN_CORE)

    # Sun reflection: a soft glow on the water under the sun, then gold
    # dashes with varying width and a double wobble so the path shimmers
    # instead of snaking (v3 issue).
    canvas.radial_glow(715, 670, 170, REFLECT, 26)
    for i, y in enumerate(range(652, 1000, 3)):
        if i % 4 == 3:
            continue
        depth = (y - 650) / 350.0
        wobble = int(9 * math.sin(y * 0.045)
                     + 6 * math.sin(y * 0.013 + 1.7))
        factor = DASH_FACTORS[i % len(DASH_FACTORS)]
        width = max(8, int((70 * (1.0 - depth) + 10) * factor))
        alpha = int(200 * (1.0 - depth) + 30)
        cx = 715 + wobble
        canvas.blend_rect(cx - width // 2, y, cx + width // 2, y + 2,
                          REFLECT, alpha)
    for (y, x0, x1, alpha) in GOLD_WAVES:
        canvas.blend_rect(x0, y, x1, y + 2, REFLECT, alpha)
    for (y, x0, x1, alpha) in WAVES:
        canvas.blend_rect(x0, y, x1, y + 2, WAVE, alpha)
    for (x, y, hw, alpha) in SPARKLES:
        canvas.blend_rect(x - hw, y, x + hw, y + 2, REFLECT, alpha)
    # v5: lift the deep bottom band and add fine texture across the
    # open sea, so the lowest 12% of the poster stops being a flat
    # dark slab.
    canvas.sea_lift(HORIZON, H, 445, SEA_LIFT, 0.30)
    _sea_texture(canvas)

    # Clouds, kept clear of the tower, the sun disc and the feature line.
    # (v5: two more at varied heights so the sky stops reading as six
    # identical thin bars at the same heights.)
    _draw_cloud(canvas, 520, 250, 280, CLOUD, 70)
    _draw_cloud(canvas, 740, 430, 200, CLOUD, 75)
    _draw_cloud(canvas, 100, 155, 120, CLOUD, 80)
    _draw_cloud(canvas, 920, 160, 130, CLOUD, 80)
    _draw_cloud(canvas, 620, 330, 240, CLOUD, 80)
    _draw_cloud(canvas, 430, 300, 180, CLOUD, 75)
    _draw_cloud(canvas, 860, 470, 170, CLOUD, 80)
    _draw_cloud(canvas, 120, 400, 150, CLOUD, 75)

    # Cliff headland with a sunlit rim on its sun-facing (right) side.
    cliff = [(0, H)] + CLIFF_TOP + CLIFF_FACE
    canvas.polygon(cliff, CLIFF)
    for (x0, y0), (x1, y1) in zip(CLIFF_TOP, CLIFF_TOP[1:]):
        # Cool rim on the shaded left slope, warm rim toward the sun.
        colour = CLIFF_RIM if x0 < 215 else CLIFF_RIM_WARM
        canvas.line(x0, y0, x1, y1, colour, width=3)
    for (x0, y0), (x1, y1) in zip(CLIFF_TOP[-1:] + CLIFF_FACE,
                                  CLIFF_FACE):
        canvas.line(x0, y0, x1, y1, CLIFF_RIM_WARM, width=3)
    # Rock strata following the slope, and foam where the sea meets the
    # face, so the cliff reads as rock (v3 issue). (Boulders were tried
    # and dropped: as flat polygons they read as dark blobs floating
    # off the cliff face.)
    strata = [
        [(0, 960), (55, 890), (112, 888), (150, 795), (215, 768),
         (300, 758), (365, 772), (395, 805)],
        [(0, 1010), (55, 950), (112, 948), (150, 855), (215, 828),
         (300, 818), (365, 832)],
    ]
    for line_points in strata:
        for (x0, y0), (x1, y1) in zip(line_points, line_points[1:]):
            canvas.line(x0, y0, x1, y1, STRATA, width=2)
    for (y, x0, x1, alpha) in FOAM_LINES:
        canvas.blend_rect(x0, y, x1, y + 2, FOAM, alpha)
    # Two cypress trees on the rim, right of the tower.
    for (tx, ty, th) in ((348, 707, 42), (375, 714, 32)):
        canvas.polygon([(tx - 6, ty), (tx + 6, ty), (tx, ty - th)], CLIFF)

    _draw_cottage(canvas)
    _draw_lighthouse(canvas)

    for (x, y, s) in BIRDS:
        _draw_bird(canvas, x, y, s, BIRD)

    # v5: pale warm haze around the horizon, so the sea/sky join stops
    # reading as one dead-straight cut. Applied after the scene so it
    # veils the cliff rim and the far headland exactly as prototyped.
    canvas.horizon_haze(520, 700, HORIZON, HAZE, 50, 0.35)

    # The name: big cream letters with a soft dark shadow, gold rule
    # beneath, then one small gold line naming the single feature.
    # This is the only copy in the picture.
    scale = 16
    gap = 16
    name_w = text_width(PLACE_NAME, scale, gap)
    nx = (W - name_w) // 2
    ny = 64
    draw_text(canvas, PLACE_NAME, nx, ny, scale, TEXT_CREAM, gap=gap,
              shadow=TEXT_SHADOW, shadow_dx=5, shadow_dy=6)
    canvas.fill_rect(nx, ny + 7 * scale + 18, nx + name_w,
                     ny + 7 * scale + 21, RULE_GOLD)
    fscale = 3
    fgap = 3
    feat_w = text_width(FEATURE_LINE, fscale, fgap)
    fx = (W - feat_w) // 2
    draw_text(canvas, FEATURE_LINE, fx, ny + 7 * scale + 34, fscale,
              RULE_GOLD, gap=fgap)
