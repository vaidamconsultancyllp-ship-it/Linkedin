"""Print today's posting plan for the daily run.

    python3 scripts/plan_today.py

Uses the topic planned for today in data/plan.json; if today isn't in the
plan, falls back to the weekday pillar in data/schedule.json. Also lists
recently posted topics so they aren't repeated. Exit codes:
  0  post today
  2  no post scheduled today
  3  already posted today
"""
import json
import sys
from datetime import datetime, timedelta, timezone

from common import DATA


def main():
    schedule = json.loads((DATA / "schedule.json").read_text())
    history = json.loads((DATA / "history.json").read_text())
    plan = {p["date"]: p for p in json.loads((DATA / "plan.json").read_text())}
    now = datetime.now(timezone(timedelta(hours=schedule["timezone_offset_hours"])))
    today = now.date().isoformat()
    day = now.strftime("%A")

    print(f"Date: {today} ({day})")
    if any(h["date"] == today for h in history):
        print("Already posted today. Stop.")
        sys.exit(3)
    weekday = schedule["weekdays"].get(day)
    if not weekday:
        print("No post scheduled today. Stop.")
        sys.exit(2)

    print(f"Pillar: {weekday['pillar']}")
    print(f"why_label: {weekday['why_label']}")
    print(f"Format: {plan.get(today, weekday).get('format', 'carousel')}")
    if today in plan:
        print(f"Planned topic: {plan[today]['topic']}")
        print(f"Key points: {plan[today]['key_points']}")
    else:
        print("No planned topic for today: choose one for this pillar.")
    cutoff = (now.date() - timedelta(days=schedule["avoid_repeat_days"])).isoformat()
    recent = [h for h in history if h["date"] >= cutoff]
    if recent:
        print(f"Topics posted in the last {schedule['avoid_repeat_days']} days (don't repeat):")
        for h in recent:
            print(f"- {h['date']} [{h['pillar']}] {h['title']}: {', '.join(h.get('topics', []))}")


if __name__ == "__main__":
    main()
