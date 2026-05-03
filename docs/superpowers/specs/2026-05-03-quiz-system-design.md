# Quiz System Design
_Date: 2026-05-03_
_Status: Approved_

## Overview

A spaced-repetition quiz system for the Spanish learning wiki. Quizzes are triggered by a scheduled notification (Tue/Thu/Sat 9pm SGT) and taken interactively in a Claude Code session. Results feed a performance tracker and eventually promote items into the `errors/` section or advance their acquisition stage.

---

## Architecture

### New files

```
wiki/quiz/
  performance.md          # Central performance log — one row per item ever quizzed
  history/
    YYYY-MM-DD_quiz.md    # Per-session transcript — questions, answers, pass/fail
docs/superpowers/specs/
  2026-05-03-quiz-system-design.md   # This file
```

### Modified files

- `CLAUDE.md` — new QUIZ operation spec added
- `wiki/log.md` — quiz sessions appended like ingests
- `wiki/curriculum/curriculum-map.md` — stage column updated on promotion
- `wiki/errors/` — new error pages created when miss threshold is reached
- Individual topic/vocab frontmatter — `stage` field updated on promotion

### No changes to existing vocab/topic frontmatter for performance data

All performance data lives in `wiki/quiz/performance.md`. The 200+ existing wiki pages are not touched by the quiz system except for `stage` updates on promotion.

---

## End-to-End Flow

```
Cron fires (Tue/Thu/Sat 0013 UTC = 9pm SGT)
  → push notification to device
  → Gmail with item summary

User opens Claude Code → types "quiz me"
  → Claude reads performance.md + wiki pages
  → Applies weighting → selects 10 questions
  → Interactive Q&A (one question at a time)
  → End-of-session summary shown in terminal

Post-quiz (automatic):
  → performance.md updated
  → Stage promotions applied to pages + curriculum map
  → Error promotions applied to wiki/errors/
  → history/YYYY-MM-DD_quiz.md written
  → log.md appended
  → Gmail summary sent
```

---

## Question Selection

### Pool composition (per quiz, 10 questions total)

| Type | Count | Source |
|---|---|---|
| Vocab | 5 | `wiki/vocab/` |
| Grammar/topic | 3 | `wiki/topics/` |
| Error patterns | 2 | `wiki/errors/` (fill with vocab if <2 error pages) |

### Item weighting

| Signal | Multiplier |
|---|---|
| Item in `wiki/errors/` | 3× |
| Last quiz result = incorrect | 3× |
| Added within last 7 days | 2× |
| On debt board (>14 days unpracticed) | 2× |
| Previously quizzed, streak < 3 | 1× |
| Never quizzed before | 1× |
| Stage = `practiced` or `automated` | 0.5× |

Multipliers stack. An item that is both new (2×) and previously missed (3×) scores 6×.

### Question formats

**Vocab:**
- ES→EN: "What does *entretenido* mean?"
- EN→ES: "How do you say 'mailbox' in Spanish?"
- Sentence use (B1 items): "Use *quizás* in a sentence."

**Topics:**
- Fill-in-the-blank: drawn from `## Common Patterns` table
- Choose correct: "Which is correct: A or B?"
- Translate: "Translate: 'I know that you have it.'"

**Errors:**
- Correct the mistake: drawn from `## What Goes Wrong` section

### Answer evaluation

Claude accepts near-correct answers as correct (minor spelling errors, missing accent, clear English paraphrase). The exact form is noted but not penalised. Rationale: this is a recall quiz, not a spelling test.

---

## Interactive Quiz UX

```
Question 1/10 [vocab]
How do you say "mailbox" in Spanish?

> buzón

✓ Correct. El buzón — note the accent.
```

```
Question 3/10 [grammar]
Complete: "No trabaja ___ por la mañana." (nobody)

> nadie

✓ Correct. Post-verb → double negation required: No trabaja nadie.
```

```
Question 7/10 [vocab]
What does "lamentablemente" mean?

> unluckily

✗ Incorrect. lamentablemente = unfortunately / regrettably (from lamentar).
```

No retries within a session — retrying immediately does not test real recall.

**End-of-session summary:**
```
Quiz complete — 8/10

✓ Correct (8): buzón, nadie, lamentablemente...
✗ Missed (2):
  • dar — you said "llevar". dar = to give (doy/das/da)
  • sorprendido vs sorprendente — review: [[sorprendido-vs-sorprendente]]

Stage promotions: quizás → practiced (3-quiz streak)
New error flagged: dar (missed in 2 separate sessions)
```

---

## Performance Tracking Schema

### `wiki/quiz/performance.md`

```markdown
# Quiz Performance
_Last updated: YYYY-MM-DD_

| Slug | Type | Attempts | Correct | Streak | Last Quizzed | Last Result |
|---|---|---|---|---|---|---|
| buzón | vocab | 3 | 3 | 3 | 2026-05-06 | correct |
| dar | vocab | 2 | 0 | 0 | 2026-05-08 | incorrect |
| nadie-nada-negation | topic | 1 | 1 | 1 | 2026-05-06 | correct |
| algo-vs-algun | error | 4 | 2 | 0 | 2026-05-08 | incorrect |
```

### `wiki/quiz/history/YYYY-MM-DD_quiz.md`

```markdown
# Quiz — YYYY-MM-DD

Score: 8/10

| # | Slug | Type | Question | Your Answer | Result |
|---|---|---|---|---|---|
| 1 | buzón | vocab | How do you say "mailbox"? | buzón | correct |
| 2 | dar | vocab | How do you say "to give"? | llevar | incorrect |
```

---

## Promotion Rules

### Stage promotion (acquisition model advancement)

- **Trigger:** `streak >= 3` on an item whose current stage is `encountered` or `understood`
- **Action:** Advance stage one level (encountered → understood, understood → practiced)
- **Writes to:** Page frontmatter `stage` field + `curriculum-map.md` Stage column

Items in errors/ require `streak >= 5` before their error page is archived.

### Error promotion (quiz-driven)

- **Trigger:** `attempts >= 2` AND `correct / attempts < 0.5` across at least 2 different quiz dates
- **Action:** Create or update `wiki/errors/<slug>.md` with a `## Quiz Evidence` section listing quiz dates and wrong answers given
- **Weight:** Error items permanently hold 3× weight until `streak >= 5`

### Coexistence with INGEST errors

INGEST writes to `wiki/errors/` from observed session mistakes (current behaviour, unchanged). Quiz writes to `wiki/errors/` from performance data. Both use the same file format. An item can have evidence from both sources in the same error page.

---

## Scheduling & Notification

**Cron:** `0 13 * * 2,4,6` (UTC) = Tue/Thu/Sat 9:00pm SGT

**Cron agent responsibilities (minimal):**
1. Read `performance.md` — count items due (new + debt + high-miss)
2. Send push notification
3. Send Gmail

**Push notification format:**
```
🇪🇸 Spanish quiz ready
12 items prioritised (3 new, 2 overdue, 2 high-miss). Run "quiz me".
```

**Gmail format:**
```
Subject: 🇪🇸 Spanish Quiz — [Day] 9pm

N items queued for tonight's quiz.
Highlights: [top 3 items by weight]

Open Claude Code and type: quiz me
```

**Skip behaviour:** No catch-up quiz generated. Skipped items accumulate weight and surface more strongly in the next session.

**Manual trigger:** `quiz me` works any time outside the schedule. Cron notification on the next scheduled day reflects updated performance.

---

## CLAUDE.md Addition — QUIZ Operation

```
### QUIZ

**Trigger:** User says `quiz me`

1. Read `wiki/quiz/performance.md` and relevant wiki pages
2. Select 10 questions using the weighting algorithm (5 vocab, 3 topic, 2 error)
3. Ask questions one at a time; evaluate each answer immediately
4. After all 10: display end-of-session summary
5. Update `wiki/quiz/performance.md` — increment attempts, correct, streak for each item
6. Apply stage promotions where streak >= 3
7. Apply error promotions where miss threshold is met
8. Write `wiki/quiz/history/YYYY-MM-DD_quiz.md`
9. Append to `wiki/log.md`:
   ## [YYYY-MM-DD] quiz
   - Score: N/10
   - N stage promotions
   - N new errors flagged
10. Send Gmail summary
```

---

## Out of Scope

- Anki integration
- Audio/pronunciation quizzing
- Sentence construction grading beyond loose equivalence
- Leaderboards or streaks visible outside the wiki
