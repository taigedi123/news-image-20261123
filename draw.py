#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

A newspaper-style infographic: one masthead, one lead story and five
smaller panels, each with a flat icon, a kicker, a headline and a short
blurb. Renders 1024x1024 PNG, deterministic, no network, no clock.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (28, 28, 28)
MUTED = (90, 84, 72)
NAVY = (20, 33, 61)
GOLD = (198, 158, 62)
RED = (143, 29, 29)
CARD = (255, 255, 255)
BORDER = (201, 191, 168)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 15)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 22


def card(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=BORDER, width=2)


def icon_box(draw, x, y, s, color, kind):
    """Flat pictogram in a rounded square."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=12, fill=color)
    cx, cy = x + s // 2, y + s // 2
    white = (255, 255, 255)
    if kind == "globe":
        r = s // 2 - 14
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=white, width=4)
        draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                     outline=white, width=3)
        draw.line([cx - r, cy, cx + r, cy], fill=white, width=3)
        draw.line([cx - r + 8, cy - r + 26, cx - r + 22, cy - r + 40,
                   cx - r + 12, cy - r + 52], fill=GOLD, width=4)
    elif kind == "burst":
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rad = s // 2 - 6 if i % 2 == 0 else s // 4
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=(255, 214, 64))
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255))
    elif kind == "ship":
        draw.polygon([(cx - 34, cy + 6), (cx + 34, cy + 6),
                      (cx + 24, cy + 24), (cx - 24, cy + 24)],
                     fill=white)
        draw.rectangle([cx - 8, cy - 12, cx + 8, cy + 6], fill=white)
        draw.polygon([(cx - 4, cy - 34), (cx + 10, cy - 8), (cx - 2, cy - 8),
                      (cx + 6, cy - 22), (cx - 12, cy - 8)],
                     fill=(255, 170, 40))
    elif kind == "robot":
        draw.rounded_rectangle([cx - 26, cy - 16, cx + 26, cy + 22],
                               radius=8, fill=white)
        draw.line([cx, cy - 16, cx, cy - 30], fill=white, width=4)
        draw.ellipse([cx - 5, cy - 35, cx + 5, cy - 25], fill=(255, 214, 64))
        draw.ellipse([cx - 16, cy - 4, cx - 6, cy + 6], fill=color)
        draw.ellipse([cx + 6, cy - 4, cx + 16, cy + 6], fill=color)
        draw.line([cx - 12, cy + 14, cx + 12, cy + 14], fill=color, width=3)
    elif kind == "paper":
        draw.rectangle([cx - 22, cy - 30, cx + 22, cy + 30], fill=white)
        for i, yy in enumerate([-18, -6, 6]):
            draw.line([cx - 14, cy + yy, cx + 14, cy + yy],
                      fill=(120, 120, 120), width=3)
        draw.line([cx + 6, cy + 14, cx + 20, cy + 28], fill=(200, 30, 30),
                  width=5)
        draw.line([cx + 20, cy + 14, cx + 6, cy + 28], fill=(200, 30, 30),
                  width=5)
    elif kind == "cricket":
        draw.ellipse([cx - 26, cy - 26, cx + 2, cy + 2], fill=(200, 40, 40),
                     outline=white, width=3)
        draw.arc([cx - 26, cy - 26, cx + 2, cy + 2], start=200, end=340,
                 fill=white, width=3)
        # bat leaning to the lower right
        draw.polygon([(cx + 8, cy - 18), (cx + 20, cy - 12),
                      (cx + 2, cy + 30), (cx - 10, cy + 24)],
                     fill=(245, 222, 179), outline=white)


def story_card(draw, x, y, w, h, icon, color, kick, head, blurb):
    card(draw, x, y, w, h)
    icon_box(draw, x + 16, y + 16, 72, color, icon)
    kicker(draw, x + 102, y + 20, kick, color)
    f_head = font(SERIF_B, 22)
    hy = y + 48
    for ln in wrap(draw, head, f_head, w - 118)[:2]:
        draw.text((x + 102, hy), ln, font=f_head, fill=INK)
        hy += 27
    f_body = font(SANS, 16)
    para(draw, x + 16, y + 104, blurb, f_body, w - 32, 21, (60, 56, 48))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    f_title = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 26), title, font=f_title, fill=(255, 255, 255))
    d.rectangle([0, 116, W, 121], fill=GOLD)

    # Dateline
    f_date = font(SERIF_B, 34)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 128), date, font=f_date, fill=RED)
    f_sub = font(SANS, 15)
    sub = "SIX STORIES  •  EVERY REGION  •  ONE DAY'S NEWS"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 172), sub, font=f_sub, fill=MUTED)

    # Lead story: COP31
    lx, ly, lw, lh = 28, 196, 968, 196
    card(d, lx, ly, lw, lh)
    icon_box(d, lx + 18, ly + 18, 160, (15, 118, 110), "globe")
    kicker(d, lx + 198, ly + 20, "Climate · Antalya, Türkiye", (15, 118, 110))
    f_lead = font(SERIF_B, 31)
    for i, ln in enumerate(["COP31 talks collapse —",
                            "no deal on fossil fuels"]):
        d.text((lx + 198, ly + 50 + i * 38), ln, font=f_lead, fill=INK)
    f_blurb = font(SANS, 18)
    para(d, lx + 198, ly + 132,
         "The EU and allies reject a draft pact that never names fossil "
         "fuels, and the summit ends with no agreement.",
         f_blurb, lw - 216, 23, (60, 56, 48))

    # Middle grid: four stories
    gy, gh = 408, 214
    gw = 472
    stories = [
        ("burst", (185, 28, 28), "Middle East · Bahrain",
         "Iran hits US bases in Bahrain as Gulf war widens",
         "Tehran strikes two American bases; two people are wounded. "
         "Houthi rebels fire a missile at Saudi Arabia."),
        ("ship", (30, 58, 95), "Ukraine · Baltic Sea",
         "Russian ship ablaze; 14 missing near Kyiv",
         "A Ukrainian drone sets a Russian cargo ship ablaze off Finland. "
         "A Russian drone strike hits a building in the Kyiv region."),
        ("robot", (109, 40, 217), "United Nations",
         "Nations agree to keep talking on lethal AI weapons",
         "Governments extend negotiations on curbing autonomous weapons "
         "at a UN conference on killer robots."),
        ("paper", (180, 83, 9), "South Korea · Seoul",
         "Minister quits over AI exam-cheating scandal",
         "The minister resigns after AI cheating claims rock the "
         "national exams, shaking trust in the system."),
    ]
    for i, (icon, color, kick, head, blurb) in enumerate(stories):
        x = 28 + (i % 2) * (gw + 24)
        y = gy + (i // 2) * (gh + 16)
        story_card(d, x, y, gw, gh, icon, color, kick, head, blurb)

    # Bottom strip: cricket
    bx, by, bw, bh = 28, 868, 968, 92
    card(d, bx, by, bw, bh)
    icon_box(d, bx + 14, by + 14, 64, (21, 128, 61), "cricket")
    kicker(d, bx + 94, by + 14, "Sport · Wellington", (21, 128, 61))
    f_sport = font(SERIF_B, 24)
    d.text((bx + 94, by + 40),
           "India declare on a record 720 for 9",
           font=f_sport, fill=INK)
    f_sblurb = font(SANS, 15)
    d.text((bx + 94, by + 70),
           "Highest Test total ever in New Zealand — Rahul 136, Pant 128. "
           "Hosts 119 for 2 at stumps.",
           font=f_sblurb, fill=(60, 56, 48))

    # Footer
    f_foot = font(SANS, 13)
    foot = ("Sources: AFP · AP · Reuters wires, 23 November 2026  •  "
            "Drawn in code for make.fun")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 978), foot, font=f_foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
