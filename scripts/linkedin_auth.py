"""One-time LinkedIn OAuth 2.0 login.

Opens the LinkedIn consent page, catches the redirect on localhost, exchanges
the code for an access token (valid ~60 days) and stores the token plus your
person URN in .env.

    python scripts/linkedin_auth.py
"""
import secrets
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

from common import env, set_env

SCOPES = "openid profile email w_member_social"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"


def main():
    client_id = env("LINKEDIN_CLIENT_ID", required=True)
    client_secret = env("LINKEDIN_CLIENT_SECRET", required=True)
    redirect_uri = env("LINKEDIN_REDIRECT_URI", "http://localhost:8765/callback")
    state = secrets.token_urlsafe(16)

    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": SCOPES,
    })

    result = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result["code"] = query.get("code", [None])[0]
            result["state"] = query.get("state", [None])[0]
            result["error"] = query.get("error_description", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>LinkedIn connected. You can close this tab.</h2>")

        def log_message(self, *args):
            pass

    parsed = urllib.parse.urlparse(redirect_uri)
    server = HTTPServer((parsed.hostname, parsed.port or 80), Handler)
    print("Open this URL if your browser doesn't launch:\n" + url)
    webbrowser.open(url)
    server.handle_request()

    if result.get("error") or not result.get("code"):
        raise SystemExit(f"Authorization failed: {result.get('error')}")
    if result["state"] != state:
        raise SystemExit("State mismatch, aborting.")

    token = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": result["code"],
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }, timeout=30)
    token.raise_for_status()
    access_token = token.json()["access_token"]

    me = requests.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    me.raise_for_status()
    person_urn = f"urn:li:person:{me.json()['sub']}"

    set_env("LINKEDIN_ACCESS_TOKEN", access_token)
    set_env("LINKEDIN_PERSON_URN", person_urn)
    print(f"Saved token for {me.json().get('name')} ({person_urn}) to .env")


if __name__ == "__main__":
    main()
