# Spanish Learning Wiki

Personal Spanish learning wiki for Xin Wu. Target: CEFR B2 from A2.

## Structure

- `raw/` — drop source files here (immutable, never edited by LLM)
  - `bootstrap/` — one-time historical exports (Google Sheets CSV)
  - Session notes: `YYYY-MM-DD_session.md`
- `wiki/` — LLM-maintained knowledge base (read this, don't write it)
  - `curriculum/` — curriculum map and debt board
  - `topics/` — grammar and pattern synthesis hubs
  - `vocab/` — individual word/phrase pages
  - `errors/` — recurring error pattern analysis

## Usage

Open this folder as an Obsidian vault. Install the Dataview plugin.

- **Ingest a session:** `ingest raw/YYYY-MM-DD_session.md`
- **Ask a question:** just ask naturally
- **Health check:** `lint wiki`

See `CLAUDE.md` for full schema and workflow details.