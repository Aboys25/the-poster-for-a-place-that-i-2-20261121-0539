"""Palette for the Velmara poster: one deliberate sunset palette.

Every colour is a plain RGB tuple. The poster uses a single mood:
dusk over a turquoise sea, warm low sun, dark cliffs, one white lighthouse.
"""

# Sky, top (darkest) to horizon (warmest).
SKY_TOP = (28, 36, 80)
SKY_MID1 = (90, 63, 125)
SKY_MID2 = (182, 90, 114)
SKY_LOW = (239, 154, 99)
SKY_HORIZON = (247, 200, 115)

# Sun.
SUN_CORE = (255, 237, 181)
SUN_GLOW = (255, 207, 125)

# Clouds (drawn translucent).
CLOUD = (255, 217, 194)

# Sea, horizon to bottom.
SEA_TOP = (63, 154, 160)
SEA_MID = (26, 106, 128)
SEA_DEEP = (10, 42, 68)

# Sun reflection on the sea.
REFLECT = (255, 217, 138)
WAVE = (127, 184, 196)

# Cliff, cottage, lighthouse.
CLIFF = (30, 35, 64)
CLIFF_RIM = (86, 100, 150)
STRATA = (44, 52, 84)
COTTAGE = (36, 31, 56)
COTTAGE_ROOF = (24, 21, 46)
WINDOW = (255, 202, 106)
LIGHTHOUSE_WHITE = (246, 241, 227)
LIGHTHOUSE_BAND = (42, 51, 85)
LAMP = (255, 215, 106)
BEAM = (255, 214, 120)

# Type: cream letters on the dark top sky, with a soft dark shadow.
TEXT_CREAM = (255, 243, 214)
TEXT_SHADOW = (26, 32, 68)
RULE_GOLD = (247, 200, 115)

# Birds and stars.
BIRD = (42, 47, 77)
STAR = (255, 244, 214)


def lerp(a, b, t):
    """Linear blend of two RGB colours; t in [0, 1]."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def lerp_stops(stops, t):
    """Blend across sorted (position, colour) stops; t in [0, 1]."""
    if t <= stops[0][0]:
        return stops[0][1]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if t <= p1:
            u = (t - p0) / max(1e-9, p1 - p0)
            return lerp(c0, c1, u)
    return stops[-1][1]
