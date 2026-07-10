# Spanish Learning Wiki — Schema

This is Xin Wu's personal Spanish learning wiki. You are the maintainer.  
**You own `wiki/`. You never modify `raw/`.**  
Goal: CEFR B2 from current A2. Primary source: Duolingo.

---

## Git

Remote: `https://github.com/laowuisme/spanish-wiki` (branch: `master`)

After completing any operation (INGEST, QUIZ, LINT, BOOTSTRAP), stage all changed wiki files and push:

```bash
git add wiki/
git commit -m "<type>: <brief description>"
git push
```

Do not stage `raw/` or `.claude/`. Use conventional commit prefixes: `feat` for new pages, `chore` for curriculum/index updates, `fix` for corrections.

---

## Directory Layout

```
raw/                    # Immutable source files — read only, never modify
  bootstrap/            # One-time historical exports (Google Sheets CSV)
  YYYY-MM-DD_session.md # Ongoing Duolingo session notes

wiki/
  index.md              # Page catalog — read this first on every query
  log.md                # Append-only operation history
  curriculum/
    curriculum-map.md   # All topics × CEFR × acquisition stage
    debt-board.md       # Items stuck > 2 weeks at Encountered or Understood
  topics/               # Synthesis hub pages — one per grammar/pattern concept
  vocab/                # Lightweight concept atoms — individual words/phrases
  errors/               # Recurring error pattern analysis
  quiz/
    performance.md      # Quiz performance log — one row per item ever quizzed
    history/            # Per-session quiz transcripts (YYYY-MM-DD_quiz.md)
```

---

## Acquisition Stage Model

Every topic and vocab item has a stage. Track it in YAML frontmatter.

| Stage | Definition | How to advance |
|---|---|---|
| `encountered` | Seen and flagged, not internalized | Present in raw notes |
| `understood` | Can explain the rule or meaning | Topic hub page created with full explanation |
| `practiced` | Used correctly in controlled contexts | ≥ 3 correct quiz attempts OR correct usage in session notes |
| `automated` | Comes naturally, no conscious effort | Consistent correct usage, zero errors in last 30 days |

**Debt flag:** Any item at `encountered` or `understood` for > 2 weeks → appears on debt-board.md

---

## Page Formats

### Topic Hub (`wiki/topics/<slug>.md`)

```yaml
---
cefr: A1
stage: encountered
last_updated: YYYY-MM-DD
debt: false
sources:
  - raw/2026-04-18_session.md
---
```

Sections: `## Rule`, `## Common Patterns`, `## Your Mistakes`, `## Related Topics`, `## Examples From Your Notes`

- Use `[[wiki-links]]` for all cross-references
- Pull direct quotes from raw sources under Examples
- Related Topics must link to actual existing pages only. If a related topic doesn't have a page yet, mention it in plain text without a link and append `(not yet created)`. On future LINT passes, offer to create stubs for these.

### Vocab Atom (`wiki/vocab/<word>.md`)

```yaml
---
cefr: A1
stage: encountered
type: verb
last_updated: YYYY-MM-DD
---
```

Sections: `**Meaning:**`, `**Pattern:**` (link to topic hub if applicable), `**Example:**` (italicised Spanish + translation)

### Error Page (`wiki/errors/<slug>.md`)

```yaml
---
cefr: A2
frequency: high
last_updated: YYYY-MM-DD
---
```

Sections: `## What Goes Wrong`, `## Why It Happens`, `## Correct Usage`, `## Your Examples`, `## Related Topics`

---

## Operations

### INGEST

**Trigger:** User says `ingest <filename>` or `ingest --silent <filename>`

1. Read the raw file in full
2. Unless `--silent`: briefly summarise key new items (list vocab, patterns, mistakes found). Ask user yes/no: "Proceed with ingest?" If no, abort entirely. If yes, proceed with steps 3–9.
3. For each new word/phrase → create or update `wiki/vocab/<word>.md`
4. For each pattern/grammar rule → create or update `wiki/topics/<slug>.md`
   - Synthesise: don't just copy notes. Connect to existing topics, add context, flag contradictions
   - **If a page already exists:** append new evidence to `## Examples From Your Notes`, update `last_updated` in frontmatter, and update `stage` only if new evidence explicitly warrants promotion. Do not replace existing content.
5. For each mistake → check if an error page exists; create or update `wiki/errors/<slug>.md`
6. Update `wiki/curriculum/curriculum-map.md` — add new rows for new topics, update `Last Practiced` to the date from the raw note filename, recalculate `Days Since` and `Debt?` for ALL existing rows. Stage values in page frontmatter are the source of truth — sync the curriculum map to reflect them.
7. Regenerate `wiki/curriculum/debt-board.md` — flag all items at encountered/understood > 2 weeks
8. Update `wiki/index.md` — add entries for any new pages created
9. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <filename>
   - N vocab atoms created/updated
   - N topic hubs created/updated
   - N error pages created/updated
   ```

**Raw note label mapping:**
- `new words:` → vocab atoms
- `new patterns:` → topic hubs
- `mistakes:` → error pages
- Unlabelled lines → infer only if the line contains a concrete language unit (a word, grammar rule, or error pattern). Skip lines that are context noise (e.g., "difficult session", "forgot my notes", "short session today").

### QUERY

**Trigger:** User asks a question

1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Answer with citations: `([[ser-vs-estar]])`, `([[curriculum-map]])`
4. If the answer represents valuable synthesis (a comparison, a connection, a discovery) — offer to file it as a new wiki page

### LINT

**Trigger:** User says `lint wiki`

1. Scan for contradictions between topic hub pages
2. Find orphan pages — topic/vocab/error pages that have no inbound `[[links]]` from other topic/vocab/error pages or from `index.md`. Curriculum pages (`curriculum-map`, `debt-board`) are exempt from orphan checks.
3. Find concepts mentioned in pages but lacking their own page
4. Find items at `encountered` or `understood` > 30 days (escalate to urgent debt)
5. Suggest Duolingo units or focus topics based on debt board
6. Report findings as a numbered list — user decides what to act on
7. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] lint
   - N orphans found
   - N contradictions found
   - N urgent debt items
   ```

### BOOTSTRAP

**Trigger:** User says `bootstrap raw/bootstrap/ledger-export.csv`

This is a one-time full history ingest. Process all rows in the CSV:
1. Map columns to raw note labels: treat each row as a session note entry
2. Group entries by date if a date column exists — process chronologically
3. Run the full INGEST workflow across all entries
4. After processing, generate a bootstrap summary:
   - Total vocab atoms created
   - Total topic hubs created
   - Total error pages created
   - Curriculum map row count
   - Debt board summary (how many items, oldest item date)
5. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] bootstrap | ledger-export.csv
   - N entries processed
   - N vocab atoms created
   - N topic hubs created
   - N error pages created
   ```

### QUIZ

**Trigger:** User says `quiz me`

**Question pool (10 per quiz):** 5 vocab, 3 topic, 2 error. If any pool type cannot fill its quota from qualifying items, fill remaining slots with the highest-weighted items from the other pool types. Each slug may appear at most once per quiz session.

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
- Vocab (EN→ES): "How do you say '[English meaning]' in Spanish?" (vary direction across vocab questions; no strict alternation required)
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

✓ Correct. [one-line note from the page's **Example:** or **Pattern:** section, if it adds useful context]
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
   - If the file does not exist, create it with the standard table header (# Quiz Performance / _Last updated: YYYY-MM-DD_ / table header row) before writing.
   - For each item quizzed: increment Attempts; if correct increment Correct and Streak, else reset Streak to 0; update Last Quizzed to today; update Last Result.
   - If item not yet in table: add a new row with Attempts=1, Correct=0 or 1, Streak=0 or 1, Last Quizzed=today.

2. Apply stage promotions:
   - For each item where Streak >= 3 AND stage is `encountered` or `understood`:
     - Advance stage one level: encountered → understood, understood → practiced
     - Update `stage` in that page's YAML frontmatter and `last_updated` to today
     - Update Stage column in `wiki/curriculum/curriculum-map.md` for that slug

3. Apply error promotions:
   - For each item where Attempts >= 2 AND (Correct / Attempts) < 0.5 AND the item appears on at least 2 distinct Last Quizzed dates in performance.md:
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

6. Create a Gmail draft to laowuisme@gmail.com using `mcp__claude_ai_Gmail__create_draft`:
   - Subject: `🇪🇸 Spanish Quiz Results — YYYY-MM-DD`
   - Body:
     ```
     Score: N/10
     
     ✓ Correct: slug1, slug2, ...
     ✗ Missed: slug3 (you said "X"), slug4 (you said "Y")
     
     Stage promotions: [if any, else omit line]
     New errors flagged: [if any, else omit line]
     
     Next quiz: Tuesday, Thursday, or Saturday at 9pm SGT.
     ```

---

## Curriculum Map Format

`wiki/curriculum/curriculum-map.md` must stay as a valid markdown table:

```markdown
# Curriculum Map
_Last updated: YYYY-MM-DD_

| Topic | CEFR | Stage | Last Practiced | Days Since | Debt? |
|---|---|---|---|---|---|
| Ser vs Estar | A1 | practiced | 2026-04-10 | 8 | No |
| Reflexive Verbs | A2 | understood | 2026-03-20 | 29 | YES ⚠️ |
```

Update `Days Since` and `Debt?` on every ingest and lint pass.

---

## Debt Board Format

`wiki/curriculum/debt-board.md` must be regenerated on every ingest:

**Debt calculation:** `Days Since = today's date - last_updated date on the page frontmatter` (or `last_practiced` in the curriculum map if populated). Debt flag = `Days Since > 14`. Update `Days Since` and `Debt?` columns for ALL existing curriculum map rows on every ingest, not just newly added rows.

```markdown
# Learning Debt Board
_Last updated: YYYY-MM-DD_

## ⚠️ Overdue (stuck > 2 weeks)
- **[[topic-slug]]** — CEFR A2, `understood` since YYYY-MM-DD (N days) — seen N times in notes

## Suggested Next Focus
1. **[[topic-slug]]** — reason why this should be prioritised
2. **[[topic-slug]]** — reason

## ✅ No Debt
_List topics with stage `practiced` or `automated` here if debt board is otherwise empty_
```

---

## Index Format

`wiki/index.md` must stay as a categorised catalog:

```markdown
# Wiki Index
_Last updated: YYYY-MM-DD | N pages total_

## Topics
- [[ser-vs-estar]] — When to use ser vs estar (A1, practiced)

## Vocab
- [[querer]] — to want / to love (A1, understood)

## Errors
- [[confusing-por-para]] — recurring confusion between por and para (A2, high frequency)

## Curriculum
- [[curriculum-map]] — full progress tracker
- [[debt-board]] — items needing attention
```

**Ordering:** Entries within each section are alphabetical by slug. Insert new entries in alphabetical position.

---

## Conventions

- File slugs: lowercase, hyphens, no spaces (e.g. `ser-vs-estar.md`, `querer.md`)
- All cross-references use `[[slug]]` wiki-link syntax (no `.md` extension)
- YAML frontmatter required on all topic, vocab, and error pages
- `raw/` files: never create, modify, or delete — read only
- `last_updated` (page frontmatter) = when this page was created or last edited by the LLM
- `Last Practiced` (curriculum map) = date from the raw note filename being ingested, not today's date. These are different fields.
- Dates: always YYYY-MM-DD format

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `laowuisme/spanish-wiki` (via the `gh` CLI); external PRs are not treated as a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) — no repo-specific overrides. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` + `docs/adr/` at the repo root (neither exists yet; created lazily). See `docs/agents/domain.md`.
