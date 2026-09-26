"""Shared helpers: paths, .env loading and updating."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

try:
    from dotenv import load_dotenv

    load_dotenv(ENV_PATH)
except ImportError:  # python-dotenv is optional
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def env(name, default=None, required=False):
    value = os.environ.get(name) or default
    if required and not value:
        raise SystemExit(f"Missing {name} in .env (see .env.example)")
    return value


def set_env(name, value):
    """Write or replace NAME=value in .env."""
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    for i, line in enumerate(lines):
        if line.startswith(f"{name}="):
            lines[i] = f"{name}={value}"
            break
    else:
        lines.append(f"{name}={value}")
    ENV_PATH.write_text("\n".join(lines) + "\n")
    os.environ[name] = value
