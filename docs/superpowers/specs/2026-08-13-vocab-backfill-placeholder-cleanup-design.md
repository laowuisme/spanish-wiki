# Vocab Backfill Placeholder Cleanup — Design

## Problem

822 of 1,605 files in `wiki/vocab/` (51%) contain auto-generated placeholder content from the bulk backfill commit `1d34fc6` ("feat: backfill 1,182 vocab atoms from Duolingo word export", 2026-06-19), sourced from `raw/duolingo_words_raw.json` (word + translation only, no part-of-speech or usage data).

Every one of these 822 files:
- Has `type: noun` in frontmatter regardless of actual part of speech (many are verbs, adjectives, adverbs, phrases)
- Has a templated `**Pattern:**` line ("Use with article...") that is often meaningless or wrong for the word's real part of speech
- Has a generic, low-value `**Example:**` sentence not grounded in real usage

Identification method: `grep -l "Use with article" wiki/vocab/*.md` → 822 files, confirmed against the known backfill commit.

## Scope

Fix all 822 junk files. Within that set, 20 files also form accent/typo-duplicate pairs discovered during the same investigation — these are handled as part of this same pass since fixing them requires touching the same files.

**Ordering:** Alphabetical sweep, batches of ~50 files each (~17 batches total). No prioritization by curriculum relevance, CEFR level, or debt status — straight alphabetical order through the sorted file list.

## Per-file content fix (the ~800 non-duplicate junk files)

For each file:
1. Determine real part of speech from Spanish-language knowledge (noun/verb/adjective/adverb/phrase/etc.) and correct `type:` in frontmatter.
2. Replace the templated `**Pattern:**` line with something genuinely useful for that word's real grammar (e.g., gender for nouns, conjugation group for verbs, comparison note for adjectives) — or omit the Pattern line if there's nothing meaningful to say, consistent with the Vocab Atom format being optional per-section.
3. Replace the generic `**Example:**` with a real, natural Spanish sentence + translation.
4. Update `last_updated` to today's date.
5. Leave `cefr` as-is unless clearly wrong (e.g., a basic A1 word tagged A2) — use judgment, don't relitigate every value.
6. Leave `stage: encountered` as-is — content quality fixes don't change acquisition stage.
7. `**Meaning:**` stays as the existing raw translation unless it's actively wrong.

## The 20 accent/typo-duplicate pairs

Confirmed via NFD-normalization scan; each pair currently has **two separate files and two separate index.md entries**. Three sub-categories:

### A. 15 junk-vs-real pairs (one junk file, one pre-existing real file, differing only by accent)
`antipatico`/`antipático`, `balcon`/`balcón`, `bañera`/`banera`, `cóctel`/`coctel`, `egoísta`/`egoista`, `en-común`/`en-comun`, `físico`/`fisico`, `peluqueria`/`peluquería`, `pina`/`piña`, `qué-alivio`/`que-alivio`, `sandia`/`sandía`, `sarten`/`sartén`, `tecnologia`/`tecnología`, `traje-de-bano`/`traje-de-baño`, `últimamente`/`ultimamente`.

Resolution per pair:
1. Keep the **correctly-accented** filename (the real Spanish spelling) as the surviving file.
2. Copy/merge the real content from the unaccented file into it (correcting type/pattern/example as needed per the standard fix above).
3. Delete the unaccented file.
4. Remove the unaccented file's line from `wiki/index.md` (15 lines removed total).

### B. 1 junk-vs-junk pair (both files are placeholder junk, same word)
`si-o-si` / `sí-o-sí` — idiom meaning "no matter what."

Resolution:
1. Keep `sí-o-sí` (correct orthography).
2. Write fresh real content (type: phrase, real pattern/example).
3. Delete `si-o-si.md`.
4. Remove its line from `wiki/index.md` (1 line removed — 16 total with group A).

### C. 4 pairs that are NOT duplicates — genuinely distinct words distinguished only by accent
`el`/`él`, `tu`/`tú`, `papa`/`papá`, `cuando`/`cuándo` (8 files total).

Resolution: **no merge, no deletion.** Each of the 8 files is junk and gets an independent real-content rewrite in place (steps 1–7 above), respecting that each pair is two different words (e.g., `el` = "the" vs `él` = "he"). No index.md line removal for this group.

## What stays untouched

- The ~783 pre-existing non-junk vocab files (not matching the junk signature).
- `wiki/topics/`, `wiki/errors/`, `wiki/curriculum/`, `wiki/quiz/` — out of scope.
- `raw/` — never modified, per repo convention.
- Curriculum map / debt board — not touched by this cleanup since `stage` doesn't change.

## Per-batch process

For each batch of ~50 files (alphabetical slice of the 822):
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
- Any typo-dupes among the ~783 non-junk files not already covered by the 20 pairs above (none were found during the scan, but the scan was accent-normalization only, not a full fuzzy-typo check).
