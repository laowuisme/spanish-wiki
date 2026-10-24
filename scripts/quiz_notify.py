#!/usr/bin/env python3
"""
quiz_notify.py — Spanish wiki quiz notification agent
Fired by launchd on Tue/Thu/Sat at 9pm SGT.
Reads wiki files, counts items that need review, sends a macOS notification.
Does NOT modify any wiki files.
"""

import re
import subprocess
from datetime import date
from pathlib import Path

WIKI_ROOT = Path("/Users/laowuisme/Documents/MyWork/spanish-wiki")
PERFORMANCE_FILE = WIKI_ROOT / "wiki/quiz/performance.md"
CURRICULUM_FILE = WIKI_ROOT / "wiki/curriculum/curriculum-map.md"
VOCAB_DIR = WIKI_ROOT / "wiki/vocab"
TOPICS_DIR = WIKI_ROOT / "wiki/topics"
LOG_FILE = WIKI_ROOT / "wiki/quiz/notify.log"

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


def notify_macos(title: str, message: str) -> None:
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False)


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{TODAY} {msg}\n")


def main() -> None:
    perf = parse_performance()
    overdue = parse_overdue()
    new_items = get_new_items(perf)
    high_miss = get_high_miss(perf)

    n = len(new_items) + len(overdue) + len(high_miss)

    notify_macos(
        "🇪🇸 Spanish quiz ready",
        f"{n} items prioritised ({len(new_items)} new, {len(overdue)} overdue, "
        f"{len(high_miss)} high-miss). Open Claude Code → quiz me",
    )

    _log(f"Notification sent — {n} items ({len(new_items)} new, {len(overdue)} overdue, {len(high_miss)} high-miss)")


if __name__ == "__main__":
    main()
