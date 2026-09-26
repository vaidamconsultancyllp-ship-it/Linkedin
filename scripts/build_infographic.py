"""Render a one-page structured infographic (numbered cards, flow, table) to PNG.

    python3 scripts/build_infographic.py output/2026-09-30/infographic.json

infographic.json:
{
  "title": "Pvt Ltd vs LLP vs OPC",
  "subtitle": "Which structure should you choose?",
  "tagline": "A simple guide for Indian founders",
  "badge": ["By Vaidam Consultancy LLP", "vaidamconsultancy.in"],
  "rows": [
    {"type": "cards", "cards": [
      {"heading": "...", "bullets": ["...", "..."], "highlight": "optional big text"}]},
    {"type": "flow", "heading": "...", "steps": [{"title": "...", "text": "..."}]},
    {"type": "mixed", "cards": [
      {"heading": "...", "table": [["Aspect", "A", "B"], ["...", "...", "..."]], "span": 2},
      {"heading": "...", "bullets": ["..."]}]}
  ],
  "footer": "Need help? DM us · vaidamconsultancy.in",
  "disclaimer": "For education purposes only"
}

Cards are numbered automatically in reading order. Writes infographic.png
next to the JSON; post it with linkedin_post.py --image.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from build_carousel import BG, BLUE, GOLD, ORANGE, TEAL, TEXT, font, wrap

W = 1600
PAD = 40
GAP = 24
INK = (18, 32, 44)
SOFT = (90, 104, 116)
PAGE = (244, 247, 250)
PALETTE = [TEAL, BLUE, GOLD, ORANGE]
TINTS = {TEAL: (226, 242, 241), BLUE: (224, 241, 247), GOLD: (253, 244, 226), ORANGE: (252, 232, 223)}


def lines_height(draw, text, fnt, width, spacing=1.3):
    return len(wrap(draw, text, fnt, width)) * int(fnt.size * spacing)


def draw_lines(draw, xy, text, fnt, fill, width, spacing=1.3):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * spacing)
    return y


class Card:
    """Measures and draws one numbered card."""

    HEAD = font(34, True)
    BODY = font(26)
    BIG = font(38, True)
    CELL = font(22)
    CELL_B = font(22, True)

    def __init__(self, data, number, color):
        self.data, self.number, self.color = data, number, color

    def inner(self, width):
        return width - 2 * 28

    def table_layout(self, draw, width):
        rows = self.data["table"]
        cols = len(rows[0])
        first = int(self.inner(width) * 0.24)
        rest = (self.inner(width) - first) / (cols - 1)
        widths = [first] + [rest] * (cols - 1)
        heights = []
        for r, row in enumerate(rows):
            h = max(lines_height(draw, str(cell), self.CELL_B if (r == 0 or c == 0) else self.CELL, w - 20, 1.25)
                    for c, (cell, w) in enumerate(zip(row, widths)))
            heights.append(h + 18)
        return widths, heights

    def height(self, draw, width):
        h = 28 + 60  # top padding + heading row
        body = self.inner(width)
        if self.data.get("highlight"):
            h += lines_height(draw, self.data["highlight"], self.BIG, body, 1.15) + 16
        for b in self.data.get("bullets", []):
            h += lines_height(draw, b, self.BODY, body - 30) + 10
        if self.data.get("table"):
            h += sum(self.table_layout(draw, width)[1]) + 10
        return h + 28

    def draw(self, draw, x, y, width, height):
        draw.rounded_rectangle([x, y, x + width, y + height], radius=22, fill=TINTS[self.color],
                               outline=self.color, width=3)
        cx, cy = x + 28, y + 28
        draw.ellipse([cx, cy, cx + 50, cy + 50], fill=self.color)
        num = str(self.number)
        nf = font(30, True)
        draw.text((cx + 25 - draw.textlength(num, font=nf) / 2, cy + 7), num, font=nf, fill=TEXT)
        draw_lines(draw, (cx + 66, cy + 6), self.data["heading"], self.HEAD, INK, self.inner(width) - 66, 1.15)
        cy += 60 + (lines_height(draw, self.data["heading"], self.HEAD, self.inner(width) - 66, 1.15) - 40)
        body = self.inner(width)
        if self.data.get("highlight"):
            cy = draw_lines(draw, (cx, cy + 8), self.data["highlight"], self.BIG, self.color, body, 1.15) + 8
        for b in self.data.get("bullets", []):
            draw.ellipse([cx + 4, cy + 12, cx + 14, cy + 22], fill=self.color)
            cy = draw_lines(draw, (cx + 30, cy), b, self.BODY, INK, body - 30) + 10
        if self.data.get("table"):
            widths, heights = self.table_layout(draw, width)
            ty = cy + 6
            for r, row in enumerate(self.data["table"]):
                if r == 0:
                    draw.rectangle([cx, ty, cx + body, ty + heights[r]], fill=self.color)
                elif r % 2 == 0:
                    draw.rectangle([cx, ty, cx + body, ty + heights[r]], fill=(255, 255, 255))
                tx = cx
                for c, (cell, w) in enumerate(zip(row, widths)):
                    fnt = self.CELL_B if (r == 0 or c == 0) else self.CELL
                    fill = TEXT if r == 0 else INK
                    draw_lines(draw, (tx + 10, ty + 9), str(cell), fnt, fill, w - 20, 1.25)
                    tx += w
                draw.line([cx, ty + heights[r], cx + body, ty + heights[r]], fill=(200, 208, 216), width=1)
                ty += heights[r]


def draw_flow(draw, row, number, y, measure_only=False):
    steps = row["steps"]
    n = len(steps)
    arrow = 34
    box_w = (W - 2 * PAD - 56 - (n - 1) * arrow) / n
    head, title_f, text_f = font(34, True), font(26, True), font(23)
    heights = [lines_height(draw, s["title"], title_f, box_w - 36, 1.2) + 14 +
               lines_height(draw, s["text"], text_f, box_w - 36, 1.3) for s in steps]
    box_h = max(heights) + 44
    total = 28 + 60 + box_h + 28
    if measure_only:
        return total
    x0 = PAD
    draw.rounded_rectangle([x0, y, W - PAD, y + total], radius=22, fill=(255, 255, 255), outline=BLUE, width=3)
    cx, cy = x0 + 28, y + 28
    draw.ellipse([cx, cy, cx + 50, cy + 50], fill=BLUE)
    nf = font(30, True)
    draw.text((cx + 25 - draw.textlength(str(number), font=nf) / 2, cy + 7), str(number), font=nf, fill=TEXT)
    draw.text((cx + 66, cy + 6), row["heading"], font=head, fill=INK)
    by = cy + 60
    bx = cx
    for i, s in enumerate(steps):
        color = PALETTE[i % len(PALETTE)]
        draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=16, fill=TINTS[color], outline=color, width=2)
        ty = draw_lines(draw, (bx + 18, by + 18), f"{i + 1}. {s['title']}", title_f, INK, box_w - 36, 1.2)
        draw_lines(draw, (bx + 18, ty + 10), s["text"], text_f, SOFT, box_w - 36)
        if i < n - 1:
            ax, ay = bx + box_w + 6, by + box_h / 2
            draw.polygon([(ax, ay - 14), (ax + arrow - 12, ay), (ax, ay + 14)], fill=BLUE)
        bx += box_w + arrow
    return total


def render(spec):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    title_f, sub_f, tag_f = font(76, True), font(40, True), font(28)
    badge_f, badge_b = font(24), font(26, True)

    badge_w = 330
    title_w = W - 2 * PAD - badge_w - 30
    header_h = 36 + lines_height(probe, spec["title"], title_f, title_w, 1.1) + \
        lines_height(probe, spec.get("subtitle", ""), sub_f, title_w, 1.2) + \
        lines_height(probe, spec.get("tagline", ""), tag_f, title_w) + 40

    # Lay out rows: (kind, payload, height)
    number = 1
    layout = []
    for row in spec["rows"]:
        if row["type"] == "flow":
            layout.append(("flow", (row, number), draw_flow(probe, row, number, 0, measure_only=True)))
            number += 1
            continue
        cards = row["cards"]
        spans = [c.get("span", 1) for c in cards]
        unit = (W - 2 * PAD - GAP * (sum(spans) - 1)) / sum(spans)
        items = []
        for c, span in zip(cards, spans):
            width = unit * span + GAP * (span - 1)
            items.append((Card(c, number, PALETTE[(number - 1) % len(PALETTE)]), width))
            number += 1
        h = max(card.height(probe, width) for card, width in items)
        layout.append(("cards", items, h))

    footer_h = 90
    H = header_h + GAP + sum(h for *_, h in layout) + GAP * len(layout) + footer_h
    img = Image.new("RGB", (W, int(H)), PAGE)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, header_h], fill=BG)
    for i, color in enumerate(PALETTE):
        d.rectangle([i * W // 4, header_h - 10, (i + 1) * W // 4, header_h], fill=color)
    y = draw_lines(d, (PAD, 30), spec["title"], title_f, TEXT, title_w, 1.1)
    if spec.get("subtitle"):
        y = draw_lines(d, (PAD, y + 4), spec["subtitle"], sub_f, GOLD, title_w, 1.2)
    if spec.get("tagline"):
        draw_lines(d, (PAD, y + 6), spec["tagline"], tag_f, (200, 212, 222), title_w)
    badge = spec.get("badge", [])
    if badge:
        bx, by = W - PAD - badge_w, 34
        bh = 30 + 40 * len(badge)
        d.rounded_rectangle([bx, by, bx + badge_w, by + bh], radius=16, fill=(255, 255, 255))
        for i, line in enumerate(badge):
            f = badge_b if i == 0 else badge_f
            size = f.size
            while d.textlength(line, font=f) > badge_w - 28 and size > 14:
                size -= 1
                f = font(size, i == 0)
            d.text((bx + badge_w / 2 - d.textlength(line, font=f) / 2, by + 16 + i * 40), line, font=f,
                   fill=BG if i == 0 else SOFT)

    y = header_h + GAP
    for kind, payload, h in layout:
        if kind == "flow":
            row, n = payload
            draw_flow(d, row, n, y)
        else:
            x = PAD
            for card, width in payload:
                card.draw(d, x, y, width, h)
                x += width + GAP
        y += h + GAP

    # Footer
    d.rectangle([0, H - footer_h, W, H], fill=BG)
    ff = font(30, True)
    d.text((PAD, H - footer_h + 28), spec.get("footer", ""), font=ff, fill=GOLD)
    disc = spec.get("disclaimer", "")
    if disc:
        df = font(22)
        d.text((W - PAD - d.textlength(disc, font=df), H - footer_h + 34), disc, font=df, fill=(200, 212, 222))
    return img


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    path = Path(sys.argv[1])
    img = render(json.loads(path.read_text()))
    out = path.parent / "infographic.png"
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
