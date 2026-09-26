"""Add a published post to data/history.json.

    python3 scripts/record_post.py output/2026-09-28/content.json "<pillar>" "<post url>"
    python3 scripts/record_post.py output/2026-09-30/infographic.json "<pillar>" "<post url>"
"""
import json
import sys
from pathlib import Path

from common import DATA


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    content_path, pillar, url = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    content = json.loads(content_path.read_text())
    path = DATA / "history.json"
    history = json.loads(path.read_text())
    history.append({
        "date": content_path.parent.name,
        "pillar": pillar,
        "title": content["title"],
        "topics": [s["headline"] for s in content.get("stories", [])]
                  or [c["heading"] for r in content.get("rows", []) for c in r.get("cards", [])],
        "url": url,
    })
    path.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    print(f"Recorded {content_path.parent.name}: {content['title']}")


if __name__ == "__main__":
    main()
