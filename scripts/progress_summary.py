#!/usr/bin/env python3
"""
progress_summary.py — Spanish wiki bi-weekly progress summary
Fired by launchd every Sunday. Self-gates: exits silently if < 14 days since last summary.
Reads wiki files, computes progress metrics, sends Gmail draft.
Only writes to wiki/quiz/last-summary.md and wiki/quiz/notify.log.
"""

import re
import base64
from datetime import date, timedelta
from email.mime.text import MIMEText
from pathlib import Path

WIKI_ROOT = Path("/Users/laowuisme/Documents/MyWork/spanish-wiki")
PERFORMANCE_FILE = WIKI_ROOT / "wiki/quiz/performance.md"
CURRICULUM_FILE = WIKI_ROOT / "wiki/curriculum/curriculum-map.md"
LOG_FILE = WIKI_ROOT / "wiki/log.md"
LAST_SUMMARY_FILE = WIKI_ROOT / "wiki/quiz/last-summary.md"

TOKEN_FILE = Path("/Users/laowuisme/Documents/MyWork/spanish-learning/token.json")
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
RECIPIENT = "laowuisme@gmail.com"

TODAY = date.today()


def get_last_summary_date() -> date:
    if LAST_SUMMARY_FILE.exists():
        m = re.search(r"(\d{4}-\d{2}-\d{2})", LAST_SUMMARY_FILE.read_text())
        if m:
            return date.fromisoformat(m.group(1))
    return TODAY - timedelta(days=14)


def update_last_summary_date() -> None:
    LAST_SUMMARY_FILE.write_text(f"last_summary: {TODAY}\n")


def parse_log_since(since: date) -> dict:
    result = {
        "vocab_created": 0,
        "topics_created": 0,
        "errors_created": 0,
        "quiz_scores": [],
        "stage_promotions": [],
    }
    if not LOG_FILE.exists():
        return result

    for section in re.split(r"\n(?=## \[)", LOG_FILE.read_text()):
        m = re.match(r"## \[(\d{4}-\d{2}-\d{2})\] (ingest|quiz)", section)
        if not m:
            continue
        if date.fromisoformat(m.group(1)) <= since:
            continue

        if m.group(2) == "ingest":
            for pattern, key in [
                (r"(\d+) vocab atoms? created", "vocab_created"),
                (r"(\d+) topic hubs? created", "topics_created"),
                (r"(\d+) error pages? created", "errors_created"),
            ]:
                hit = re.search(pattern, section)
                if hit:
                    result[key] += int(hit.group(1))

        elif m.group(2) == "quiz":
            score_m = re.search(r"Score: (\d+)/10", section)
            if score_m:
                result["quiz_scores"].append(int(score_m.group(1)))
            promo_m = re.search(r"(\d+) stage promotions?: (.+)", section)
            if promo_m and int(promo_m.group(1)) > 0:
                result["stage_promotions"].extend(
                    [p.strip() for p in promo_m.group(2).split(",")]
                )

    return result


def get_high_miss_items() -> list[dict]:
    items = []
    if not PERFORMANCE_FILE.exists():
        return items
    for line in PERFORMANCE_FILE.read_text().splitlines():
        if not line.startswith("| ") or "Attempts" in line or "---" in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 7:
            continue
        slug, _, attempts, correct = parts[0], parts[1], parts[2], parts[3]
        try:
            att, cor = int(attempts), int(correct)
            if att >= 2 and cor / att < 0.5:
                items.append({"slug": slug, "correct": cor, "attempts": att})
        except ValueError:
            pass
    return items


def get_debt_count() -> int:
    if not CURRICULUM_FILE.exists():
        return 0
    return sum(1 for line in CURRICULUM_FILE.read_text().splitlines() if "YES" in line)


def get_stage_breakdown() -> dict:
    counts = {"encountered": 0, "understood": 0, "practiced": 0, "automated": 0}
    if not CURRICULUM_FILE.exists():
        return counts
    for line in CURRICULUM_FILE.read_text().splitlines():
        for stage in counts:
            if f"| {stage}" in line:
                counts[stage] += 1
                break
    return counts


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
                _log("Gmail auth failed — token missing or expired.")
                return

        service = build("gmail", "v1", credentials=creds)
        msg = MIMEText(body)
        msg["to"] = RECIPIENT
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().drafts().create(
            userId="me", body={"message": {"raw": raw}}
        ).execute()
    except Exception as e:
        _log(f"Gmail error: {e}")


def _log(msg: str) -> None:
    log_path = WIKI_ROOT / "wiki/quiz/notify.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"{TODAY} [summary] {msg}\n")


def main() -> None:
    last_summary = get_last_summary_date()
    if (TODAY - last_summary).days < 14:
        return

    log_data = parse_log_since(last_summary)
    high_miss = get_high_miss_items()
    debt_count = get_debt_count()
    stages = get_stage_breakdown()

    scores = log_data["quiz_scores"]
    if scores:
        score_line = (
            f"{len(scores)} session(s) — avg {sum(scores)/len(scores):.1f}/10"
            f"  (best {max(scores)}/10, worst {min(scores)}/10)"
        )
    else:
        score_line = "No quizzes taken this period"

    miss_lines = (
        "\n".join(f"  • {i['slug']} — {i['correct']}/{i['attempts']} correct" for i in high_miss)
        if high_miss
        else "  None"
    )

    promo_line = ", ".join(log_data["stage_promotions"]) if log_data["stage_promotions"] else "None"

    period = f"{last_summary} → {TODAY}"
    body = f"""🇪🇸 Spanish Progress — {period}

NEW THIS PERIOD
  Vocab words encountered:    {log_data['vocab_created']}
  Grammar patterns learned:   {log_data['topics_created']}
  Error patterns flagged:     {log_data['errors_created']}

QUIZ PERFORMANCE
  {score_line}
  Stage promotions: {promo_line}

PERSISTENT HIGH-MISS ITEMS (< 50% correct, ≥ 2 attempts)
{miss_lines}

OVERALL PROGRESS
  Encountered: {stages['encountered']}  |  Understood: {stages['understood']}  |  Practiced: {stages['practiced']}  |  Automated: {stages['automated']}
  On debt board: {debt_count}

Open Claude Code and type: quiz me
"""

    create_gmail_draft(subject=f"🇪🇸 Spanish Progress — {period}", body=body)
    update_last_summary_date()
    _log(
        f"Summary sent — {period}, {log_data['vocab_created']} vocab, "
        f"{log_data['topics_created']} topics, {len(scores)} quiz(zes)"
    )


if __name__ == "__main__":
    main()
