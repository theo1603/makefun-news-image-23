#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

A newspaper front page summing up the day's world news, drawn with Pillow.
Every headline is set from reporting published on 23 November 2026:
the NATO emergency session in Brussels, the COP31 fallout, Nepal's PM
in Delhi, the Houthi refinery claim, the UN killer-robots talks, Seoul's
education minister resigning, and India's record Test total.

Run:  python3 draw_poster.py   -> writes entry.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (179, 18, 46)
GOLD = (201, 162, 39)
GREY = (90, 88, 80)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, bg, fg=(255, 255, 255)):
    fnt = font(SANS_B, 16)
    w = draw.textlength(label, font=fnt) + 18
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=bg)
    draw.text((x + 9, y + 4), label, font=fnt, fill=fg)
    return w


def draw_star(draw, cx, cy, r_out, r_in, points, fill):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_lead_art(draw, box):
    """NATO compass over a border line: the lead illustration."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 10
    # faint stars
    for sx, sy in [(x0 + 40, y0 + 30), (x1 - 60, y0 + 55), (x0 + 90, y0 + 90),
                   (x1 - 30, y1 - 90), (x0 + 200, y0 + 24)]:
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255))
    # dashed red arc: a missile path crossing the border
    import math
    for t in range(0, 101, 4):
        a = math.pi * (0.15 + 0.7 * t / 100.0)
        px = cx - 150 + 300 * t / 100.0
        py = cy + 60 - 150 * math.sin(a)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(235, 90, 90))
    # border line
    draw.line([cx + 60, y0 + 20, cx + 60, y1 - 20], fill=GOLD, width=4)
    # NATO-style compass star
    draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=(255, 255, 255), width=3)
    draw_star(draw, cx, cy, 58, 14, 4, (255, 255, 255))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD)
    # labels
    fnt = font(SANS_B, 20)
    draw.text((x0 + 16, y0 + 12), "BRUSSELS", font=fnt, fill=GOLD)
    draw.text((x0 + 16, y0 + 40), "32 ALLIES MEET", font=font(SANS_B, 16), fill=(255, 255, 255))
    # bottom strip: Poland flag
    draw.rectangle([x0, y1 - 46, x1, y1], fill=(30, 48, 80))
    draw.rectangle([x0 + 16, y1 - 34, x0 + 52, y1 - 12], fill=(255, 255, 255))
    draw.rectangle([x0 + 16, y1 - 23, x0 + 52, y1 - 12], fill=(220, 20, 60))
    draw.text((x0 + 62, y1 - 36), "POLAND", font=fnt, fill=(255, 255, 255))


def draw_card(draw, box, kicker, kcolor, headline, body):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=(200, 192, 175), width=2)
    draw.line([x0, y0, x1, y0], fill=kcolor, width=5)
    chip(draw, x0 + 12, y0 + 12, kicker, kcolor)
    f_h = font(SANS_B, 23)
    lines = wrap(draw, headline, f_h, (x1 - x0) - 24)
    y = text_block(draw, (x0 + 12, y0 + 48), lines[:2], f_h, INK, 28)
    f_b = font(SANS, 16)
    blines = wrap(draw, body, f_b, (x1 - x0) - 24)
    text_block(draw, (x0 + 12, y + 4), blines[:3], f_b, (60, 58, 52), 19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((W // 2, 8), "THE WORLD TODAY", font=font(SERIF, 62),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 70), "ONE DAY  •  ONE PAGE  •  EVERY STORY THAT MATTERED",
           font=font(SANS_B, 15), fill=GOLD, anchor="ma")

    # ---- date band ----
    d.rectangle([0, 96, W, 152], fill=RED)
    d.text((W // 2, 104), "MONDAY, 23 NOVEMBER 2026", font=font(SERIF, 40),
           fill=(255, 255, 255), anchor="ma")
    d.line([0, 152, W, 152], fill=GOLD, width=4)

    # ---- lead story ----
    lx, ly = 36, 172
    chip(d, lx, ly, "EUROPE  •  NATO", RED)
    f_lead = font(SERIF, 48)
    lead = "NATO in emergency session over Poland"
    lines = wrap(d, lead, f_lead, 560)
    y = text_block(d, (lx, ly + 40), lines, f_lead, INK, 54)
    d.text((lx, y + 6), "Rutte: alliance will defend \u2018every inch\u2019",
           font=font(SERIF_IT, 26), fill=RED)
    body = ("All 32 allies meet in Brussels after Russian missiles and a "
            "drone crossed into Poland on Friday. Warsaw wants stronger "
            "air defences on NATO\u2019s eastern flank.")
    f_body = font(SANS, 19)
    text_block(d, (lx, y + 48), wrap(d, body, f_body, 560)[:3], f_body, (40, 38, 34), 26)

    draw_lead_art(d, (620, 172, 988, 462))
    d.line([36, 476, 988, 476], fill=(200, 192, 175), width=2)

    # ---- six story cards, 2 rows x 3 ----
    cards = [
        ("CLIMATE", (34, 139, 34),
         "COP31 collapse: leaders react",
         "Antalya talks end with no deal; the EU rejects a text that never names fossil fuels."),
        ("ASIA", (214, 90, 0),
         "Nepal\u2019s PM meets Modi in Delhi",
         "Balendra Shah\u2019s first foreign trip as PM: trade, energy and ties top the agenda."),
        ("GULF", (0, 128, 128),
         "Houthis claim Saudi refinery hit",
         "Claim unconfirmed by Riyadh; Iran says two tankers hit mines off Hormuz."),
        ("UNITED NATIONS", (90, 60, 160),
         "UN to keep talking on killer robots",
         "States agree to continue negotiations on lethal autonomous weapons."),
        ("KOREA", (0, 90, 180),
         "Seoul minister quits over AI exam row",
         "Seoul\u2019s education chief resigns after last-minute anti-cheating chaos."),
        ("SPORT", (160, 20, 40),
         "India post record 720 in Wellington",
         "India declare at 720/9 against New Zealand, a record first-innings total."),
    ]
    cw, ch, gap = 304, 168, 12
    x0, y0 = 36, 490
    for i, (kick, col, head, body) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gap)
        cy = y0 + (i // 3) * (ch + gap)
        draw_card(d, (cx, cy, cx + cw, cy + ch), kick, col, head, body)

    # ---- also today strip ----
    ay = 848
    d.rectangle([0, ay, W, 952], fill=NAVY)
    d.text((36, ay + 10), "ALSO TODAY", font=font(SANS_B, 20), fill=GOLD)
    items = ("Myanmar calls ASEAN decision \u2018unfair\u2019  •  Lisbon marches over living costs  •  "
             "Java factory fire: search resumes as 24 body bags found  •  "
             "Father and daughter held by ICE at Seattle airport")
    f_a = font(SANS, 19)
    text_block(d, (36, ay + 40), wrap(d, items, f_a, 952), f_a, (255, 255, 255), 26)

    # ---- footer ----
    d.text((W // 2, 962), "Drawn from the day\u2019s reporting  •  AP  •  Reuters  •  AFP",
           font=font(SERIF_IT, 17), fill=GREY, anchor="ma")
    d.text((W // 2, 984), "THE WORLD TODAY  —  MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 15), fill=(60, 58, 52), anchor="ma")
    d.line([W // 2 - 60, 1014, W // 2 + 60, 1014], fill=GOLD, width=3)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
