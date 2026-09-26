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
- [x] **LinkedIn app + login:** done 26 Sep 2026 (token lasts ~60 days).
- [x] **For cloud daily runs**, in the cloud environment settings (title-bar
      environment menu → Edit):
  - env vars `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`, `LINKEDIN_VERSION=202509`
    (never paste tokens into chat)
  - network access: allow `api.linkedin.com` plus mca.gov.in, incometax.gov.in,
    gst.gov.in, cbic-gst.gov.in, rbi.org.in (or full access)
  - setup script: `pip install -r requirements.txt`
- [x] **Schedule:** daily at 10 AM IST, fully automatic.

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

## Scheduled (Claude Code Routines)

- **Vaidam LinkedIn daily post** (`trig_01YAyqhVeMaVwqwkR2DWs6GW`): every day,
  starts 9:51 AM IST so the post is live around 10 AM; fresh cloud session each
  time, runs `/linkedin-daily`, push + email summary. First real test post went
  out 26 Sep 2026. Scheduled runs can't push `data/history.json` (no GitHub
  write access) – the fixed topic plan in `data/plan.json` prevents repeats.
- **Refresh LinkedIn token reminder** (`trig_01JNUxpSjW1N8FaLXRA3cUHk`):
  20 Nov 2026 (token issued 26 Sep, expires ~25 Nov).
- LinkedIn app "Vaidam Post Autopilot" created; login done on the laptop.

## Content plan & design (26 Sep 2026)

- `data/plan.json`: one topic per day, 27 Sep – 25 Nov 2026; exported to
  `plan/content-plan-2026-09-27-to-2026-11-25.xlsx/.pdf` (`scripts/export_plan.py`).
- Weekly themes: Mon deadlines · Tue rule changes · Wed explainers (infographic) ·
  Thu costly mistakes · Fri checklists (infographic) · Sat founder FAQ · Sun myth vs fact.
- Carousels and infographics use the logo colours (navy, teal, blue, gold, orange).
- Next plan: extend `data/plan.json` before 25 Nov and rerun the export.

## Costs

All free except Claude usage: daily runs count against the existing Claude
plan's limits. LinkedIn API, GitHub and the scripts cost nothing.
