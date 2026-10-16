#!/usr/bin/env python3
"""Reproduce Dissonant Collective logo options 1, 5 and 6 as SVG.

Requires Python 3 only (no third-party packages).
Run: python3 create_logos.py
Optional: python3 create_logos.py --output-dir ./logos --transparent

Typography uses Arial or Georgia with browser fallbacks. Install these fonts
to match the original preview; SVG text remains editable.
"""


# <link rel="stylesheet" href="https://use.typekit.net/bwv0xoi.css">

"""

font-family: typeka, sans-serif;
font-style: normal;
font-weight: 400;

@font-face {
      font-family: "typeka, sans-serif";
      font-style: normal;
      font-weight: 400;
      src:
        url("https://mdn.github.io/shared-assets/fonts/FiraSans-Italic.woff2")
          format("woff2"),
        url("https://mdn.github.io/shared-assets/fonts/FiraSans-Bold.woff2")
          format("woff2");
    }


"""

import argparse
import math
from html import escape
from pathlib import Path

# MIDI C1 = 24, D1 = 26. Twelve-tone equal temperament at A4 = 440 Hz.
C1_HZ = 440.0 * 2 ** ((24 - 69) / 12)
D1_HZ = 440.0 * 2 ** ((26 - 69) / 12)
INK = "#181818"
SAMPLES = 1601


def signal(kind, time):
    """Equal-amplitude, zero-phase waves. Scale their sum by 1/2 to fit."""
    c = math.sin(2 * math.pi * C1_HZ * time)
    d = math.sin(2 * math.pi * D1_HZ * time)
    if kind == "c":
        return c
    if kind == "d":
        return d
    if kind == "sum":
        return (c + d) / 2
    raise ValueError(f"Unknown signal: {kind}")


def wave(kind, x, y, width, amplitude, duration, stroke_width=4):
    """Map a time interval (seconds) to an SVG path; y is its baseline."""
    points = []
    for index in range(SAMPLES):
        fraction = index / (SAMPLES - 1)
        time = fraction * duration
        px = x + fraction * width
        py = y - amplitude * signal(kind, time)
        points.append(f"{px:.3f},{py:.3f}")
    coordinates = "M" + " L".join(points)
    return (
        f'<path d="{coordinates}" fill="none" stroke="{INK}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" '
        'stroke-linejoin="round"/>'
    )


def lettering(label, x, y, size, family="Arial, sans-serif"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'font-family="{escape(family, quote=True)}" font-size="{size}" '
        f'font-weight="600" letter-spacing="0" fill="{INK}">'
        f'{escape(label)}</text>'
    )


def logo_1():
    # Separate wave paths: 0.105 seconds, drawn on the same baseline.
    return (
        wave("c", 90, 110, 420, 37, 0.105)
        + wave("d", 90, 110, 420, 37, 0.105, 3)
        + lettering("Dissonant", 300, 213, 38)
        + lettering("Collective", 300, 257, 38)
    )


def logo_5():
    # Separate waves between two lines of serif lettering.
    return (
        lettering("Dissonant", 300, 106, 47, "Georgia, serif")
        + wave("c", 100, 158, 400, 23, 0.09, 3)
        + wave("d", 100, 158, 400, 23, 0.09, 3)
        + lettering("Collective", 300, 246, 47, "Georgia, serif")
    )


def logo_6():
    # Arithmetic sum over 0.25 seconds reveals the beat envelope.
    return (
        wave("sum", 65, 118, 470, 52, 0.25)
        + lettering("Dissonant", 300, 224, 39)
        + lettering("Collective", 300, 267, 39)
    )


def svg_document(title, body, transparent=False):
    background = "" if transparent else '<rect width="600" height="330" fill="white"/>'
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 330" '
        f'role="img" aria-label="{escape(title, quote=True)}">'
        f'<title>{escape(title)}</title>{background}{body}</svg>'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "generated")
    parser.add_argument("--transparent", action="store_true", help="Omit the white background")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    designs = [
        ("01-near-unison.svg", "Near unison", logo_1()),
        ("05-wave-divider.svg", "Wave divider", logo_5()),
        ("06-beat-signature.svg", "Beat signature", logo_6()),
    ]
    print(f"C1: {C1_HZ:.9f} Hz; D1: {D1_HZ:.9f} Hz")
    for filename, title, body in designs:
        destination = args.output_dir / filename
        destination.write_text(svg_document(title, body, args.transparent), encoding="utf-8")
        print(destination.resolve())


if __name__ == "__main__":
    main()
