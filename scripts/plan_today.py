"""Print today's posting plan for the daily run.

    python3 scripts/plan_today.py

Prints today's date (IST), the content pillar from data/schedule.json and the
topics posted recently (to avoid repeating them). Exit codes:
  0  post today
  2  no post scheduled today (weekend / day not in schedule)
  3  already posted today
"""
import json
import sys
from datetime import datetime, timedelta, timezone

from common import DATA


def main():
    schedule = json.loads((DATA / "schedule.json").read_text())
    history = json.loads((DATA / "history.json").read_text())
    now = datetime.now(timezone(timedelta(hours=schedule["timezone_offset_hours"])))
    today = now.date().isoformat()
    day = now.strftime("%A")

    print(f"Date: {today} ({day})")
    if any(h["date"] == today for h in history):
        print("Already posted today. Stop.")
        sys.exit(3)
    plan = schedule["weekdays"].get(day)
    if not plan:
        print("No post scheduled today. Stop.")
        sys.exit(2)

    print(f"Pillar: {plan['pillar']}")
    print(f"why_label: {plan['why_label']}")
    cutoff = (now.date() - timedelta(days=schedule["avoid_repeat_days"])).isoformat()
    recent = [h for h in history if h["date"] >= cutoff]
    if recent:
        print(f"Topics posted in the last {schedule['avoid_repeat_days']} days (don't repeat):")
        for h in recent:
            print(f"- {h['date']} [{h['pillar']}] {h['title']}: {', '.join(h.get('topics', []))}")
    else:
        print("No recent posts.")


if __name__ == "__main__":
    main()
