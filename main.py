"""Entrypoint: write /output/entry.png (Python 3.13, stdlib only).

Deterministic: no network, no clock, no unseeded randomness, no reads
outside this entry directory. The output directory comes from
MAKEFUN_OUTPUT_DIR when set (local runs), defaulting to /output.
"""

import os

from build import build_poster_png


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    png = build_poster_png()
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
