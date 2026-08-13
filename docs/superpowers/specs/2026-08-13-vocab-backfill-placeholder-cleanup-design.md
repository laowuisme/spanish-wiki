# Vocab Backfill Placeholder Cleanup — Design

## Problem

1,161 of 1,605 files in `wiki/vocab/` (72.3%) contain auto-generated placeholder content from two bulk backfill commits:
- `1d34fc6` ("feat: backfill 1,182 vocab atoms from Duolingo word export", 2026-06-19) — created 1,182 files, sourced from `raw/duolingo_words_raw.json` (word + translation only, no part-of-speech or usage data).
- `89d33f3` ("feat: ingest 2026-06-27 — 12 vocab atoms, 1 topic hub, 1 error page, 6 backfill enrichments", 2026-06-27) — created 12 more files via the same broken generator, while separately enriching ~15 previously-junk files with real content on the same date (those enrichments are not junk and are excluded).

Junk files show up to 8 distinct auto-generated template variants (not just one), including:
- `type: noun` in frontmatter regardless of actual part of speech (many are verbs, adjectives, adverbs, phrases)
- A templated `**Pattern:**` line ("Use with article...", "regular use:", "Modifies verbs, adjectives, or other adverbs...", "Day of week; no article", "Month; no capital letter") that is often meaningless or wrong for the word's real part of speech
- A generic, formulaic `**Example:**` sentence not grounded in real usage (e.g. `*Necesito ___.*` filled in mechanically), sometimes with fabricated incorrect forms (e.g. invariable adjectives like `azul`/`gris` given fake feminine/plural forms)
- Broken formatting artifacts (`— — ` double-dash) in some variants

**Identification method:** a single-marker grep (`"Use with article"`) undercounted junk by 41%, finding only 822 files. The corrected method unions 8 content-signature regex markers and validates the result against the git-derived list of files created by the two backfill commits:

```python
markers = [
    r"Use with article",
    r"— — ",
    r"regular use:",
    r"Modifies verbs, adjectives, or other adverbs",
    r"\*Necesito \w+\.\*",
    r"if ends in -o\)",
    r"Day of week; no article",
    r"Month; no capital letter",
]
```

Two broader-looking markers (`"Fixed expression:"`, `"Fixed phrase"`) were tried and rejected — they produced false positives on genuinely well-written entries (`de-acuerdo.md`, `la-proxima-vez.md`, `por-casualidad.md`, `sin-duda.md`, `todo-el-tiempo.md`, `en-comun.md`) where those phrases occur naturally in good prose.

Cross-checking the marker-matched set against every file created by the two backfill commits left 15 files unaccounted for; manual inspection confirmed all 15 are genuinely good, hand-quality content (not junk) and are correctly excluded.

## Scope

Fix all 1,161 junk files. Within that set, 20 files also form accent/typo-duplicate pairs discovered during the same investigation — these are handled as part of this same pass since fixing them requires touching the same files.

**Ordering:** Alphabetical sweep, batches of ~50 files each (24 batches total: 23 full batches of 50 + 1 final batch of 11). No prioritization by curriculum relevance, CEFR level, or debt status — straight alphabetical order through the sorted file list.

## Per-file content fix (the 1,138 non-duplicate junk files)

For each file:
1. Determine real part of speech from Spanish-language knowledge (noun/verb/adjective/adverb/phrase/etc.) and correct `type:` in frontmatter.
2. Replace the templated `**Pattern:**` line with something genuinely useful for that word's real grammar (e.g., gender for nouns, conjugation group for verbs, comparison note for adjectives) — or omit the Pattern line if there's nothing meaningful to say, consistent with the Vocab Atom format being optional per-section.
3. Replace the generic `**Example:**` with a real, natural Spanish sentence + translation.
4. Update `last_updated` to today's date.
5. Leave `cefr` as-is unless clearly wrong (e.g., a basic A1 word tagged A2) — use judgment, don't relitigate every value.
6. Leave `stage: encountered` as-is — content quality fixes don't change acquisition stage.
7. `**Meaning:**` stays as the existing raw translation unless it's actively wrong.

## The 20 accent/typo-duplicate pairs

Confirmed via NFD-normalization scan; each pair currently has **two separate files and two separate index.md entries**. Junk status re-verified per file against the corrected 8-marker detection set. Two categories:

### Category 1: 16 true duplicate pairs (junk file + pre-existing real file, differing only by accent)
`antipatico`/`antipático`, `balcon`/`balcón`, `bañera`/`banera`, `cóctel`/`coctel`, `egoísta`/`egoista`, `en-común`/`en-comun`, `físico`/`fisico`, `peluqueria`/`peluquería`, `pina`/`piña`, `qué-alivio`/`que-alivio`, `sandia`/`sandía`, `sarten`/`sartén`, `tecnologia`/`tecnología`, `traje-de-bano`/`traje-de-baño`, `últimamente`/`ultimamente`, `si-o-si`/`sí-o-sí`.

In every one of these 16 pairs the unaccented filename holds good, pre-existing real content and the accented filename is the junk stub — including `si-o-si.md` (good) / `sí-o-sí.md` (junk), which earlier analysis had mischaracterized as a junk-vs-junk pair.

Resolution per pair:
1. Keep the **correctly-accented** filename (the real Spanish spelling) as the surviving file.
2. Copy/merge the real content from the unaccented file into it (correcting type/pattern/example as needed per the standard fix above).
3. Delete the unaccented file.
4. Remove the unaccented file's line from `wiki/index.md` (16 lines removed total).

### Category 2: 4 pairs that are NOT duplicates — genuinely distinct words distinguished only by accent
`el`/`él`, `tu`/`tú`, `papa`/`papá`, `cuando`/`cuándo` (8 files total, only 7 are junk).

Per-file junk status: `el.md` junk, `él.md` junk, `tu.md` junk, `tú.md` junk, `papa.md` junk, `papá.md` junk, `cuando.md` **not junk** (good pre-existing content, no edit needed), `cuándo.md` junk.

Resolution: **no merge, no deletion.** Each of the 7 junk files gets an independent real-content rewrite in place (steps 1–7 above), respecting that each pair is two different words (e.g., `el` = "the" vs `él` = "he"). `cuando.md` is skipped entirely — it already has real content. No index.md line removal for this group.

## What stays untouched

- The 444 pre-existing non-junk vocab files (not matching the junk signature), including `si-o-si.md` and `cuando.md`.
- `wiki/topics/`, `wiki/errors/`, `wiki/curriculum/`, `wiki/quiz/` — out of scope.
- `raw/` — never modified, per repo convention.
- Curriculum map / debt board — not touched by this cleanup since `stage` doesn't change.

## Per-batch process

For each batch of ~50 files (alphabetical slice of the 1,161):
1. Rewrite each file's content per the rules above.
2. For any duplicate-pair files that fall in this batch: delete the losing file, remove its `wiki/index.md` line.
3. `git add wiki/` and commit with prefix `fix:` (e.g., `fix: correct vocab placeholder content, batch 3 (abr–arr)`).
4. Push to remote after each batch commit (matches this repo's existing convention of pushing after every completed operation).
5. Append one entry to `wiki/log.md` per batch:
   ```
   ## [YYYY-MM-DD] fix | vocab placeholder cleanup batch N
   - N files corrected (type/pattern/example rewritten)
   - N duplicate files removed (if any this batch)
   ```

A final summary log entry is not planned separately — the per-batch log entries constitute the full record.

## Out of scope (explicitly deferred)

- Full inflection/conjugation consolidation (the original broader request) — narrowed away earlier in this conversation.
- Any typo-dupes among the 444 non-junk files not already covered by the 20 pairs above (none were found during the scan, but the scan was accent-normalization only, not a full fuzzy-typo check).
