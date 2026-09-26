"""Print the next opening hook line, rotating through data/hooks.json.

    python scripts/next_hook.py          # advance and print
    python scripts/next_hook.py --peek   # print without advancing
"""
import json
import sys

from common import DATA


def main():
    hooks = json.loads((DATA / "hooks.json").read_text())
    state_path = DATA / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"hook_index": -1}
    index = (state.get("hook_index", -1) + 1) % len(hooks)
    if "--peek" not in sys.argv:
        state["hook_index"] = index
        state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(hooks[index])


if __name__ == "__main__":
    main()
