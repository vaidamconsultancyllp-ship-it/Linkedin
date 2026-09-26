# Handoff – where we left off (26 Sep 2026)

Notes from the Claude Code session that built this repo, so work can resume
on another machine. Open Claude Code in this folder and say:
**"Read HANDOFF.md and continue."**

## What was done

1. **Rebuilt the workflow from the video**
   [How I Fully Automated My LinkedIn Posts! (Claude Code)](https://youtu.be/1q0RmehD8SU)
   (the video itself couldn't be watched from the cloud session; rebuilt from
   its description): research → post with rotating hook → 7-slide carousel
   PDF → publish through the LinkedIn API. See `README.md`.
2. **Retargeted it to Vaidam Consultancy LLP.** The first test post was AI
   news, which doesn't fit the business. `CLAUDE.md` now holds the
   audience (founders, SMEs, startups, NRIs in India), content pillars
   (deadlines, rule changes, explainers, costly mistakes, checklists), voice
   and accuracy rules. Website: vaidamconsultancy.in.
3. **First post drafted (not yet published):** "Compliance Deadlines You
   Can't Miss" – OPC AOC-4 (27 Sep), Tax Audit Report (30 Sep), ADT-1
   (15 Oct), AOC-4 (29 Oct) / LLP Form 8 (30 Oct), DIR-3 KYC now every 3
   years. Regenerate with `/linkedin-post --dry-run` – dates will have moved on.

## Blocked on (user actions)

- [x] **GitHub:** connected; code pushed to branch `claude/video-analysis-dor-m3-1kls85`.
- [ ] **LinkedIn app + login:** create the app (README → Setup), then run
      `python3 scripts/linkedin_auth.py` on the laptop. Token lasts ~60 days.
- [ ] **For cloud daily runs**, in the cloud environment settings (title-bar
      environment menu → Edit):
  - env vars `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`, `LINKEDIN_VERSION=202509`
    (never paste tokens into chat)
  - network access: allow `api.linkedin.com` plus mca.gov.in, incometax.gov.in,
    gst.gov.in, cbic-gst.gov.in, rbi.org.in (or full access)
  - setup script: `pip install -r requirements.txt`
- [ ] **Confirm defaults:** 9:00 AM IST, Mon–Fri, fully automatic
      (change days in `data/schedule.json`).

## Open questions for the user

- Is vaidamconsultancy.com also theirs? (Early research used it.)
- Contact email / phone to show in posts?
- Sign explainer posts as "CS Harshita Jhawar, Vaidam Consultancy"?
- Share a few past LinkedIn posts so the tone can match.

## Built for daily posting

- `data/schedule.json`: Mon deadlines · Tue rule change · Wed explainer ·
  Thu costly mistake · Fri founder checklist (times in IST, Mon–Fri).
- `scripts/plan_today.py` + `data/history.json`: no weekend posts, never
  twice a day, no topic repeated within 60 days.
- `/linkedin-daily`: unattended run with a quality gate (skips the day
  rather than posting unverified facts), records and pushes the history.
- `linkedin_post.py` stops with a clear message when the token expires (401).

## Still to do (Claude, after the user's setup steps)

1. Test once: `/linkedin-daily` by hand, check the live post.
2. Create the daily Routine (default 8:5x AM IST Mon–Fri) running `/linkedin-daily`.
3. Schedule a reminder every ~55 days to refresh the LinkedIn token.

## Costs

All free except Claude usage: daily runs count against the existing Claude
plan's limits. LinkedIn API, GitHub and the scripts cost nothing.
