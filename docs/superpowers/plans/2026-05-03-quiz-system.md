# Quiz System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a spaced-repetition quiz system to the Spanish wiki — scheduled Tue/Thu/Sat 9pm SGT notifications, interactive `quiz me` sessions in Claude Code, and automatic performance tracking that feeds stage promotions and error pages.

**Architecture:** Quiz state lives in `wiki/quiz/performance.md` (one row per item ever quizzed); per-session transcripts go in `wiki/quiz/history/`. The QUIZ operation is defined in CLAUDE.md and executed by Claude interactively. A registered cron agent fires at `0 13 * * 2,4,6` UTC and sends push + Gmail notifications only — it does not run the quiz itself.

**Tech Stack:** Markdown files, YAML frontmatter, Claude Code (executor), Gmail MCP (`mcp__claude_ai_Gmail__create_draft` / `mcp__claude_ai_Gmail__search_threads`), PushNotification tool, CronCreate tool.

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `wiki/quiz/performance.md` | Create | Central performance log — one row per quizzed item |
| `wiki/quiz/history/.gitkeep` | Create | Ensures history/ directory is tracked by git |
| `CLAUDE.md` | Modify | Add QUIZ operation section after BOOTSTRAP |
| `wiki/log.md` | Modified at runtime | Quiz sessions appended after each quiz |
| `wiki/quiz/history/YYYY-MM-DD_quiz.md` | Created at runtime | Per-session transcript |
| `wiki/errors/<slug>.md` | Modified at runtime | Quiz Evidence section added on error promotion |
| `wiki/vocab/<slug>.md` / `wiki/topics/<slug>.md` | Modified at runtime | `stage` frontmatter updated on stage promotion |
| `wiki/curriculum/curriculum-map.md` | Modified at runtime | Stage column updated on stage promotion |

---

## Task 1: Scaffold the quiz directory

**Files:**
- Create: `wiki/quiz/performance.md`
- Create: `wiki/quiz/history/.gitkeep`

- [ ] **Step 1: Create `wiki/quiz/performance.md` with header and empty table**

Create the file with this exact content:

```markdown
# Quiz Performance
_Last updated: 2026-05-03_

| Slug | Type | Attempts | Correct | Streak | Last Quizzed | Last Result |
|---|---|---|---|---|---|---|
```

- [ ] **Step 2: Create `wiki/quiz/history/.gitkeep`**

Create an empty file at `wiki/quiz/history/.gitkeep` so git tracks the directory.

- [ ] **Step 3: Verify both files exist**

Run:
```bash
ls -la /Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/
ls -la /Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/history/
```

Expected output:
```
wiki/quiz/
  performance.md
  history/

wiki/quiz/history/
  .gitkeep
```

- [ ] **Step 4: Verify performance.md has correct format**

Run:
```bash
cat /Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/performance.md
```

Expected: the header + empty table shown in Step 1. No extra content.

- [ ] **Step 5: Commit**

```bash
git add wiki/quiz/performance.md wiki/quiz/history/.gitkeep
git commit -m "feat: scaffold wiki/quiz directory — performance.md and history/"
```

---

## Task 2: Add QUIZ operation to CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` — append QUIZ operation after the BOOTSTRAP section

- [ ] **Step 1: Verify current CLAUDE.md ends after BOOTSTRAP**

Read `CLAUDE.md` and confirm the last operation defined is BOOTSTRAP. The new QUIZ section will be inserted between BOOTSTRAP and the `---` separator before Curriculum Map Format.

- [ ] **Step 2: Insert the QUIZ operation section**

In `CLAUDE.md`, after the BOOTSTRAP section (after the closing ``` of the bootstrap log format) and before `---\n\n## Curriculum Map Format`, insert:

```markdown

### QUIZ

**Trigger:** User says `quiz me`

**Question pool (10 per quiz):** 5 vocab, 3 topic, 2 error. If fewer than 2 error pages exist, replace with vocab.

**Item weighting — score each candidate item, higher = more likely selected:**

| Signal | Multiplier |
|---|---|
| Item in `wiki/errors/` | 3× |
| Last quiz result = incorrect (from performance.md) | 3× |
| `last_updated` within 7 days of today | 2× |
| Days Since > 14 in curriculum-map (debt board) | 2× |
| Previously quizzed, streak < 3 | 1× |
| Never quizzed before | 1× |
| Stage = `practiced` or `automated` | 0.5× |

Multipliers stack. Select top-weighted items within each pool type. Randomise among items with equal score.

**Question formats by type:**

- Vocab (ES→EN): "What does *[Spanish word]* mean?"
- Vocab (EN→ES): "How do you say '[English meaning]' in Spanish?" (alternate direction each question)
- Vocab (B1, sentence use): "Use *[word]* in a Spanish sentence."
- Topic (fill-blank): "Complete: '[sentence with ___]' ([English hint])" — drawn from `## Common Patterns` table
- Topic (choose correct): "Which is correct: A or B?" — drawn from `## Common Patterns` table
- Topic (translate): "Translate: '[English sentence]'" — drawn from `## Examples From Your Notes`
- Error (correct the mistake): "Correct this sentence: '[wrong sentence]'" — drawn from `## What Goes Wrong`

**Answer evaluation:** Accept near-correct answers as correct (minor spelling, missing accent, clear English paraphrase). Note the exact form but do not penalise. No retries within a session.

**Interactive UX (one question at a time):**

```
Question N/10 [type]
[question text]

> [user's answer]

✓ Correct. [one-line note from wiki page if useful]
— or —
✗ Incorrect. [correct answer] — [one-line explanation from wiki page]
```

**End-of-session summary (shown after question 10):**

```
Quiz complete — N/10

✓ Correct (N): slug1, slug2, ...
✗ Missed (N):
  • slug — you said "X". Correct: Y — [brief note]

Stage promotions: [slug → new-stage] (N-quiz streak)
New errors flagged: [slug] (missed in N separate sessions)
```

**Post-quiz steps (execute automatically after summary):**

1. Update `wiki/quiz/performance.md`:
   - For each item quizzed: increment Attempts; if correct increment Correct and Streak, else reset Streak to 0; update Last Quizzed to today; update Last Result.
   - If item not yet in table: add a new row with Attempts=1, Correct=0 or 1, Streak=0 or 1, Last Quizzed=today.

2. Apply stage promotions:
   - For each item where Streak >= 3 AND stage is `encountered` or `understood`:
     - Advance stage one level: encountered → understood, understood → practiced
     - Update `stage` in that page's YAML frontmatter and `last_updated` to today
     - Update Stage column in `wiki/curriculum/curriculum-map.md` for that slug

3. Apply error promotions:
   - For each item where Attempts >= 2 AND (Correct / Attempts) < 0.5 AND the item appears in at least 2 distinct Last Quizzed dates in performance.md:
     - If `wiki/errors/<slug>.md` does not exist: create it with standard error page format plus a `## Quiz Evidence` section
     - If `wiki/errors/<slug>.md` exists: append to or create `## Quiz Evidence` section listing quiz dates and wrong answers given
     - `## Quiz Evidence` format:
       ```
       ## Quiz Evidence
       - 2026-05-06: asked "What does X mean?", answered "Y" (incorrect)
       - 2026-05-08: asked "How do you say X?", answered "Z" (incorrect)
       ```

4. Write `wiki/quiz/history/YYYY-MM-DD_quiz.md` (today's date):
   ```markdown
   # Quiz — YYYY-MM-DD
   
   Score: N/10
   
   | # | Slug | Type | Question | Your Answer | Result |
   |---|---|---|---|---|---|
   | 1 | slug | vocab | question text | answer given | correct |
   | 2 | slug | topic | question text | answer given | incorrect |
   ```

5. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] quiz
   - Score: N/10
   - N stage promotions: [slug → stage, ...]
   - N new errors flagged: [slug, ...]
   ```

6. Send Gmail summary using mcp__claude_ai_Gmail__create_draft then send, to laowuisme@gmail.com:
   - Subject: `🇪🇸 Spanish Quiz Results — YYYY-MM-DD`
   - Body:
     ```
     Score: N/10
     
     ✓ Correct: slug1, slug2, ...
     ✗ Missed: slug3 (you said "X"), slug4 (you said "Y")
     
     Stage promotions: [if any]
     New errors flagged: [if any]
     
     Next quiz: [next scheduled day] at 9pm SGT.
     ```
```

- [ ] **Step 3: Read back the QUIZ section in CLAUDE.md and verify it was inserted correctly**

Confirm:
- QUIZ section appears after BOOTSTRAP and before `## Curriculum Map Format`
- All 6 post-quiz steps are present
- Weighting table is intact
- Gmail step references `laowuisme@gmail.com`

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add QUIZ operation to CLAUDE.md"
```

---

## Task 3: Dry-run the QUIZ operation

This task verifies the full interactive flow end-to-end before the cron is set up.

**Files modified at runtime:**
- `wiki/quiz/performance.md` — rows added
- `wiki/quiz/history/YYYY-MM-DD_quiz.md` — created
- `wiki/log.md` — appended

- [ ] **Step 1: Define expected outputs before running**

Before triggering `quiz me`, note today's date and confirm:
- `wiki/quiz/performance.md` currently has zero data rows (empty table)
- `wiki/quiz/history/` contains only `.gitkeep`
- `wiki/log.md` last entry is the `2026-05-02 ingest` entry

- [ ] **Step 2: Trigger the quiz**

Type `quiz me` in Claude Code. Complete all 10 questions. For this dry-run, intentionally answer 2–3 questions incorrectly so that the incorrect-answer path is exercised.

- [ ] **Step 3: Verify performance.md was updated**

After quiz completes, read `wiki/quiz/performance.md`. Confirm:
- Exactly 10 rows added (one per quizzed item)
- Attempts = 1 for all rows (first quiz ever)
- Correct column matches how many you answered correctly
- Streak = 1 for correct, 0 for incorrect
- Last Quizzed = today's date (YYYY-MM-DD)
- Last Result = correct or incorrect per item

- [ ] **Step 4: Verify history file was created**

Run:
```bash
ls /Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/history/
```

Expected: one file named `YYYY-MM-DD_quiz.md` (today's date). Read it and confirm it has 10 rows in the transcript table.

- [ ] **Step 5: Verify log.md was appended**

Read `wiki/log.md`. The last entry should be:
```
## [YYYY-MM-DD] quiz
- Score: N/10
- 0 stage promotions (first quiz, no streaks yet)
- 0 new errors flagged (need 2 separate sessions to trigger)
```

- [ ] **Step 6: Verify Gmail summary was sent**

Check `laowuisme@gmail.com` for an email with subject `🇪🇸 Spanish Quiz Results — YYYY-MM-DD`. Confirm it contains the score, correct/missed slugs, and "Next quiz" line.

- [ ] **Step 7: Fix any deviations found**

If any step above produced unexpected output (wrong table format, missing columns, wrong item count), update the QUIZ section in `CLAUDE.md` to correct the behaviour, then re-run from Step 2.

- [ ] **Step 8: Commit**

```bash
git add wiki/quiz/performance.md wiki/quiz/history/ wiki/log.md
git commit -m "feat: first quiz dry-run — performance.md and history seeded"
```

---

## Task 4: Register the cron notification agent

The cron agent fires Tue/Thu/Sat at 0013 UTC (9pm SGT). It reads performance.md, counts prioritised items, sends push notification and Gmail. It does NOT run the quiz.

**Files:**
- Create: `docs/quiz-cron-prompt.md` — canonical prompt for the scheduled agent (source of truth)

- [ ] **Step 1: Create `docs/quiz-cron-prompt.md`**

Create the file with this exact content:

```markdown
# Quiz Cron Agent Prompt

This agent fires Tue/Thu/Sat at 9pm SGT. Its only job is to count prioritised quiz items and send a notification. It does NOT run the quiz.

## Instructions

1. Read `/Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/performance.md`
2. Read `/Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/curriculum/curriculum-map.md`
3. Count items by priority bucket:
   - **New** (last_updated within 7 days, never quizzed): read vocab/topic pages, check last_updated frontmatter vs today
   - **Overdue** (Days Since > 14 in curriculum-map AND stage = encountered or understood)
   - **High-miss** (in performance.md: Correct/Attempts < 0.5 AND Attempts >= 2)
4. Identify top 3 items by weight (apply the same weighting as the QUIZ operation in CLAUDE.md)
5. Send push notification:
   - Title: "🇪🇸 Spanish quiz ready"
   - Body: "[N] items prioritised ([X] new, [Y] overdue, [Z] high-miss). Run 'quiz me'."
6. Send Gmail to laowuisme@gmail.com:
   - Subject: "🇪🇸 Spanish Quiz — [Tuesday/Thursday/Saturday] 9pm"
   - Body:
     "[N] items queued for tonight's quiz.
     Top picks: [slug1] ([reason]), [slug2] ([reason]), [slug3] ([reason])
     
     Open Claude Code and type: quiz me"
7. Do nothing else. Do not modify any wiki files.
```

- [ ] **Step 2: Verify the prompt file reads correctly**

Run:
```bash
cat /Users/laowuisme/Documents/MyWork/spanish-wiki/docs/quiz-cron-prompt.md
```

Confirm all 7 numbered instructions are present and paths are correct.

- [ ] **Step 3: Register the cron using CronCreate**

Use the CronCreate tool with:
- Schedule: `0 13 * * 2,4,6` (UTC)
- Prompt: the full content of `docs/quiz-cron-prompt.md`
- Description: "Spanish quiz notification — Tue/Thu/Sat 9pm SGT"

- [ ] **Step 4: Verify the cron is registered**

Use CronList to confirm the cron appears with the correct schedule `0 13 * * 2,4,6`.

- [ ] **Step 5: Trigger the cron agent manually once to test**

Use RemoteTrigger (or the equivalent manual-fire mechanism) to fire the cron agent immediately. Then:
- Check for push notification on device
- Check `laowuisme@gmail.com` for the notification email
- Confirm the email subject matches `🇪🇸 Spanish Quiz — [Day] 9pm`
- Confirm the body lists N items and top 3 picks

- [ ] **Step 6: Fix any issues**

If the notification or email was malformed, update `docs/quiz-cron-prompt.md` and re-register the cron (delete old entry with CronDelete, re-create with CronCreate).

- [ ] **Step 7: Commit**

```bash
git add docs/quiz-cron-prompt.md
git commit -m "feat: register quiz cron — Tue/Thu/Sat 9pm SGT push + Gmail notification"
```

---

## Task 5: Verify promotion rules with a second quiz session

Run a second quiz to confirm that streak accumulation, stage promotion, and error promotion all fire correctly.

**Files modified at runtime:**
- `wiki/quiz/performance.md` — streaks updated
- Vocab/topic page frontmatter — stage field updated if promotion triggered
- `wiki/curriculum/curriculum-map.md` — Stage column updated if promotion triggered
- `wiki/errors/<slug>.md` — Quiz Evidence section added if error promotion triggered

- [ ] **Step 1: Identify items expected to hit thresholds**

Before running the second quiz, read `wiki/quiz/performance.md` from the dry-run. Note:
- Any items with Streak = 1 that you answered correctly last time — if correct again, Streak becomes 2 (not yet promoted)
- Any items with Last Result = incorrect — watch for error promotion if answered incorrectly again

Since this is only the second quiz, no stage promotions (need streak 3) and no error promotions (need 2 distinct quiz dates AND <50% correct) will fire unless an item was already missed in the dry-run AND is missed again. That's fine — verify the streak counter increments correctly.

- [ ] **Step 2: Run `quiz me` a second time**

Complete all 10 questions. Answer the same incorrectly-answered items from the dry-run incorrectly again (if they appear) to exercise the error-promotion path.

- [ ] **Step 3: Verify performance.md accumulation**

Read `wiki/quiz/performance.md`. For each item that appeared in both quizzes:
- Attempts = 2
- Correct incremented correctly
- Streak: incremented if correct again, reset to 0 if incorrect
- Last Quizzed = today

For items that appeared only once (new selections): Attempts = 1, as in Task 3.

- [ ] **Step 4: Verify error promotion fires if triggered**

If any item has Attempts >= 2, Correct/Attempts < 0.5, and appeared on two different Last Quizzed dates:
- Confirm `wiki/errors/<slug>.md` now contains a `## Quiz Evidence` section
- Confirm the section lists both quiz dates and the wrong answers given

If no item meets the threshold yet (Attempts still only 2 and one correct), confirm no spurious error pages were created.

- [ ] **Step 5: Verify stage promotion fires at streak 3 (simulation)**

Stage promotion requires streak >= 3. After two quizzes, streak is at most 2. To verify promotion logic is correct without running 3 full quizzes, manually edit one row in `performance.md` to have Streak = 2, then run `quiz me` and answer that item correctly. Confirm:
- Streak advances to 3 in performance.md
- The item's page frontmatter `stage` is updated
- curriculum-map.md Stage column reflects the promotion
- The end-of-session summary lists the promotion

After verifying, the Streak value will have naturally become 3 through the quiz, so no cleanup needed.

- [ ] **Step 6: Commit**

```bash
git add wiki/quiz/performance.md wiki/quiz/history/ wiki/log.md
# If any promotions or error pages were triggered:
git add wiki/vocab/ wiki/topics/ wiki/errors/ wiki/curriculum/curriculum-map.md
git commit -m "test: second quiz session — verify streak accumulation and promotion rules"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Covered in task |
|---|---|
| wiki/quiz/performance.md created | Task 1 |
| wiki/quiz/history/ directory | Task 1 |
| QUIZ operation in CLAUDE.md | Task 2 |
| 10 questions: 5 vocab, 3 topic, 2 error | Task 2 (CLAUDE.md) |
| Weighting algorithm (all 7 signals) | Task 2 (CLAUDE.md) |
| Interactive Q&A UX | Task 2 (CLAUDE.md) |
| Near-correct answer leniency | Task 2 (CLAUDE.md) |
| performance.md updated post-quiz | Task 2 + verified Task 3 |
| Stage promotion (streak >= 3) | Task 2 + verified Task 5 |
| Error promotion (2 sessions, <50%) | Task 2 + verified Task 5 |
| history/YYYY-MM-DD_quiz.md written | Task 2 + verified Task 3 |
| log.md appended | Task 2 + verified Task 3 |
| Gmail results summary | Task 2 + verified Task 3 |
| Cron: 0 13 * * 2,4,6 UTC | Task 4 |
| Push notification | Task 4 |
| Gmail notification (pre-quiz) | Task 4 |
| Skip behaviour (no catch-up) | Handled by cron — it reads live performance.md each fire |
| Manual `quiz me` trigger | Works by default — no schedule dependency |

No gaps found.
