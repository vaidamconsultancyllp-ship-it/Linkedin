---
description: Research Indian business-compliance news and deadlines, write a LinkedIn post + 7-slide carousel, and publish it
argument-hint: "[optional pillar or topic, e.g. 'GST' or 'explainer: LLP vs Pvt Ltd'] [--dry-run]"
allowed-tools: WebSearch, WebFetch, Bash(python3 scripts/*), Bash(python scripts/*), Bash(mkdir *), Read, Write
---

Run the full LinkedIn pipeline end to end. Topic / flags: $ARGUMENTS

Follow the audience, content pillars, voice and accuracy rules in CLAUDE.md.

1. **Pick the pillar.** Use the topic above if given. Otherwise pick the
   content pillar from CLAUDE.md that fits this week best: a deadline alert when
   big filings are due in the next 30 days, a rule change when a major MCA /
   CBDT / GST / RBI notification came out, otherwise an explainer, costly
   mistakes or a checklist.

2. **Research.** Use WebSearch for Indian compliance news from the last 7
   days and filings due in the next 30 days (MCA/ROC, income tax, GST, LLP,
   FEMA, Startup India). Confirm every date and rupee amount from an
   official or reliable professional source. Pick **5 items**, most urgent or
   most useful first. Note whether any extension has actually been notified.

3. **Set up today's folder.** `mkdir -p output/<YYYY-MM-DD>`.

4. **Hook.** Run `python3 scripts/next_hook.py` and use its output as the
   first line of the post (adapt the wording slightly if it doesn't fit the pillar).

5. **Write the post** to `output/<date>/post.txt`:
   - Line 1: the hook. Blank line.
   - One short block per item: a marker emoji and the form/topic with its date,
     then who it applies to, then the action or penalty. Blank line between items.
   - A soft call to action (question, or "Comment 'CHECKLIST'" / "DM us").
   - For deadline posts: "Dates as per current notifications; check for any extension."
   - 3–5 hashtags on the last line.
   - Under 1,300 characters. No links in the body.

6. **Write the carousel content** to `output/<date>/content.json` in the
   format documented at the top of `scripts/build_carousel.py`: title,
   subtitle, date, author, `why_label` ("WHAT TO DO" for deadlines and
   rule changes), 5 items each with `tag` (e.g. "DUE 30 SEP 2026", ≤ 22
   chars), `headline` (≤ 60 chars), `summary` (≤ 200 chars), `why` (the
   action, ≤ 130 chars), `source`, then `cta_heading`, `cta` and `cta_lines`.

7. **Build the carousel.** `python3 scripts/build_carousel.py output/<date>/content.json`.
   Read `slide-1.png` and one item slide to check nothing is cut off; shorten
   and rebuild if it is.

8. **Publish.**
   - If `--dry-run` is in the arguments, run
     `python3 scripts/linkedin_post.py --text output/<date>/post.txt --pdf output/<date>/carousel.pdf --title "<carousel title>" --dry-run`
     and stop.
   - Otherwise run the same command without `--dry-run`.

9. **Report** the pillar, the 5 items with source links, the post text, and
   the published URL.
