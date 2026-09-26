"""Render a 7-slide editorial carousel (cover + 5 stories + CTA) to PNG + PDF.

    python scripts/build_carousel.py output/2026-09-26/content.json

content.json:
{
  "title": "This Week in AI & Tech",
  "subtitle": "5 stories worth your attention",
  "date": "Sep 26, 2026",
  "author": "Your Name",
  "stories": [
    {"headline": "...", "summary": "...", "why": "...", "source": "The Verge"}
  ],
  "cta": "Follow for a weekly AI & tech briefing"
}

Writes slide-1.png ... slide-7.png and carousel.pdf next to content.json.
LinkedIn shows the PDF as a swipeable document post.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
MARGIN = 90
BG = (15, 17, 26)
PANEL = (27, 31, 46)
TEXT = (240, 242, 248)
MUTED = (150, 158, 180)
ACCENT = (10, 132, 255)

FONT_DIRS = [
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/Library/Fonts"),
    Path("C:/Windows/Fonts"),
]


def font(size, bold=False):
    names = (["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"] if bold
             else ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf"])
    for d in FONT_DIRS:
        for n in names:
            if (d / n).exists():
                return ImageFont.truetype(str(d / n), size)
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, max_width):
    """Wrap text to fit max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(), ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_block(draw, xy, text, fnt, fill, max_width, spacing=1.3):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * spacing)
    return y


def frame(page, total, author):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=ACCENT)
    footer = font(28)
    d.text((MARGIN, H - 90), author, font=footer, fill=MUTED)
    label = f"{page}/{total}"
    d.text((W - MARGIN - d.textlength(label, font=footer), 60), label, font=footer, fill=MUTED)
    if page < total:
        swipe = "Swipe  →"
        d.text((W - MARGIN - d.textlength(swipe, font=footer), H - 90), swipe, font=footer, fill=ACCENT)
    return img, d


def cover(c, total):
    img, d = frame(1, total, c.get("author", ""))
    d.text((MARGIN, 200), c.get("date", "").upper(), font=font(34, True), fill=ACCENT)
    y = draw_block(d, (MARGIN, 280), c["title"], font(104, True), TEXT, W - 2 * MARGIN, 1.15)
    d.rectangle([MARGIN, y + 40, MARGIN + 160, y + 52], fill=ACCENT)
    draw_block(d, (MARGIN, y + 100), c.get("subtitle", ""), font(48), MUTED, W - 2 * MARGIN)
    return img


def story(s, n, page, total, author):
    img, d = frame(page, total, author)
    d.text((MARGIN, 150), f"{n:02d}", font=font(150, True), fill=ACCENT)
    y = draw_block(d, (MARGIN, 360), s["headline"], font(62, True), TEXT, W - 2 * MARGIN, 1.2)
    y = draw_block(d, (MARGIN, y + 40), s["summary"], font(38), TEXT, W - 2 * MARGIN, 1.4)
    if s.get("why"):
        top = y + 40
        body = font(34)
        lines = wrap(d, s["why"], body, W - 2 * MARGIN - 80)
        bottom = top + 110 + len(lines) * int(body.size * 1.4)
        d.rounded_rectangle([MARGIN, top, W - MARGIN, bottom], radius=24, fill=PANEL)
        d.text((MARGIN + 40, top + 35), "WHY IT MATTERS", font=font(28, True), fill=ACCENT)
        draw_block(d, (MARGIN + 40, top + 90), s["why"], body, MUTED, W - 2 * MARGIN - 80, 1.4)
    if s.get("source"):
        d.text((MARGIN, H - 170), f"Source: {s['source']}", font=font(28), fill=MUTED)
    return img


def cta(c, total):
    img, d = frame(total, total, c.get("author", ""))
    y = draw_block(d, (MARGIN, 380), "Found this useful?", font(88, True), TEXT, W - 2 * MARGIN, 1.15)
    y = draw_block(d, (MARGIN, y + 50), c.get("cta", "Follow for more"), font(50), MUTED, W - 2 * MARGIN)
    for i, line in enumerate(["→ Repost to share", "→ Comment your take", "→ Follow for next week"]):
        d.text((MARGIN, y + 120 + i * 80), line, font=font(42, True), fill=ACCENT)
    return img


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    path = Path(sys.argv[1])
    c = json.loads(path.read_text())
    stories = c["stories"][:5]
    total = len(stories) + 2
    slides = [cover(c, total)]
    slides += [story(s, i + 1, i + 2, total, c.get("author", "")) for i, s in enumerate(stories)]
    slides.append(cta(c, total))

    out = path.parent
    for i, img in enumerate(slides, 1):
        img.save(out / f"slide-{i}.png")
    pdf = out / "carousel.pdf"
    slides[0].save(pdf, save_all=True, append_images=slides[1:], resolution=150)
    print(pdf)


if __name__ == "__main__":
    main()
