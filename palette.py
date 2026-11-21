"""Palette for the Velmara poster: one deliberate sunset palette.

Every colour is a plain RGB tuple. The poster uses a single mood:
dusk over a turquoise sea, warm low sun, dark cliffs, one white lighthouse.
(v4: deeper dusk top, warmer horizon, deeper sea.)
"""

# Sky, top (darkest) to horizon (warmest).
SKY_TOP = (22, 28, 70)
SKY_MID1 = (74, 50, 118)
SKY_MID2 = (178, 84, 122)
SKY_LOW = (233, 132, 96)
SKY_GOLD = (247, 178, 105)
SKY_HORIZON = (250, 202, 122)

# Sun.
SUN_CORE = (255, 237, 181)
SUN_RIM = (255, 186, 92)
SUN_GLOW = (255, 207, 125)
SUN_BLOOM = (255, 198, 118)

# Horizon haze: pale warm veil that softens the dead-straight horizon.
HAZE = (252, 208, 158)

# Sea lift: slightly lighter teal that keeps the deep bottom band alive.
SEA_LIFT = (26, 84, 118)

# Clouds (drawn translucent), with a warm-lit underside.
CLOUD = (255, 217, 194)
CLOUD_UNDER = (255, 190, 130)

# Sea, horizon to bottom.
SEA_TOP = (72, 158, 160)
SEA_MID = (34, 112, 132)
SEA_LOW = (16, 70, 100)
SEA_DEEP = (8, 34, 60)

# Sun reflection on the sea.
REFLECT = (255, 217, 138)
WAVE = (127, 184, 196)
FOAM = (214, 236, 238)

# Far headland silhouette on the right horizon (drawn translucent).
FAR_HEADLAND = (96, 74, 118)

# Cliff, cottage, lighthouse.
CLIFF = (30, 35, 64)
CLIFF_RIM = (86, 100, 150)
CLIFF_RIM_WARM = (255, 183, 110)
STRATA = (44, 52, 84)
COTTAGE = (36, 31, 56)
COTTAGE_ROOF = (24, 21, 46)
WINDOW = (255, 202, 106)
LIGHTHOUSE_WHITE = (246, 241, 227)
LIGHTHOUSE_BAND = (42, 51, 85)
TOWER_SUN = (255, 214, 160)
LAMP = (255, 215, 106)
LAMP_HALO = (255, 222, 130)
BEAM = (255, 214, 120)
FLAG = (255, 118, 88)

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
