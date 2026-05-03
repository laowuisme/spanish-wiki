#!/usr/bin/env python3
"""
quiz_notify.py — Spanish wiki quiz notification agent
Fired by launchd on Tue/Thu/Sat at 9pm SGT.
Reads wiki files, computes item priority, sends macOS notification + Gmail draft.
Does NOT modify any wiki files.
"""

import re
import subprocess
import base64
from datetime import date
from email.mime.text import MIMEText
from pathlib import Path

WIKI_ROOT = Path("/Users/laowuisme/Documents/MyWork/spanish-wiki")
PERFORMANCE_FILE = WIKI_ROOT / "wiki/quiz/performance.md"
CURRICULUM_FILE = WIKI_ROOT / "wiki/curriculum/curriculum-map.md"
VOCAB_DIR = WIKI_ROOT / "wiki/vocab"
TOPICS_DIR = WIKI_ROOT / "wiki/topics"
ERRORS_DIR = WIKI_ROOT / "wiki/errors"
LOG_FILE = WIKI_ROOT / "wiki/quiz/notify.log"

# Reuse Gmail credentials from the existing Spanish learning project
CREDS_FILE = Path("/Users/laowuisme/Documents/MyWork/spanish-learning/credentials.json")
TOKEN_FILE = Path("/Users/laowuisme/Documents/MyWork/spanish-learning/token.json")
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
RECIPIENT = "laowuisme@gmail.com"

TODAY = date.today()


def parse_performance() -> dict:
    """Return {slug: {type, attempts, correct, streak, last_quizzed, last_result}}."""
    perf = {}
    if not PERFORMANCE_FILE.exists():
        return perf
    for line in PERFORMANCE_FILE.read_text().splitlines():
        if not line.startswith("| ") or "Attempts" in line or "---" in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 7:
            continue
        slug, type_, attempts, correct, streak, last_quizzed, last_result = parts
        try:
            perf[slug] = {
                "type": type_,
                "attempts": int(attempts),
                "correct": int(correct),
                "streak": int(streak),
                "last_quizzed": last_quizzed,
                "last_result": last_result,
            }
        except ValueError:
            pass
    return perf


def parse_overdue() -> list[dict]:
    """Return items from curriculum-map with Days Since > 14 at encountered/understood."""
    overdue = []
    if not CURRICULUM_FILE.exists():
        return overdue
    for line in CURRICULUM_FILE.read_text().splitlines():
        if "| [[" not in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 6:
            continue
        slug_raw, _, stage, _, days_since, _ = parts[:6]
        slug = slug_raw.replace("[[", "").replace("]]", "").strip()
        if stage not in ("encountered", "understood"):
            continue
        try:
            days = int(days_since)
            if days > 14:
                overdue.append({"slug": slug, "days": days})
        except ValueError:
            pass
    return overdue


def get_new_items(perf: dict) -> list[dict]:
    """Vocab/topic pages updated within 7 days that have never been quizzed."""
    new_items = []
    for dir_ in (VOCAB_DIR, TOPICS_DIR):
        if not dir_.exists():
            continue
        for f in dir_.glob("*.md"):
            slug = f.stem
            if slug in perf:
                continue
            m = re.search(r"last_updated:\s*(\d{4}-\d{2}-\d{2})", f.read_text())
            if m:
                days_ago = (TODAY - date.fromisoformat(m.group(1))).days
                if days_ago <= 7:
                    new_items.append({"slug": slug, "days_ago": days_ago})
    return new_items


def get_high_miss(perf: dict) -> list[dict]:
    """Items with >= 2 attempts and < 50% correct."""
    return [
        {"slug": slug}
        for slug, v in perf.items()
        if v["attempts"] >= 2 and v["correct"] / v["attempts"] < 0.5
    ]


def top_items(perf: dict, overdue: list, new_items: list, high_miss: list) -> list[tuple]:
    """Return top 3 (slug, reason) by priority weight."""
    error_slugs = {f.stem for f in ERRORS_DIR.glob("*.md")} if ERRORS_DIR.exists() else set()
    overdue_slugs = {i["slug"] for i in overdue}
    new_slugs = {i["slug"] for i in new_items}
    high_miss_slugs = {i["slug"] for i in high_miss}

    candidates = set(perf.keys()) | new_slugs | overdue_slugs
    scored = []
    for slug in candidates:
        w = 1.0
        v = perf.get(slug)
        if slug in error_slugs:
            w *= 3
        if v and v["last_result"] == "incorrect":
            w *= 3
        if slug in new_slugs:
            w *= 2
        if slug in overdue_slugs:
            w *= 2
        if v and v["streak"] >= 3:
            w *= 0.5

        if slug in error_slugs:
            reason = "error pattern"
        elif slug in high_miss_slugs:
            reason = "high-miss"
        elif slug in new_slugs:
            reason = "new this week"
        elif slug in overdue_slugs:
            days = next((i["days"] for i in overdue if i["slug"] == slug), "?")
            reason = f"{days}d overdue"
        elif v and v["last_result"] == "incorrect":
            reason = "missed last quiz"
        else:
            reason = "due for review"
        scored.append((slug, w, reason))

    scored.sort(key=lambda x: -x[1])
    return [(s, r) for s, _, r in scored[:3]]


def notify_macos(title: str, message: str) -> None:
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False)


def create_gmail_draft(subject: str, body: str) -> None:
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = None
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), GMAIL_SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                _log("Gmail auth failed — token missing or expired. Run auth once interactively.")
                return

        service = build("gmail", "v1", credentials=creds)
        msg = MIMEText(body)
        msg["to"] = RECIPIENT
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    except Exception as e:
        _log(f"Gmail error: {e}")


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{TODAY} {msg}\n")


def main() -> None:
    perf = parse_performance()
    overdue = parse_overdue()
    new_items = get_new_items(perf)
    high_miss = get_high_miss(perf)
    top = top_items(perf, overdue, new_items, high_miss)

    n = len(new_items) + len(overdue) + len(high_miss)
    day_name = TODAY.strftime("%A")

    notify_macos(
        "🇪🇸 Spanish quiz ready",
        f"{n} items prioritised ({len(new_items)} new, {len(overdue)} overdue, "
        f"{len(high_miss)} high-miss). Open Claude Code → quiz me",
    )

    top_str = ", ".join(f"{s} ({r})" for s, r in top) if top else "none yet"
    create_gmail_draft(
        subject=f"🇪🇸 Spanish Quiz — {day_name} 9pm",
        body=(
            f"{n} items queued for tonight's quiz.\n"
            f"Top picks: {top_str}\n\n"
            f"Open Claude Code and type: quiz me"
        ),
    )
    _log(f"Notification sent — {n} items ({len(new_items)} new, {len(overdue)} overdue, {len(high_miss)} high-miss)")


if __name__ == "__main__":
    main()
