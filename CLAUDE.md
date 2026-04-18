# Spanish Learning Wiki — Schema

This is Xin Wu's personal Spanish learning wiki. You are the maintainer.  
**You own `wiki/`. You never modify `raw/`.**  
Goal: CEFR B2 from current A2. Primary source: Duolingo.

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
- Related Topics must link to actual existing pages only

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
2. Unless `--silent`: briefly summarise key new items and confirm with user before writing
3. For each new word/phrase → create or update `wiki/vocab/<word>.md`
4. For each pattern/grammar rule → create or update `wiki/topics/<slug>.md`
   - Synthesise: don't just copy notes. Connect to existing topics, add context, flag contradictions
5. For each mistake → check if an error page exists; create or update `wiki/errors/<slug>.md`
6. Update `wiki/curriculum/curriculum-map.md` — add new rows, update stages if evidence warrants
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
- Unlabelled lines → infer from content

### QUERY

**Trigger:** User asks a question

1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Answer with citations: `([[ser-vs-estar]])`, `([[curriculum-map]])`
4. If the answer represents valuable synthesis (a comparison, a connection, a discovery) — offer to file it as a new wiki page

### LINT

**Trigger:** User says `lint wiki`

1. Scan for contradictions between topic hub pages
2. Find orphan pages (no inbound `[[links]]`)
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

---

## Conventions

- File slugs: lowercase, hyphens, no spaces (e.g. `ser-vs-estar.md`, `querer.md`)
- All cross-references use `[[slug]]` wiki-link syntax (no `.md` extension)
- YAML frontmatter required on all topic, vocab, and error pages
- `raw/` files: never create, modify, or delete — read only
- Dates: always YYYY-MM-DD format
