---
description: Research this week's top 5 AI/tech stories, write a LinkedIn post + 7-slide carousel, and publish it
argument-hint: "[optional topic focus, e.g. 'AI agents'] [--dry-run]"
allowed-tools: WebSearch, WebFetch, Bash(python3 scripts/*), Bash(python scripts/*), Bash(mkdir *), Read, Write
---

Run the full LinkedIn pipeline end to end. Focus / flags: $ARGUMENTS

1. **Research.** Use WebSearch for AI and tech news from the last 7 days
   (focus on the topic above if one is given). Look at several sources, then
   pick the **5 most important stories** — prefer real launches, research,
   funding, policy, or big product changes over opinion pieces. Skip anything
   you can't confirm from a credible source.

2. **Set up today's folder.** `mkdir -p output/<YYYY-MM-DD>`.

3. **Hook.** Run `python3 scripts/next_hook.py` and use its output as the
   first line of the post (it rotates so posts don't all open the same way).

4. **Write the post** to `output/<date>/post.txt`, following the voice rules
   in CLAUDE.md:
   - Line 1: the hook. Blank line.
   - One short line per story: number emoji, the story in plain words, one
     takeaway. Blank line between stories.
   - A closing question that invites comments.
   - 3–5 relevant hashtags on the last line.
   - Under 1,300 characters in total. No links in the body (they reduce reach).

5. **Write the carousel content** to `output/<date>/content.json` in the
   format documented at the top of `scripts/build_carousel.py`: title,
   subtitle, date, author (from CLAUDE.md), 5 stories each with `headline`
   (≤ 70 chars), `summary` (≤ 220 chars), `why` (≤ 140 chars), `source`,
   and a `cta`.

6. **Build the carousel.** `python3 scripts/build_carousel.py output/<date>/content.json`.
   Read `slide-1.png` and one story slide to check nothing is cut off or
   overflowing; shorten the text and rebuild if it is.

7. **Publish.**
   - If `--dry-run` is in the arguments, run
     `python3 scripts/linkedin_post.py --text output/<date>/post.txt --pdf output/<date>/carousel.pdf --title "<carousel title>" --dry-run`
     and stop.
   - Otherwise run the same command without `--dry-run`.

8. **Report** the 5 stories you chose (with source links), the post text, and
   the published URL.
