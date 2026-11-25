#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday, 25 November 2026.

A single typographic newspaper front page, rendered with Pillow. All fifty
stories come from the verified story list for this day; nothing is invented.
Layout is a flowing column of blocks: masthead, lead story, supporting
stories, then two dense index sections. Text is measured as it is drawn so
nothing overlaps; any line that would overflow its column is shrunk, then
trimmed with an ellipsis.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 32
CW = W - 2 * MARGIN  # 960

PAPER = (247, 242, 231)
INK = (17, 17, 17)
FAINT = (90, 84, 74)
RED = (164, 30, 34)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width, max_lines=None):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        # squeeze an ellipsis onto the last line
        while lines and fnt.getlength(lines[-1] + " ...") > width:
            lines[-1] = lines[-1][:-1]
        if lines:
            lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def fit_one_line(text, fnt_path, size, width, floor=10):
    """Largest font size (down to floor) that fits text on one line."""
    s = size
    while s > floor:
        f = font(fnt_path, s)
        if f.getlength(text) <= width:
            return f, text
        s -= 1
    f = font(fnt_path, floor)
    t = text
    while f.getlength(t + " ...") > width and len(t) > 4:
        t = t[:-1]
    return f, t


def line_height(fnt, leading=1.18):
    return int(fnt.size * leading)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 0

    def rule(self, y, weight=1, color=RULE):
        self.d.line([(MARGIN, y), (W - MARGIN, y)], fill=color, width=weight)

    def text(self, x, y, s, fnt, color=INK):
        self.d.text((x, y), s, font=fnt, fill=color)

    def centred(self, y, s, fnt, color=INK):
        w = self.d.textlength(s, font=fnt)
        self.d.text(((W - w) / 2, y), s, font=fnt, fill=color)
        return w

    def kicker(self, x, y, s, color=RED):
        self.text(x, y, s.upper(), font(SANS_B, 12), color=color)

    def block(self, x, y, width, kicker_s, head, head_size, deck,
              deck_size, max_head_lines=2, max_deck_lines=3):
        """A headed story block; returns the y just below it."""
        yy = y
        if kicker_s:
            self.kicker(x, yy, kicker_s)
            yy += 16
        hf = font(SERIF_B, head_size)
        for ln in wrap(head, hf, width, max_head_lines):
            self.text(x, yy, ln, hf)
            yy += line_height(hf, 1.12)
        if deck:
            df = font(SERIF, deck_size)
            for ln in wrap(deck, df, width, max_deck_lines):
                self.text(x, yy, ln, df, color=(38, 36, 32))
                yy += line_height(df, 1.16)
        return yy


# ---------------------------------------------------------------- stories
# (headline, one-line fact) — facts taken only from the verified list.

LEAD = (
    "NATO sends AWACS to Poland after Russian missiles land",
    "Three Kh-101 cruise missiles crashed in south-east Poland on 20 Nov during a "
    "huge Russian barrage on Ukraine. A second incursion \u2014 a Russian drone \u2014 "
    "came overnight on 24 Nov, and Poland renewed its push for a permanent US troop presence.",
)

PAIR = [
    ("China probes Shanghai chief Chen Jining",
     "Anti-graft watchdog CCDI is investigating Politburo member Chen Jining, 62, "
     "for \u201cserious violations of discipline and law\u201d \u2014 the fourth Politburo "
     "member probed since 2025."),
    ("Tanker war in the Strait of Hormuz",
     "Iran\u2019s IRGC Navy claims five to six tankers struck mines since 22 Nov \u2014 "
     "unverified. UKMTO confirmed three projectile strikes near Khasab; oil traffic "
     "is down 40% and Brent is about $102."),
]

QUAD = [
    ("Albanese hits record low in Australia",
     "Guardian Essential poll: approval 32%, disapproval 60%, net \u221228 \u2014 his "
     "worst. Reserve Bank rate 4.85%, an 18-year high."),
    ("South Korea cracks down on AI exam cheating",
     "Max prison term for state-exam cheating to rise from 2 to 5 years after the "
     "top tax-exam scorer confessed to using a hidden-camera AI."),
    ("Thanksgiving storm bears down on the US East Coast",
     "Storm peaks on Thanksgiving (26 Nov) with 50\u201360 mph gusts; FAA expects the "
     "busiest Thanksgiving travel in 16 years."),
    ("Gold slides as Fed\u2019s Williams turns hawkish",
     "Spot gold about $3,570, down about 2% after NY Fed chief Williams called "
     "inflation near 3.5% \u201cunacceptably high\u201d."),
]

TRIO = [
    ("UK warns firms of Russian sabotage threat",
     "MI5 and the MoD warned UK firms supplying Ukraine to \u201cact now\u201d against sabotage."),
    ("Sheikh Hasina plans return to Bangladesh",
     "Ousted PM Hasina plans to return from India on 16 Dec, Victory Day."),
    ("Nvidia soars as Jensen Huang returns as CEO",
     "Board reinstated Huang on 23 Nov; shares jumped 31.5% (about +$950bn)."),
]

MIDDLE = [
    ("COP31 climate summit collapses",
     "COP31 in Antalya ended with no deal \u2014 the first UN climate summit collapse since 2009."),
    ("Denmark foils Russian plot to kill rapper",
     "Danish intelligence says Russia plotted to kill rapper Kyivstoner; two men arrested."),
    ("Record settler attacks mar West Bank olive harvest",
     "More than 400 settler attacks since September \u2014 the worst olive harvest on record."),
    ("French officers convicted of racist assault",
     "Three Paris officers convicted over the racist assault on producer Michel Zecler."),
    ("World court: Myanmar committed genocide",
     "ICJ ruled 9\u20136 Myanmar committed genocide against the Rohingya \u2014 a first for the court."),
    ("Israel kills Hamas commander as Gaza truce stalls",
     "Israel killed Rafah Brigade commander Samir Mahmoud Abu Younis, 53, in Khan Younis."),
    ("Van Gogh sells for record $190.4m",
     "\u201cChâtaigniers en fleurs\u201d (1890) sold at Sotheby\u2019s for $190.4m \u2014 a Van Gogh record."),
    ("US and Venezuela sign military deal",
     "Defence Secretary Hegseth signed a deal in Caracas to re-establish military ties."),
    ("AI claims to have cracked the Riemann Hypothesis",
     "Anthropic mathematician Levent Alpoge claims a proof \u2014 peer review still pending."),
    ("Paolo Bulgari dies at 89",
     "The jeweller who built the family firm into a global luxury house died in Rome at 89."),
    ("Mexico captures \u201cEl Chapo Isidro\u201d",
     "FBI Top 10 fugitive Fausto Isidro Meza-Flores, 44, captured in Guasave; 11 killed."),
    ("Gen Z strikes across Europe",
     "Protests in 25+ countries and 400 cities over climate, jobs and housing."),
    ("Triple-tap strike kills boy, 7, in Kryvyi Rih",
     "A Russian strike on Zelenskyy\u2019s home town killed a boy, 7, and a paramedic, 20."),
    ("Ukrainian drones sink Russian warship off Libya",
     "Ukrainian sea drones sank the Russian corvette Merkury in Benghazi, Libya."),
    ("Thousands march in Karachi against splitting Sindh",
     "Thousands of Sindhi nationalists marched against a plan to divide Sindh province."),
    ("India\u2013Nepal rail link opens",
     "Modi and Nepal PM Balen Shah flagged off the Saryu-Kamala Express, 604 km."),
    ("EU adopts 145 new Russia listings",
     "EU ministers adopted 145 Russia sanctions listings, including 49\u201350 banks."),
    ("First Trump\u2013Xi\u2013Putin summit",
     "The three leaders met in Shenzhen and agreed a nuclear-risk declaration."),
    ("Israel elects new Knesset speaker",
     "Matan Kahana elected Knesset speaker 66\u201352, replacing Amir Ohana."),
    ("UK records worst heat deaths on record",
     "Heat deaths in Britain hit 5,258 in summer 2026, the highest since records began."),
]

BRIEFS = [
    ("Taiwan votes Saturday", "Local elections on 28 Nov."),
    ("Most Germans oppose Ukraine aid", "Koerber survey: majority opposed."),
    ("Magyar to meet Zelenskyy", "Hungarian PM cites a thaw in ties."),
    ("Norway\u2013Ukraine drone pact", "Desna system, built with Kongsberg."),
    ("Two killed in Zaporizhzhia", "Russian attack overnight, governor says."),
    ("Intruders at William\u2019s home", "The Sun reported the break-in."),
    ("Car bomb injures 23 in Colombia", "23 hurt in Villavicencio."),
    ("Murmansk governor arrested", "Rare arrest of a regional leader."),
    ("Gaza meningitis alert", "Cases spiking, officials say."),
    ("UK sanctions Houthi leaders", "Over alleged torture and rape."),
    ("Hamas security chief killed", "Source: Israeli airstrike in Gaza."),
    ("Fiji drought emergency", "El Nino dry spell blamed."),
    ("Malaysia to return Rohingya", "Refugees to be sent to Myanmar."),
    ("GPS jamming hits 140 flights", "Russian ship blamed for jamming."),
    ("CIA and ODNI hit by cyberattack", "Some public information affected."),
    ("Trump pardons two turkeys", "Freedom and Feathers spared."),
    ("Bangladesh garment clashes", "Pay protests halt production."),
    ("Australia to fine big tech", "Multibillion-dollar fines planned."),
    ("Landmine casualties at 5-year high", "Myanmar and Syria fuel the rise."),
    ("Day against violence to women", "16 Days of Activism opens today."),
]


def section_bar(pg, y, left, right):
    pg.d.rectangle([MARGIN, y, W - MARGIN, y + 24], fill=INK)
    pg.text(MARGIN + 10, y + 4, left, font(SANS_B, 14), PAPER)
    rw = pg.d.textlength(right, font=font(SANS_B, 12))
    pg.text(W - MARGIN - 10 - rw, y + 5, right, font(SANS_B, 12), (210, 205, 192))
    return y + 24


def index_item(pg, x, y, width, head, fact):
    """One-line headline + one-line fact, shrunk to fit; returns bottom y."""
    hf, ht = fit_one_line(head, SERIF_B, 14, width)
    pg.text(x, y, ht, hf)
    ff, ft = fit_one_line(fact, SERIF, 12, width)
    pg.text(x, y + 14, ft, ff, color=(38, 36, 32))
    return y + 29


def brief_item(pg, x, y, width, head, fact):
    hf, ht = fit_one_line(head, SERIF_B, 12, width)
    pg.text(x, y, ht, hf)
    ff, ft = fit_one_line(fact, SERIF, 11, width)
    pg.text(x, y + 13, ft, ff, color=(38, 36, 32))
    return y + 28


def main():
    pg = Page()
    d = pg.d
    y = 12

    # ---- masthead ------------------------------------------------------
    pg.rule(y, 1)
    y += 6
    pg.centred(y, "THE WORLD TODAY", font(SERIF_B, 54))
    y += 64
    pg.centred(y, "TUESDAY, 25 NOVEMBER 2026", font(SANS_B, 15))
    y += 20
    pg.rule(y, 4)
    y += 5
    pg.rule(y, 1)
    y += 8

    # ---- lead story ----------------------------------------------------
    y = pg.block(MARGIN, y, CW, "War in Europe \u2014 NATO \u00b7 Poland",
                 LEAD[0], 28, LEAD[1], 14, max_head_lines=2, max_deck_lines=2)
    y += 4
    pg.rule(y, 1)
    y += 6

    # ---- pair: stories 2 and 3 ----------------------------------------
    col_w = (CW - 24) // 2
    y2 = pg.block(MARGIN, y, col_w, "China", PAIR[0][0], 19, PAIR[0][1], 13)
    y3 = pg.block(MARGIN + col_w + 24, y, col_w, "Strait of Hormuz",
                  PAIR[1][0], 19, PAIR[1][1], 13)
    y = max(y2, y3) + 4
    pg.rule(y, 1)
    y += 6

    # ---- quad: stories 4-7, two by two ---------------------------------
    row_h = 0
    for i in range(0, 4, 2):
        yy = y
        for j, idx in enumerate((i, i + 1)):
            x = MARGIN + j * (col_w + 24)
            end = pg.block(x, yy, col_w, None, QUAD[idx][0], 17,
                           QUAD[idx][1], 13, max_head_lines=2, max_deck_lines=2)
            row_h = max(row_h, end - yy)
        y += row_h + 4
        row_h = 0
    pg.rule(y, 1)
    y += 6

    # ---- trio: stories 8-10, three columns -----------------------------
    tcol = (CW - 2 * 20) // 3
    ends = []
    for j, (head, deck) in enumerate(TRIO):
        x = MARGIN + j * (tcol + 20)
        ends.append(pg.block(x, y, tcol, None, head, 16, deck, 12,
                             max_head_lines=2, max_deck_lines=2))
    y = max(ends) + 6

    # ---- middle index: stories 11-30, two columns ----------------------
    y = section_bar(pg, y, "MORE WORLD NEWS", "STORIES 11\u201330") + 6
    top = y
    for col in range(2):
        yy = top
        for item in MIDDLE[col * 10:(col + 1) * 10]:
            yy = index_item(pg, MARGIN + col * (col_w + 24), yy, col_w,
                            item[0], item[1])
        y = max(y, yy)
    y += 2

    # ---- briefs: stories 31-50, four columns ---------------------------
    y = section_bar(pg, y, "IN BRIEF \u2014 25 NOVEMBER", "STORIES 31\u201350") + 6
    bcol = (CW - 3 * 16) // 4
    top = y
    for col in range(4):
        yy = top
        for item in BRIEFS[col * 5:(col + 1) * 5]:
            yy = brief_item(pg, MARGIN + col * (bcol + 16), yy, bcol,
                            item[0], item[1])
        y = max(y, yy)
    y += 4
    pg.rule(y, 1)
    y += 6
    pg.centred(y, "THE WORLD TODAY  \u00b7  TUESDAY, 25 NOVEMBER 2026  \u00b7  "
                  "ALL 50 STORIES VERIFIED AGAINST LIVE SOURCES",
               font(SANS, 11), color=FAINT)
    print("content bottom y =", y + 12, "of", H)

    pg.img.save("entry.png", optimize=True)
    print("saved entry.png", pg.img.size)


if __name__ == "__main__":
    main()
