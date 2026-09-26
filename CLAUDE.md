# LinkedIn Autopilot

This repo turns one prompt into a published LinkedIn post: research the week's
top AI/tech news, write the post, build a 7-slide carousel PDF, and publish it
through the LinkedIn API. The whole workflow is `/linkedin-post`
(`.claude/commands/linkedin-post.md`).

## Layout

- `scripts/linkedin_auth.py` – one-time OAuth login; saves token + person URN to `.env`
- `scripts/next_hook.py` – rotating opening line from `data/hooks.json`
- `scripts/build_carousel.py` – `content.json` → `slide-N.png` + `carousel.pdf`
- `scripts/linkedin_post.py` – publishes text / PDF carousel / image (`--dry-run` supported)
- `output/<YYYY-MM-DD>/` – each run's `post.txt`, `content.json`, slides, PDF (git-ignored)

## Author profile

Edit this so posts sound like you.

- **Name (carousel footer):** Vaidam Consultancy LLP
- **Audience:** founders, business owners, professionals who want to keep up with AI
- **Angle:** what each story means for a business, not just what happened

## Voice rules

- Plain, confident, conversational. Short sentences. No hype words
  ("game-changer", "revolutionary", "mind-blowing"), no "In today's fast-paced world".
- One idea per line; lots of white space.
- Facts must come from sources you actually read this run. Never invent
  numbers, quotes, or dates.
- End with a real question, then 3–5 hashtags.

## Rules

- Never commit `.env` or anything in `output/`.
- Don't publish if research turned up fewer than 5 credible stories — say so instead.
- LinkedIn tokens last ~60 days. On a 401, tell the user to rerun
  `python3 scripts/linkedin_auth.py`.
