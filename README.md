# LinkedIn Autopilot (Claude Code)

One prompt → researched post + 7-slide carousel → published on LinkedIn.

A rebuild of the workflow from
[How I Fully Automated My LinkedIn Posts! (Claude Code)](https://youtu.be/1q0RmehD8SU):
The video's pipeline was built for AI news. This version is tuned for
Vaidam Consultancy LLP: Claude researches Indian business-compliance news and
upcoming deadlines (MCA/ROC, income tax, GST, LLP, FEMA), writes a post in
the voice set out in `CLAUDE.md`, builds a 7-slide carousel, and posts it
straight to your LinkedIn profile.

```
/linkedin-post
   │
   ├─ WebSearch ─────────────► 5 deadlines / rule changes
   ├─ next_hook.py ──────────► rotating first line
   ├─ post.txt + content.json
   ├─ build_carousel.py ─────► slide-1..7.png + carousel.pdf
   └─ linkedin_post.py ──────► LinkedIn Posts API (document post)
```

## Setup (one time)

1. **Install**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```
2. **Create a LinkedIn app** at <https://www.linkedin.com/developers/apps>
   - Link it to a LinkedIn Company Page (any page you admin; required by LinkedIn).
   - **Products** tab → add **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn**.
   - **Auth** tab → add redirect URL `http://localhost:8765/callback`.
   - Copy the Client ID and Client Secret into `.env`.
3. **Log in**
   ```bash
   python3 scripts/linkedin_auth.py
   ```
   Approve in the browser. Your access token and person URN are written to `.env`.
   The token lasts about 60 days; run this again when it expires.
4. **Make it yours:** edit the *Author profile* and *Voice rules* in `CLAUDE.md`,
   and the opening lines in `data/hooks.json`.

## Use

In Claude Code, from this folder:

```
/linkedin-post --dry-run          # everything except publishing
/linkedin-post                    # research, build and publish
/linkedin-post GST                # focus on a topic or content pillar
```

Each run leaves its files in `output/<date>/`.

### Scripts on their own

```bash
python3 scripts/build_carousel.py examples/content.json
python3 scripts/linkedin_post.py --text examples/post.txt --pdf examples/carousel.pdf --title "This Week in AI" --dry-run
```

## Run it on a schedule

Use a Claude Code Routine / cron to run `claude -p "/linkedin-post"` every
Monday morning, with `.env` available to the job.
