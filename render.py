#!/usr/bin/env python3
"""Render the news-image-20261126 front page (build time only, Pillow).

Layout (1024x1024): navy masthead, one big hero panel on the tariff salvo,
a 2x3 grid of six story panels, and a news ticker along the bottom.
All stories were verified against live sources on 26 Nov 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
INK = (18, 18, 18)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
CREAM = (255, 250, 235)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r):
    """Stylised globe: disc, meridians, parallels, a few land blobs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 90, 150),
              outline=(140, 190, 230), width=3)
    for k in (-2, -1, 0, 1, 2):
        x = cx + k * r // 3
        xr = int(r * (1 - (k / 3.0) ** 2) ** 0.5) if abs(k) < 3 else 0
        if xr > 0:
            d.arc([cx - xr, cy - r, cx + xr, cy + r], 270, 90,
                  fill=(140, 190, 230), width=2)
            d.arc([cx - xr, cy - r, cx + xr, cy + r], 90, 270,
                  fill=(140, 190, 230), width=2)
    for k in (-1, 0, 1):
        y = cy + k * r // 2
        half = int((r * r - (y - cy) ** 2) ** 0.5)
        d.line([cx - half, y, cx + half, y], fill=(140, 190, 230), width=2)
    # land blobs (abstract continents)
    d.ellipse([cx - r * 0.55, cy - r * 0.62, cx - r * 0.05, cy - r * 0.18],
              fill=(96, 160, 90))
    d.ellipse([cx + r * 0.08, cy - r * 0.30, cx + r * 0.52, cy + r * 0.22],
              fill=(96, 160, 90))
    d.ellipse([cx - r * 0.35, cy + r * 0.28, cx + r * 0.05, cy + r * 0.60],
              fill=(120, 170, 95))


def draw_ship(d, x, y, s):
    """Simple container-ship silhouette."""
    d.polygon([(x, y), (x + 150 * s, y), (x + 132 * s, y + 26 * s),
               (x + 18 * s, y + 26 * s)], fill=(30, 30, 40))
    for i, col in enumerate([(178, 34, 34), (201, 162, 39), (38, 90, 150)]):
        bx = x + 30 * s + i * 34 * s
        d.rectangle([bx, y - 26 * s, bx + 28 * s, y - 2 * s], fill=col)
    d.rectangle([x + 128 * s, y - 34 * s, x + 140 * s, y], fill=(30, 30, 40))


def rate_chip(d, x, y, text):
    w = 92
    d.rounded_rectangle([x, y, x + w, y + 44], radius=22, fill=RED,
                        outline=WHITE, width=2)
    f = font(SANS_B, 24)
    tw = d.textlength(text, font=f)
    d.text((x + (w - tw) / 2, y + 8), text, font=f, fill=WHITE)


def icon_magnifier(d, x, y, s):
    d.ellipse([x, y, x + 34 * s, y + 34 * s], outline=RED, width=5)
    d.line([x + 26 * s, y + 26 * s, x + 44 * s, y + 44 * s], fill=RED, width=6)


def icon_satellite(d, x, y, s):
    d.ellipse([x - 4 * s, y - 4 * s, x + 52 * s, y + 52 * s], outline=GREY, width=2)
    d.rectangle([x + 14 * s, y + 16 * s, x + 36 * s, y + 34 * s], fill=NAVY2)
    d.rectangle([x - 6 * s, y + 20 * s, x + 12 * s, y + 30 * s], fill=(90, 140, 200))
    d.rectangle([x + 38 * s, y + 20 * s, x + 56 * s, y + 30 * s], fill=(90, 140, 200))


def icon_flag(d, x, y, s):
    d.line([x + 6 * s, y, x + 6 * s, y + 48 * s], fill=INK, width=4)
    d.polygon([(x + 6 * s, y), (x + 46 * s, y + 8 * s), (x + 6 * s, y + 20 * s)],
              fill=RED)
    d.polygon([(x + 6 * s, y + 20 * s), (x + 46 * s, y + 28 * s),
               (x + 6 * s, y + 36 * s)], fill=(38, 90, 150))


def icon_chip(d, x, y, s):
    d.rectangle([x + 8 * s, y + 8 * s, x + 42 * s, y + 42 * s], fill=(34, 120, 60))
    d.rectangle([x + 18 * s, y + 18 * s, x + 32 * s, y + 32 * s], fill=CREAM)
    for i in range(3):
        d.line([x + 14 * s + i * 11 * s, y, x + 14 * s + i * 11 * s, y + 8 * s],
               fill=INK, width=3)
        d.line([x + 14 * s + i * 11 * s, y + 42 * s, x + 14 * s + i * 11 * s,
                y + 50 * s], fill=INK, width=3)


def icon_bars(d, x, y, s):
    for i, h in enumerate((18, 30, 44)):
        bx = x + i * 15 * s
        d.rectangle([bx, y + 48 * s - h * s, bx + 10 * s, y + 48 * s],
                    fill=RED if i == 2 else (90, 90, 90))
    d.line([x, y + 48 * s, x + 48 * s, y + 48 * s], fill=INK, width=3)


def icon_asteroid(d, x, y, s):
    d.ellipse([x, y, x + 48 * s, y + 48 * s], fill=(140, 135, 125))
    d.ellipse([x + 12 * s, y + 10 * s, x + 32 * s, y + 28 * s], fill=(105, 100, 92))
    d.ellipse([x + 28 * s, y + 28 * s, x + 40 * s, y + 40 * s], fill=(105, 100, 92))


ICONS = {
    "magnifier": icon_magnifier,
    "satellite": icon_satellite,
    "flag": icon_flag,
    "chip": icon_chip,
    "bars": icon_bars,
    "asteroid": icon_asteroid,
}


def panel(d, x, y, w, h, kicker, kicker_col, headline, sub, icon):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(200, 195, 185), width=2)
    d.rectangle([x, y, x + w, y + 30], fill=kicker_col)
    kf = font(SANS_B, 16)
    d.text((x + 10, y + 6), kicker, font=kf, fill=WHITE)
    ICONS[icon](d, x + w - 56, y + 40, 1.0)
    hf = font(SERIF_B, 21)
    lines = wrap(d, headline, hf, w - 72)
    ly = y + 40
    for ln in lines[:2]:
        d.text((x + 10, ly), ln, font=hf, fill=INK)
        ly += 25
    sf = font(SANS, 15)
    slines = wrap(d, sub, sf, w - 20)
    ly = y + 96
    for ln in slines[:3]:
        d.text((x + 10, ly), ln, font=sf, fill=(60, 60, 60))
        ly += 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 92, W, 98], fill=GOLD)
    tf = font(SERIF_B, 33)
    d.text((18, 28), "THE WORLD IN ONE PICTURE", font=tf, fill=WHITE)
    df = font(SANS_B, 20)
    date = "THURSDAY, 26 NOVEMBER 2026"
    d.text((W - 18 - d.textlength(date, font=df), 32), date, font=df, fill=GOLD)

    # ---- hero ----
    hx, hy, hw, hh = 16, 110, W - 32, 452
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=NAVY2)
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=GOLD, width=3)
    draw_globe(d, hx + 150, hy + 190, 118)
    draw_ship(d, hx + 60, hy + 350, 0.9)
    # tariff chips under the globe
    rate_chip(d, hx + 30, hy + 388, "20%")
    rate_chip(d, hx + 125, hy + 388, "15%")
    rate_chip(d, hx + 220, hy + 388, "35%")
    # hero headline (right of globe)
    tx = hx + 330
    hf = font(SERIF_B, 56)
    for i, ln in enumerate(["TRUMP'S", "TARIFF", "SALVO"]):
        d.text((tx, hy + 22 + i * 62), ln, font=hf, fill=WHITE)
    sf = font(SANS, 20)
    sub = ("Washington proposes new duties on 14 economies — China 20%, "
           "the EU 15%, Vietnam up to 35% — to replace the tariffs the "
           "Supreme Court struck down in February. A public hearing is "
           "set for Jan 25; markets slide.")
    lines = wrap(d, sub, sf, hw - 330 - 24)
    ly = hy + 216
    for ln in lines:
        d.text((tx, ly), ln, font=sf, fill=(215, 225, 240))
        ly += 27
    kf = font(SANS_B, 18)
    d.text((tx, hy + 400), "WASHINGTON  •  TRADE WAR, ROUND TWO", font=kf, fill=GOLD)

    # ---- six story panels, 2 rows x 3 cols ----
    stories = [
        ("SHANGHAI", RED, "XI'S PROBE SHAKES CHINA",
         "Shanghai chief Chen Jining under graft investigation — the 4th "
         "Politburo member probed since 2025.", "magnifier"),
        ("ORBIT", NAVY2, "A MILLION SATELLITES",
         "FCC clears SpaceX Starmind orbital AI data centres; first "
         "satellite by 2033, full fleet by 2040.", "satellite"),
        ("PYONGYANG", RED, "SWISS ENVOY EXPELLED",
         "North Korea orders its diplomat out in 48 hours and shuts the "
         "office, a month after reopening.", "flag"),
        ("WASHINGTON", NAVY2, "NVIDIA: NO ANSWERS",
         "Attorney General dodges questions on the Huang probe; shares "
         "fall 7% as lawmakers demand answers.", "chip"),
        ("MOSCOW", RED, "THE HIDDEN TOLL: 490,334",
         "Leaked Rosstat data show near half a million Russian soldiers "
         "dead since February 2022.", "bars"),
        ("SPACE", NAVY2, "CRATER ON DIMORPHOS",
         "Hera reveals a stadium-size crater from the DART impact; the "
         "asteroid now tumbles in orbit.", "asteroid"),
    ]
    gx, gy = 16, 578
    pw, ph, gap = 320, 168, 16
    for i, (kick, col, head, sub_txt, icon) in enumerate(stories):
        px = gx + (i % 3) * (pw + gap)
        py = gy + (i // 3) * (ph + gap)
        panel(d, px, py, pw, ph, kick, col, head, sub_txt, icon)

    # ---- ticker ----
    ty = 950
    d.rectangle([0, ty, W, H], fill=NAVY)
    tf2 = font(SANS_B, 18)
    tick = ("CAIRO: FUEL-TANKER FIRE KILLS 31   •   CARTAGENA: 30 HOSTAGES FREED "
            "•   KYIV: PARLIAMENT LEGALISES CRYPTO   •   "
            "DOJ CHARGES 800+ IN BIGGEST SCAM SWEEP")
    tlines = wrap(d, tick, tf2, W - 32)
    ly = ty + 8
    for ln in tlines[:2]:
        d.text((16, ly), ln, font=tf2, fill=WHITE)
        ly += 22

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
