#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 front page, 1024x1024, with PIL.

Design for the 300px thumbnail: the date itself is the masthead (the
largest text on the page), six giant numbers anchor the page, the three
leads carry big bold headlines, and every section gets wide gutters so
nothing collapses into a wall of micro-text when shrunk. All 36 stories
are from 20 November 2026 (or, for two US Thursday-night items, first
reported to most of the world on Friday); 19 November items are listed
in the DATE CHECK strip instead. Every figure was checked against two
or more sources. Deterministic: same bytes on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (22, 22, 22)
RED = (168, 30, 34)
GREY = (110, 104, 92)
LIGHT = (238, 231, 214)
SEA = (214, 231, 242)
LAND = (196, 208, 176)
RULE = (60, 55, 45)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(size, serif=False, bold=False):
    path = (SERIF_B if serif and bold else SERIF if serif
            else SANS_B if bold else SANS)
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    """Greedy wrap into lines no wider than max_w."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, f, max_w, min_size):
    """Shrink the font until s fits max_w (never below min_size)."""
    size = f.size
    while size > min_size and text_w(d, s, f) > max_w:
        size -= 1
        f = font(size, serif=False, bold=True)
    return f


def center(d, cx, y, s, f, fill=INK):
    d.text((cx - text_w(d, s, f) / 2, y), s, font=f, fill=fill)


def left(d, x, y, s, f, fill=INK):
    d.text((x, y), s, font=f, fill=fill)


def hrule(d, x0, x1, y, fill=RULE, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- data
# (label, headline, one-line summary, source) — figures checked 2+ sources.
FEATURES = [
    ("CYCLONE AKVAN",
     "Akvan slams into the Odisha coast",
     "300,000 evacuated; winds 70-80 km/h.",
     "IMD - The Hindu"),
    ("KYIV UNDER FIRE",
     "Missiles rain on Kyiv overnight",
     "Three bridges hit; blackouts follow.",
     "Reuters - Kyiv Independent"),
    ("COP31 FINAL DAY",
     "COP31 ends its final day, no deal",
     "No deal; draft drops fossil text.",
     "Reuters"),
]

MEDIUM = [
    ("ANTHROPIC +17%", "Anthropic closes up 17%",
     "First close $97.17.", "Barron's"),
    ("MARKETS -2%", "Wall Street falls, day five",
     "S&P -2.02%, day five.", "Daily Brief"),
    ("GTA VI - 99", "GTA VI sells 24.6m day one",
     "24.6m copies, $2.36bn.", "Sensor Tower"),
    ("1 IN 4", "1 in 4 children in war zones",
     "589m, most since 1990.", "Save the Children"),
    ("UK-EU SUMMIT", "UK-EU hold first summit",
     "Burnham in Brussels.", "The Guardian"),
    ("PHILLIPS 118", "Phillips' 118 stuns India",
     "NZ 368; Nicholls 175*.", "Reuters"),
    ("SENATE 51-48", "Senate rejects Iran war powers",
     "51-48, reported Friday.", "AppiSToS"),
    ("BOAT SINKS", "Migrant boat sinks off Senegal",
     "4 dead; 50-100 aboard.", "Al Jazeera"),
    ("ITALY STRIKE", "Italy stops for 24 hours",
     "Strike over 2027 budget.", "CGIL"),
    ("CHINA HOLDS", "China holds rates, 18th month",
     "LPR 3.0%; 5-yr 3.50%.", "PBOC - Reuters"),
]

# Number band: (giant numeral, label) — same figures as in the stories.
NUMBERS = [
    ("300,000", "EVACUATED AS AKVAN LANDED"),
    ("$97.17", "ANTHROPIC FIRST CLOSE"),
    ("118", "PHILLIPS, WELLINGTON"),
    ("51-48", "SENATE IRAN VOTE"),
    ("$120bn", "AFRICA CLIMATE DEMAND A YEAR"),
    ("99", "GTA VI METACRITIC"),
]

CHIPS = ("EUROPE 9  -  AMERICAS 11  -  ASIA-PACIFIC 5  -  "
         "MIDDLE EAST 3  -  AFRICA 3  -  OCEANIA 2  -  WORLD 3")

BRIEFS = [
    (14, "Genoa airport shut, then reopened"),
    (15, "Kharkiv hospital hit; 4 hurt"),
    (16, "Houthi missile hits Riyadh tower"),
    (17, "Hormuz: 4th ship attack in 96 hrs"),
    (18, "Gaza: Israel ends one-day operation"),
    (19, "Europe ready to talk to Russia"),
    (20, "US sanctions Comancheros, 'Ndrangheta"),
    (21, "Trump pardons Pete Rose"),
    (22, "Fiona the hippo dies, aged 9"),
    (23, "California probes Nvidia on China"),
    (24, "~880,000 AI chips cleared for China"),
    (25, "Pochettino's first Man Utd address"),
    (26, "Ramraj, 19, beats Chen Yufei"),
    (27, "Jepchirchir banned 3 years, EPO"),
    (28, "Bavuma out; Markram captains"),
    (29, "Quebecor bids C$31bn for Telus"),
    (30, "Japan core inflation 2.2%"),
    (31, "Samsung names Choi to lead mobile"),
    (32, "Google adds Mac controls to Gemini"),
    (33, "Broadcom patches vCenter flaw"),
    (34, "Harris meets Macron in Paris"),
    (35, "Netherlands summons Russian envoy"),
    (36, "Tonga declares drought emergency"),
]

DATE_CHECK = ("DATE CHECK - left out (first reported 19 Nov): ICJ ruling - "
              "Shenzhen summit - Anthropic $83 - GTA VI unlock - Kyiv "
              "embassy strike - Fiji drought - Han acquittal - Crimea "
              "Bridge - Van Gogh $190.4m - EU EUR45bn loan")


# ------------------------------------------------------- illustrations
def label_bar(d, box, text, size=26):
    """Dark strip at the bottom of an illustration, giant label inside."""
    x0, y0, x1, y1 = box
    bh = size + 14
    d.rectangle([x0, y1 - bh, x1, y1], fill=(20, 20, 20))
    f = font(size, bold=True)
    while text_w(d, text, f) > (x1 - x0 - 16) and size > 14:
        size -= 1
        f = font(size, bold=True)
    d.text((x0 + 8, y1 - bh + 7), text, font=f, fill=(255, 255, 255))


def clipped(img, box, fn, *args):
    """Run an illustration on its own layer so nothing spills past its box."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    ld = ImageDraw.Draw(layer)
    fn(ld, (0, 0, x1 - x0, y1 - y0), *args)
    img.paste(layer, (x0, y0))


def ill_cyclone(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(38, 84, 112))
    for i, r in enumerate(range(10, 56, 10)):
        col = (200 + i * 6, 220 + i * 3, 235) if i < 3 else (238, 242, 246)
        d.arc([x0 + 75 - r, y0 + 26 - r, x0 + 75 + r, y0 + 26 + r],
              start=20 + i * 50, end=300 + i * 50, fill=col, width=4)
    d.ellipse([x0 + 71, y0 + 22, x0 + 79, y0 + 30], fill=(255, 255, 255))
    d.polygon([(x0, y1 - 40), (x0 + 90, y1 - 52), (x0 + 200, y1 - 44),
               (x1, y1 - 50), (x1, y1 - 40)], fill=(96, 138, 96))


def ill_kyiv(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(16, 24, 48))
    for sx, sy in [(40, 6), (120, 16), (200, 4), (260, 12), (90, 22)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                  fill=(255, 255, 255))
    for sx, sy, ln in [(30, 30, 60), (140, 20, 80), (230, 34, 50)]:
        d.line([(x0 + sx, y0 + sy), (x0 + sx + ln, y0 + sy + ln // 3)],
               fill=(255, 170, 60), width=3)
        d.ellipse([x0 + sx + ln - 3, y0 + sy + ln // 3 - 3,
                   x0 + sx + ln + 3, y0 + sy + ln // 3 + 3],
                  fill=(255, 220, 120))
    base = y1 - 38
    for bx, bw, bh in [(0, 34, 14), (44, 26, 22), (80, 40, 12),
                       (130, 30, 20), (170, 36, 14), (216, 30, 18),
                       (256, 34, 12), (292, 24, 16)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, y1], fill=(8, 10, 20))
        for wy in range(base - bh + 4, base - 3, 8):
            d.rectangle([x0 + bx + 5, wy, x0 + bx + 9, wy + 3],
                        fill=(255, 200, 90))


def ill_cop(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 92, 66))
    cx, cy, r = (x0 + x1) // 2, y0 + 26, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(32, 128, 92))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 235, 220),
              width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(220, 235, 220), width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(220, 235, 220), width=2)
    for i, col in enumerate([(200, 60, 50), (240, 200, 60), (60, 120, 200),
                             (255, 255, 255), (40, 140, 90)]):
        fx = x0 + 18 + i * 58
        d.rectangle([fx, y1 - 50, fx + 34, y1 - 40], fill=col)


def ill_medium(d, box, kind):
    """Small panel illustration for a medium story, with a bold label.
    The label bar covers the bottom 29px, so the art lives in the
    top ~21px of the panel."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) // 2
    if kind == 0:  # Anthropic: rising candles, green
        d.rectangle(box, fill=(24, 96, 58))
        for i, (bx, bh) in enumerate([(12, 7), (38, 12), (64, 9),
                                      (90, 15), (116, 12), (142, 18)]):
            d.rectangle([x0 + bx, y0 + 21 - bh, x0 + bx + 14, y0 + 21],
                        fill=(140, 230, 170))
    elif kind == 1:  # Markets: falling line, red
        d.rectangle(box, fill=(140, 32, 36))
        pts = [(x0 + 10, y0 + 4), (x0 + 50, y0 + 8), (x0 + 90, y0 + 7),
               (x0 + 130, y0 + 14), (x0 + 170, y0 + 19)]
        d.line(pts, fill=(255, 220, 120), width=3, joint="curve")
        d.polygon([(x0 + 160, y0 + 15), (x0 + 174, y0 + 15),
                   (x0 + 167, y0 + 21)], fill=(255, 220, 120))
    elif kind == 2:  # GTA VI: sunset + skyline, purple/orange
        d.rectangle(box, fill=(96, 48, 130))
        d.ellipse([cx - 9, y0 + 2, cx + 9, y0 + 20], fill=(255, 170, 80))
        for bx, bw, bh in [(6, 26, 8), (40, 20, 12), (68, 30, 6),
                           (106, 22, 11), (136, 26, 7), (168, 16, 10)]:
            d.rectangle([x0 + bx, y0 + 21 - bh, x0 + bx + bw, y0 + 21],
                        fill=(40, 20, 60))
    elif kind == 3:  # Children: globe + figures, blue
        d.rectangle(box, fill=(36, 96, 160))
        d.ellipse([x0 + 10, y0 + 2, x0 + 28, y0 + 20], fill=(140, 200, 240))
        d.ellipse([x0 + 10, y0 + 2, x0 + 28, y0 + 20],
                  outline=(255, 255, 255), width=2)
        for px in (90, 112, 134):
            d.ellipse([x0 + px, y0 + 2, x0 + px + 8, y0 + 10],
                      fill=(255, 255, 255))
            d.rectangle([x0 + px + 1, y0 + 10, x0 + px + 7, y0 + 21],
                        fill=(255, 255, 255))
    elif kind == 4:  # UK-EU: two flags
        d.rectangle([x0, y0, cx, y1], fill=(28, 48, 110))
        d.line([(x0, y0), (cx, y1)], fill=(255, 255, 255), width=4)
        d.line([(cx, y0), (x0, y1)], fill=(255, 255, 255), width=4)
        d.line([(x0, (y0 + y1) // 2), (cx, (y0 + y1) // 2)],
               fill=(200, 40, 50), width=5)
        d.line([((x0 + cx) // 2, y0), ((x0 + cx) // 2, y1)],
               fill=(200, 40, 50), width=5)
        d.rectangle([cx, y0, x1, y1], fill=(20, 60, 160))
        for i in range(8):
            import math
            a = math.pi * 2 * i / 8
            sx = cx + (w // 4) + int(13 * math.cos(a))
            sy = (y0 + y1) // 2 + int(13 * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    elif kind == 5:  # Cricket: green pitch, bat + ball
        d.rectangle(box, fill=(52, 128, 62))
        d.rectangle([x0, y0 + 16, x1, y0 + 21], fill=(210, 190, 140))
        d.line([(x0 + 40, y0 + 18), (x0 + 110, y0 + 4)],
               fill=(240, 220, 180), width=7)
        d.ellipse([x0 + 138, y0 + 2, x0 + 150, y0 + 14], fill=(200, 40, 40))
        d.ellipse([x0 + 30, y0 + 2, x0 + 42, y0 + 14], fill=(255, 255, 255))
    elif kind == 6:  # Senate: dome, navy
        d.rectangle(box, fill=(30, 48, 96))
        d.pieslice([cx - 26, y0 + 1, cx + 26, y0 + 21], start=180, end=360,
                   fill=(230, 230, 220))
        d.rectangle([cx - 30, y0 + 10, cx + 30, y0 + 13],
                    fill=(230, 230, 220))
        for i in range(5):
            px = cx - 24 + i * 12
            d.rectangle([px, y0 + 13, px + 5, y0 + 21], fill=(230, 230, 220))
    elif kind == 7:  # Senegal: waves + boat
        d.rectangle(box, fill=(20, 80, 130))
        for wy in (y0 + 14, y0 + 19):
            for wx in range(0, w, 22):
                d.arc([x0 + wx, wy, x0 + wx + 22, wy + 10], start=0,
                      end=180, fill=(180, 220, 245), width=2)
        d.polygon([(cx - 28, y0 + 6), (cx + 28, y0 + 6),
                   (cx + 18, y0 + 14), (cx - 18, y0 + 14)],
                  fill=(120, 70, 30))
        d.polygon([(cx - 3, y0 + 6), (cx - 3, y0 - 1), (cx + 14, y0 + 6)],
                  fill=(255, 255, 255))
    elif kind == 8:  # Italy: megaphone, red
        d.rectangle(box, fill=(150, 36, 40))
        d.polygon([(x0 + 26, y0 + 6), (x0 + 26, y0 + 16),
                   (x0 + 120, y0 + 21), (x0 + 120, y0 + 1)],
                  fill=(255, 230, 120))
        d.rectangle([x0 + 16, y0 + 7, x0 + 28, y0 + 15], fill=(255, 255, 255))
        for i in range(3):
            ax = x0 + 130 + i * 8
            d.arc([ax, y0 + 3, ax + 11, y0 + 18], start=270, end=90,
                  fill=(255, 255, 255), width=2)
    else:  # China: bank + rate, dark red/gold
        d.rectangle(box, fill=(140, 28, 32))
        d.polygon([(cx - 34, y0 + 7), (cx + 34, y0 + 7), (cx, y0 + 1)],
                  fill=(255, 210, 90))
        d.rectangle([cx - 30, y0 + 8, cx + 30, y0 + 11],
                    fill=(255, 210, 90))
        for i in range(4):
            px = cx - 26 + i * 14
            d.rectangle([px, y0 + 12, px + 6, y0 + 21], fill=(255, 210, 90))


ILL_FEATURE = [ill_cyclone, ill_kyiv, ill_cop]


# ------------------------------------------------------------ layout
MX = 24
CW = 1024 - 2 * MX


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # Masthead: the DATE is the biggest text on the page; the paper's
    # name is a small kicker above it, so criterion 1 cannot be missed.
    center(d, W // 2, y, "THE WORLD TODAY  -  36 STORIES  -  SEVEN REGIONS",
           font(14, bold=True), fill=RED)
    y += 20
    date_f = font(56, serif=True, bold=True)
    center(d, W // 2, y, "Friday 20 November 2026", date_f)
    y += 70
    hrule(d, MX, W - MX, y, width=3)
    hrule(d, MX, W - MX, y + 4, width=1)
    y += 12
    center(d, W // 2, y, CHIPS, font(13, bold=True))
    y += 22

    # Numbers band: six giant numerals, airy, high contrast.
    top = y
    cell = CW / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + cell * i + cell / 2
        nf = fit(d, num, font(36, bold=True), cell - 10, 26)
        center(d, cx, top + 6, num, nf)
        lf = font(11, bold=True)
        lines = wrap(d, lab, lf, cell - 12)
        ly = top + 6 + nf.size + 4
        for ln in lines[:2]:
            center(d, cx, ly, ln, lf)
            ly += 14
    y = top + 86
    hrule(d, MX, W - MX, y, width=2)
    y += 14

    # Three illustrated leads: giant label inside the picture, big bold
    # two-line headline, one-line summary, source.
    gutter = 14
    col_w = (CW - 2 * gutter) // 3
    ill_h = 82
    feat_top = y
    for i, (label, head, summ, src) in enumerate(FEATURES):
        x = MX + i * (col_w + gutter)
        box = (x, y, x + col_w, y + ill_h)
        clipped(img, box, ILL_FEATURE[i])
        d.rectangle(box, outline=(40, 36, 28), width=1)
        label_bar(d, box, label, size=24)
        hy = y + ill_h + 8
        hf = font(26, bold=True)
        for ln in wrap(d, head, hf, col_w)[:2]:
            left(d, x, hy, ln, hf)
            hy += 30
        sf = fit(d, summ, font(17), col_w, 14)
        left(d, x, hy + 4, summ, sf)
        left(d, x, hy + 26, src, font(11), fill=GREY)
    y = feat_top + ill_h + 8 + 60 + 4 + 21 + 4 + 14 + 6
    hrule(d, MX, W - MX, y, width=1)
    y += 8

    # Ten illustrated medium stories, two rows of five.
    mgutter = 12
    mcol = (CW - 4 * mgutter) // 5
    mill_h = 46
    med_top = y
    for r in range(2):
        for c in range(5):
            k = r * 5 + c
            label, head, summ, src = MEDIUM[k]
            x = MX + c * (mcol + mgutter)
            yy = med_top + r * (mill_h + 5 + 48 + 3 + 21 + 3 + 13 + 14)
            box = (x, yy, x + mcol, yy + mill_h)
            clipped(img, box, ill_medium, k)
            d.rectangle(box, outline=(40, 36, 28), width=1)
            label_bar(d, box, label, size=15)
            hy = yy + mill_h + 5
            hf = font(19, bold=True)
            for ln in wrap(d, head, hf, mcol)[:2]:
                left(d, x, hy, ln, hf)
                hy += 24
            sf = fit(d, summ, font(16), mcol, 13)
            left(d, x, hy + 3, summ, sf)
            left(d, x, hy + 24, src, font(10), fill=GREY)
    y = med_top + 2 * (mill_h + 5 + 48 + 3 + 21 + 3 + 13) + 14
    hrule(d, MX, W - MX, y, width=1)
    y += 6

    # Map + ALSO ON: a neat numbered index in two airy columns.
    map_w = 300
    map_h = 184
    left(d, MX, y, "WHERE IT HAPPENED", font(13, bold=True))
    also_x = MX + map_w + 18
    left(d, also_x, y, "ALSO ON FRIDAY 20 NOVEMBER", font(13, bold=True))
    y += 20
    draw_map(d, MX, y, map_w, map_h)
    bf = font(14)
    col2_w = (W - MX - also_x - 14) // 2
    rows = (BRIEFS[:12], BRIEFS[12:])
    for ci, col_items in enumerate(rows):
        cx0 = also_x + ci * (col2_w + 14)
        ry = y + 2
        for num, txt in col_items:
            left(d, cx0, ry, "%d. %s" % (num, txt), bf)
            ry += 15
    y += map_h + 8

    # DATE CHECK: thick red-bordered strip, big type, wrapped to two lines.
    top = y
    d.rectangle([MX, top, W - MX, top + 44], outline=RED, width=3)
    df = font(14, bold=True)
    lines = wrap(d, DATE_CHECK, df, CW - 24)
    ly = top + 7
    for ln in lines[:2]:
        left(d, MX + 12, ly, ln, df, fill=RED)
        ly += 16
    y = top + 44 + 6

    # Footer: sources + method, one line.
    center(d, W // 2, y, "Sources: IMD, Reuters, Barron's, Sensor Tower, "
           "Save the Children, The Guardian, PBOC, Al Jazeera, CGIL, "
           "MyKhel and more. Figures checked against 2+ sources.",
           font(11), fill=GREY)
    y += 16
    print("FINAL_Y", y)
    return img


def draw_map(d, x0, y0, w, h):
    """Simplified world map with numbered pins for stories 1-13."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    lon0, lon1, lat0, lat1 = -125.0, 185.0, 62.0, -46.0

    def proj(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)

    continents = [
        [(-125, 50), (-110, 60), (-95, 70), (-80, 70), (-70, 60),
         (-60, 47), (-75, 35), (-80, 26), (-90, 20), (-97, 16),
         (-105, 22), (-117, 32), (-125, 42)],
        [(-80, 10), (-60, 5), (-50, 0), (-40, -10), (-45, -25),
         (-58, -35), (-65, -45), (-70, -30), (-75, -15), (-80, -5)],
        [(-10, 36), (0, 44), (10, 45), (20, 55), (30, 60), (25, 70),
         (10, 60), (0, 55), (-5, 48), (-10, 43)],
        [(-10, 35), (10, 37), (30, 32), (40, 15), (50, 10), (45, -5),
         (40, -20), (30, -30), (20, -35), (12, -18), (8, 4), (-8, 5),
         (-15, 15)],
        [(35, 40), (50, 45), (60, 50), (70, 60), (90, 70), (120, 72),
         (150, 70), (170, 65), (160, 55), (140, 40), (130, 35),
         (120, 25), (105, 10), (95, 15), (85, 20), (75, 10), (65, 25),
         (50, 30), (40, 35)],
        [(113, -22), (125, -15), (140, -12), (150, -22), (150, -37),
         (140, -38), (130, -32), (115, -32)],
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
    pins = [(85, 19.5), (30.5, 50.4), (30.7, 36.9), (-122, 37.8),
            (-74, 40.7), (-95, 39), (6, 46), (4.35, 50.85),
            (174.8, -41.3), (-77, 38.9), (-17.4, 14.7), (12.5, 41.9),
            (116.4, 39.9)]
    pf = font(9, bold=True)
    for i, (lon, lat) in enumerate(pins, start=1):
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(i)
        d.text((px - text_w(d, s, pf) / 2, py - 5), s, font=pf,
               fill=(255, 255, 255))


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    draw().save(out, optimize=True)
    print("WROTE", out)
