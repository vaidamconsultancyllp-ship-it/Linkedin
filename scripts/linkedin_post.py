"""Publish to LinkedIn via the Posts API.

    python scripts/linkedin_post.py --text post.txt                         # text only
    python scripts/linkedin_post.py --text post.txt --pdf carousel.pdf \
        --title "This Week in AI"                                           # carousel
    python scripts/linkedin_post.py --text post.txt --image slide-1.png     # single image
    python scripts/linkedin_post.py ... --dry-run                           # print payload only

Needs LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN in .env
(run scripts/linkedin_auth.py once).
"""
import argparse
import json
import re
from pathlib import Path

import requests

from common import env

API = "https://api.linkedin.com/rest"


def headers(token, version, content_type="application/json"):
    return {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": version,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": content_type,
    }


def upload(kind, file_path, owner, token, version):
    """Upload a document or image and return its URN (urn:li:document / urn:li:image)."""
    init = requests.post(
        f"{API}/{kind}s?action=initializeUpload",
        headers=headers(token, version),
        json={"initializeUploadRequest": {"owner": owner}},
        timeout=30,
    )
    init.raise_for_status()
    value = init.json()["value"]
    put = requests.put(
        value["uploadUrl"],
        headers={"Authorization": f"Bearer {token}"},
        data=Path(file_path).read_bytes(),
        timeout=120,
    )
    put.raise_for_status()
    return value[kind]


def escape_commentary(text):
    """Escape LinkedIn 'little text' markup; turn #tags into real hashtags."""
    for ch in "\\|{}@[]()<>#*_~":
        text = text.replace(ch, "\\" + ch)
    return re.sub(r"\\#(\w+)", r"{hashtag|\\#|\1}", text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True, help="file containing the post text")
    p.add_argument("--pdf", help="carousel PDF to attach as a document post")
    p.add_argument("--image", help="single image to attach")
    p.add_argument("--title", default="Carousel", help="document title shown on LinkedIn")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    text = Path(args.text).read_text().strip()
    post = {
        "author": env("LINKEDIN_PERSON_URN", "urn:li:person:DRY_RUN"),
        "commentary": escape_commentary(text),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    if args.dry_run:
        if args.pdf or args.image:
            post["content"] = {"media": {"title": args.title, "id": "<uploaded urn>"}}
        print(json.dumps(post, indent=2, ensure_ascii=False))
        return

    token = env("LINKEDIN_ACCESS_TOKEN", required=True)
    env("LINKEDIN_PERSON_URN", required=True)
    version = env("LINKEDIN_VERSION", "202509")

    if args.pdf:
        urn = upload("document", args.pdf, post["author"], token, version)
        post["content"] = {"media": {"title": args.title, "id": urn}}
    elif args.image:
        urn = upload("image", args.image, post["author"], token, version)
        post["content"] = {"media": {"title": args.title, "id": urn}}

    r = requests.post(f"{API}/posts", headers=headers(token, version), json=post, timeout=30)
    if r.status_code == 401:
        raise SystemExit("LinkedIn token expired or invalid (401). "
                         "Rerun: python3 scripts/linkedin_auth.py and update LINKEDIN_ACCESS_TOKEN.")
    if r.status_code >= 400:
        raise SystemExit(f"LinkedIn API error {r.status_code}: {r.text}")
    post_urn = r.headers.get("x-restli-id", "")
    print(f"Published: https://www.linkedin.com/feed/update/{post_urn}/")


if __name__ == "__main__":
    main()
