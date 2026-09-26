# LinkedIn Autopilot – Vaidam Consultancy LLP

This repo turns one prompt into a published LinkedIn post: research this
week's Indian business-compliance news and upcoming deadlines, write the post,
build a 7-slide carousel PDF, and publish it through the LinkedIn API. The
whole workflow is `/linkedin-post` (`.claude/commands/linkedin-post.md`).

## Layout

- `scripts/linkedin_auth.py` – one-time OAuth login; saves token + person URN to `.env`
- `scripts/next_hook.py` – rotating opening line from `data/hooks.json`
- `scripts/build_carousel.py` – `content.json` → `slide-N.png` + `carousel.pdf`
- `scripts/linkedin_post.py` – publishes text / PDF carousel / image (`--dry-run` supported)
- `output/<YYYY-MM-DD>/` – each run's `post.txt`, `content.json`, slides, PDF (git-ignored)

## Who we are

- **Name (carousel footer):** Vaidam Consultancy LLP
- **What we do:** company, LLP and startup registration; GST registration and
  returns; ROC/MCA annual filings; ITR and tax compliance; MSME/Udyam; FEMA
  and NRI/foreign company setup in India; legal drafting and investment agreements.
- **Website / contact:** vaidamconsultancy.com · contact@vaidamconsultancy.com
- **Audience:** founders, startups, SMEs, small-business owners, NRIs and
  foreign companies doing business in India.
- **Goal of every post:** be the account founders save because it keeps them
  compliant, and make "ask Vaidam" the obvious next step. Teach first; sell softly.

## Content pillars (rotate; don't repeat the same pillar two weeks running)

1. **Deadline alerts** – filings due in the next 30 days (MCA/ROC, income tax,
   GST, LLP), with the date, who it applies to, and the late fee or penalty.
2. **Rule changes** – new MCA, CBDT, GST Council, RBI/FEMA, SEBI or
   Startup India notifications, in plain English: what changed, who is
   affected, what to do.
3. **Explainers** – Pvt Ltd vs LLP vs OPC, GST composition vs regular, DPIIT
   recognition benefits, how an NRI sets up a company, etc.
4. **Costly mistakes** – common compliance errors and what they cost, with the fix.
5. **Founder checklists** – "before you raise money", "first 90 days after
   incorporation", "year-end compliance".

AI/tech news only when it directly changes compliance or taxes for Indian
businesses (e.g. a new e-invoicing or MCA portal rule).

## Voice rules

- Simple, clear English a first-time founder understands. Explain every
  acronym once (e.g. "AOC-4 (annual financial statements)").
- Helpful expert, not a salesman. Calm and specific; no fear-mongering, no
  hype words, no "In today's fast-paced world".
- Always give the concrete detail: exact due date, who it applies to, the
  rupee amount of the fee/penalty, the form name.
- One idea per line, lots of white space, emojis only as list markers
  (📌 ✅ ⚠️ 🗓️) – never more than one per line.
- Every item ends with an action ("File by…", "Check if…", "Ask your CA to…").
- Close with a soft call to action: a question, or "Comment 'CHECKLIST'" /
  "DM us if you need help filing". Never a hard sell or price list.
- 3–5 hashtags, e.g. #Compliance #StartupIndia #GST #IncomeTax #ROC #MCA #SME #LLP.
- Add "Dates as per current notifications; check for any extension." when
  the post is about deadlines.

## Accuracy rules

- Facts, dates and amounts must come from official sources (mca.gov.in,
  incometax.gov.in, cbic-gst.gov.in, gst.gov.in, rbi.org.in, CBDT/CBIC
  notifications) or reliable professional sites (TaxGuru, CAclubindia,
  StudyCafe) checked this run. Never guess a date or a penalty.
- If an extension is being demanded but not notified, say "no extension
  notified yet" – don't predict one.
- Don't quote section numbers unless you've verified which Act applies
  (the Income-tax Act, 2025 replaced the 1961 Act from 1 April 2026; FY
  2025-26 filings still follow the 1961 Act).

## Rules

- Never commit `.env` or anything in `output/`.
- Don't publish if research turned up fewer than 5 solid items — say so instead.
- LinkedIn tokens last ~60 days. On a 401, tell the user to rerun
  `python3 scripts/linkedin_auth.py`.
