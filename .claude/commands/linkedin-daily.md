---
description: Unattended daily run – plan today's post from the weekday schedule, create it, publish it and record it
allowed-tools: WebSearch, WebFetch, Bash(python3 scripts/*), Bash(mkdir *), Bash(git *), Read, Write
---

This runs on a schedule with nobody watching. Never ask questions; decide
using CLAUDE.md, and when in doubt, skip the day rather than post something weak.

1. **Plan.** Run `python3 scripts/plan_today.py`.
   - Exit code 2 or 3 → stop and report "No post today" with the reason.
   - Otherwise note the pillar, the `why_label` and the recent topics.
     Don't repeat any of those topics.

2. **Create the post.** Follow steps 2–7 of `.claude/commands/linkedin-post.md`
   for today's pillar, using the `why_label` from the plan. For pillars that
   aren't news (explainers, costly mistakes, checklists), the 5 items are 5
   points on one topic; still verify every fact, date and amount. Tags can be
   short labels (e.g. "MISTAKE 1", "STEP 1", "PVT LTD") instead of due dates.

3. **Quality gate. Skip the day instead of posting if any of these hold:**
   - fewer than 5 items you could verify from reliable sources this run
   - any date, amount or form name you couldn't confirm
   - the post breaks a voice or accuracy rule in CLAUDE.md
   - a slide has cut-off text you couldn't fix

4. **Publish.** `python3 scripts/linkedin_post.py --text output/<date>/post.txt --pdf output/<date>/carousel.pdf --title "<carousel title>"`.
   On a 401 error, stop and report that the LinkedIn token must be refreshed.

5. **Record.** `python3 scripts/record_post.py output/<date>/content.json "<pillar>" "<published url>"`,
   then commit and push the history so tomorrow's run sees it:
   `git add data/history.json data/state.json && git commit -m "Record LinkedIn post for <date>" && git push`
   (push to the current branch; retry up to 4 times on network errors).

6. **Report** in 3–5 lines: pillar, title, published URL, or why the day was skipped.
