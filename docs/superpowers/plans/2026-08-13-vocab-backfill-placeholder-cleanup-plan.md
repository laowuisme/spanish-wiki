# Vocab Backfill Placeholder Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite all 1,161 auto-generated placeholder vocab files in `wiki/vocab/` with real content, and resolve the 20 accent/typo-duplicate pairs uncovered during the same audit.

**Architecture:** Alphabetical sweep in 24 batches of ~50 files. Each batch is a self-contained task: rewrite content, resolve any duplicate pairs whose junk member falls in that batch, commit, push, log. Batches are independent of each other except where a Category 1 duplicate pair requires reading a source file that lives in the untouched (non-junk) file set — never a file from another batch.

**Tech Stack:** Markdown + YAML frontmatter (no code, no test suite — verification is via content-signature grep and manual review of frontmatter validity).

## Global Constraints

- Vocab Atom frontmatter (from `/Users/laowuisme/Documents/MyWork/spanish-wiki/CLAUDE.md`): `cefr`, `stage`, `type`, `last_updated` (YAML).
- Vocab Atom body sections: `**Meaning:**`, `**Pattern:**` (optional, link to topic hub if applicable), `**Example:**` (italicised Spanish + translation).
- File slugs: lowercase, hyphens, no spaces. Cross-references use `[[slug]]` (no `.md` extension).
- Commit message prefix: `fix:`.
- Push to remote after every batch commit (matches this repo's existing convention).
- `raw/` is never created, modified, or deleted.
- Dates: `YYYY-MM-DD` format. Use the actual execution date for `last_updated`, not a hardcoded date — the plan below uses `{today}` as a placeholder for "the date this batch is actually executed," since batches may run across multiple days.
- `wiki/index.md` entries follow the format: `- [[slug]] — meaning (CEFR, stage)`, alphabetical by slug within the `## Vocab` section.

### Content-fix procedure (apply to every junk file, in every batch, unless noted otherwise)

1. Determine the word's real part of speech from Spanish-language knowledge (noun/verb/adjective/adverb/phrase/pronoun/etc.) and correct `type:` in frontmatter.
2. Replace the templated `**Pattern:**` line with something genuinely useful for the word's real grammar (gender for nouns, conjugation group/irregularity for verbs, comparison or invariability note for adjectives, usage note for adverbs/phrases) — or omit the `**Pattern:**` line entirely if there's nothing meaningful to say.
3. Replace the generic `**Example:**` with a real, natural Spanish sentence (italicised) + English translation, grounded in actual usage.
4. Set `last_updated` to the execution date.
5. Leave `cefr` as-is unless clearly wrong (e.g. a basic A1 word tagged A2) — use judgment, don't relitigate every value.
6. Leave `stage: encountered` as-is — content fixes don't change acquisition stage.
7. `**Meaning:**` stays as the existing raw translation unless it's actively wrong.

### Batch verification command (run after rewriting, before committing)

```bash
python3 -c "
import re
markers = [r'Use with article', r'— — ', r'regular use:', r'Modifies verbs, adjectives, or other adverbs', r'\*Necesito \w+\.\*', r'if ends in -o\)', r'Day of week; no article', r'Month; no capital letter']
combined = re.compile('|'.join(markers))
import sys
for path in sys.argv[1:]:
    with open(path, encoding='utf-8') as f:
        if combined.search(f.read()):
            print('STILL JUNK:', path)
" wiki/vocab/FILE1.md wiki/vocab/FILE2.md ...
```
Expected: no output (no file still matches a junk marker). Substitute the batch's actual file list for `FILE1.md wiki/vocab/FILE2.md ...`.

### Log entry template (append to `wiki/log.md` after each batch)

```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch N
- N files corrected (type/pattern/example rewritten)
- N duplicate files removed (if any this batch)
```

---

## Task 1: Generate and commit the authoritative junk file list

**Files:**
- Create: `docs/superpowers/plans/junk_authoritative.txt` (already generated during spec correction — 1,161 filenames, one per line, `wiki/vocab/*.md` basenames, in the exact batch order used by Tasks 2–25 below)

**Interfaces:**
- Produces: the master file list that Tasks 2–25 slice into 24 batches of ~50. No other task depends on regenerating it — the file lists are already embedded directly in each task below, so this file exists purely as an audit trail.

- [ ] **Step 1: Verify the file matches the detection methodology in the spec**

Run:
```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
python3 -c "
import re, glob, os
markers = [r'Use with article', r'— — ', r'regular use:', r'Modifies verbs, adjectives, or other adverbs', r'\*Necesito \w+\.\*', r'if ends in -o\)', r'Day of week; no article', r'Month; no capital letter']
combined = re.compile('|'.join(markers))
files = sorted(glob.glob('wiki/vocab/*.md'))
junk = [os.path.basename(f) for f in files if combined.search(open(f, encoding='utf-8').read())]
print(len(junk))
"
```
Expected: `1161`.

- [ ] **Step 2: Commit the audit-trail file**

```bash
git add docs/superpowers/plans/junk_authoritative.txt
git commit -m "chore: add authoritative junk file list for vocab cleanup batches"
git push
```

---

## Task 2: Batch 1 — `a-la-derecha` .. `almorzar` (50 files)

**Files:**
- Modify: `wiki/vocab/a-la-derecha.md`
- Modify: `wiki/vocab/a-la-izquierda.md`
- Modify: `wiki/vocab/a-las.md`
- Modify: `wiki/vocab/a-menudo.md`
- Modify: `wiki/vocab/a-qué-hora.md`
- Modify: `wiki/vocab/a-tiempo.md`
- Modify: `wiki/vocab/a-veces.md`
- Modify: `wiki/vocab/abierto.md`
- Modify: `wiki/vocab/abogado.md`
- Modify: `wiki/vocab/abrigo.md`
- Modify: `wiki/vocab/abril.md`
- Modify: `wiki/vocab/abrir.md`
- Modify: `wiki/vocab/abuela.md`
- Modify: `wiki/vocab/abuelo.md`
- Modify: `wiki/vocab/abuelos.md`
- Modify: `wiki/vocab/aburrido.md`
- Modify: `wiki/vocab/aceite.md`
- Modify: `wiki/vocab/actividad.md`
- Modify: `wiki/vocab/activo.md`
- Modify: `wiki/vocab/actor.md`
- Modify: `wiki/vocab/actriz.md`
- Modify: `wiki/vocab/adiós.md`
- Modify: `wiki/vocab/adolescente.md`
- Modify: `wiki/vocab/aeropuerto.md`
- Modify: `wiki/vocab/afortunadamente.md`
- Modify: `wiki/vocab/africano.md`
- Modify: `wiki/vocab/agosto.md`
- Modify: `wiki/vocab/agradable.md`
- Modify: `wiki/vocab/agua.md`
- Modify: `wiki/vocab/ah.md`
- Modify: `wiki/vocab/ahí.md`
- Modify: `wiki/vocab/ajo.md`
- Modify: `wiki/vocab/al-aire-libre.md`
- Modify: `wiki/vocab/al-final-de.md`
- Modify: `wiki/vocab/al-lado-de.md`
- Modify: `wiki/vocab/al-mediodía.md`
- Modify: `wiki/vocab/al-norte.md`
- Modify: `wiki/vocab/alcohol.md`
- Modify: `wiki/vocab/alemania.md`
- Modify: `wiki/vocab/alemán.md`
- Modify: `wiki/vocab/alergia.md`
- Modify: `wiki/vocab/algo.md`
- Modify: `wiki/vocab/alguna.md`
- Modify: `wiki/vocab/algunas.md`
- Modify: `wiki/vocab/algunos.md`
- Modify: `wiki/vocab/algún.md`
- Modify: `wiki/vocab/aliviado.md`
- Modify: `wiki/vocab/allá.md`
- Modify: `wiki/vocab/allí.md`
- Modify: `wiki/vocab/almorzar.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
a-la-derecha.md, a-la-izquierda.md, a-las.md, a-menudo.md, a-qué-hora.md, a-tiempo.md, a-veces.md, abierto.md, abogado.md, abrigo.md, abril.md, abrir.md, abuela.md, abuelo.md, abuelos.md, aburrido.md, aceite.md, actividad.md, activo.md, actor.md, actriz.md, adiós.md, adolescente.md, aeropuerto.md, afortunadamente.md, africano.md, agosto.md, agradable.md, agua.md, ah.md, ahí.md, ajo.md, al-aire-libre.md, al-final-de.md, al-lado-de.md, al-mediodía.md, al-norte.md, alcohol.md, alemania.md, alemán.md, alergia.md, algo.md, alguna.md, algunas.md, algunos.md, algún.md, aliviado.md, allá.md, allí.md, almorzar.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 1 (a-la-derecha–almorzar)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 1
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 3 begins.

---

## Task 3: Batch 2 — `almuerzo` .. `barba` (50 files, 2 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/almuerzo.md`
- Modify: `wiki/vocab/alto.md`
- Modify: `wiki/vocab/alérgico.md`
- Modify: `wiki/vocab/amable.md`
- Modify: `wiki/vocab/amarillo.md`
- Modify: `wiki/vocab/ambulancia.md`
- Modify: `wiki/vocab/amiga.md`
- Modify: `wiki/vocab/amigo.md`
- Modify: `wiki/vocab/animal.md`
- Modify: `wiki/vocab/anotar.md`
- Modify: `wiki/vocab/ansioso.md`
- Modify: `wiki/vocab/antes-de.md`
- Modify: `wiki/vocab/antes.md`
- Modify: `wiki/vocab/antiguo.md`
- Modify: `wiki/vocab/antipático.md`
- Modify: `wiki/vocab/apartamento.md`
- Modify: `wiki/vocab/aplicación.md`
- Modify: `wiki/vocab/aproximadamente.md`
- Modify: `wiki/vocab/aquí-tiene.md`
- Modify: `wiki/vocab/aquí.md`
- Modify: `wiki/vocab/archivo.md`
- Modify: `wiki/vocab/arete.md`
- Modify: `wiki/vocab/argentino.md`
- Modify: `wiki/vocab/arquitecto.md`
- Modify: `wiki/vocab/arroz.md`
- Modify: `wiki/vocab/arte.md`
- Modify: `wiki/vocab/artista.md`
- Modify: `wiki/vocab/asado.md`
- Modify: `wiki/vocab/ascensor.md`
- Modify: `wiki/vocab/aspirina.md`
- Modify: `wiki/vocab/así-es.md`
- Modify: `wiki/vocab/atlético.md`
- Modify: `wiki/vocab/autobús.md`
- Modify: `wiki/vocab/avión.md`
- Modify: `wiki/vocab/ay.md`
- Modify: `wiki/vocab/ayuda.md`
- Modify: `wiki/vocab/ayudar.md`
- Modify: `wiki/vocab/azul.md`
- Modify: `wiki/vocab/azúcar.md`
- Modify: `wiki/vocab/año.md`
- Modify: `wiki/vocab/aún.md`
- Modify: `wiki/vocab/bailar.md`
- Modify: `wiki/vocab/bailarín.md`
- Modify: `wiki/vocab/baile.md`
- Modify: `wiki/vocab/bajo.md`
- Modify: `wiki/vocab/balcón.md`
- Modify: `wiki/vocab/banco.md`
- Modify: `wiki/vocab/bar.md`
- Modify: `wiki/vocab/barato.md`
- Modify: `wiki/vocab/barba.md`
- Delete: `wiki/vocab/antipatico.md`
- Delete: `wiki/vocab/balcon.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/antipatico.md`, `wiki/vocab/balcon.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
almuerzo.md, alto.md, alérgico.md, amable.md, amarillo.md, ambulancia.md, amiga.md, amigo.md, animal.md, anotar.md, ansioso.md, antes-de.md, antes.md, antiguo.md, antipático.md, apartamento.md, aplicación.md, aproximadamente.md, aquí-tiene.md, aquí.md, archivo.md, arete.md, argentino.md, arquitecto.md, arroz.md, arte.md, artista.md, asado.md, ascensor.md, aspirina.md, así-es.md, atlético.md, autobús.md, avión.md, ay.md, ayuda.md, ayudar.md, azul.md, azúcar.md, año.md, aún.md, bailar.md, bailarín.md, baile.md, bajo.md, balcón.md, banco.md, bar.md, barato.md, barba.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `antipático.md` / `antipatico.md`:** `antipático.md` is the junk file (Category 1). Read the real content from `wiki/vocab/antipatico.md` and merge it into `wiki/vocab/antipático.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/antipatico.md`. Then remove the line `- [[antipatico]] ...` from `wiki/index.md` (search for the exact line starting with `- [[antipatico]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Duplicate pair — `balcón.md` / `balcon.md`:** `balcón.md` is the junk file (Category 1). Read the real content from `wiki/vocab/balcon.md` and merge it into `wiki/vocab/balcón.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/balcon.md`. Then remove the line `- [[balcon]] ...` from `wiki/index.md` (search for the exact line starting with `- [[balcon]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 2 (almuerzo–barba)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 2
- 50 files corrected (type/pattern/example rewritten)
- 2 duplicate files removed (antipatico.md, balcon.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 4 begins.

---

## Task 4: Batch 3 — `barco` .. `cambiar-dinero` (50 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/barco.md`
- Modify: `wiki/vocab/basta-de.md`
- Modify: `wiki/vocab/bastantes.md`
- Modify: `wiki/vocab/batido.md`
- Modify: `wiki/vocab/bañarse.md`
- Modify: `wiki/vocab/bañera.md`
- Modify: `wiki/vocab/baño.md`
- Modify: `wiki/vocab/beber.md`
- Modify: `wiki/vocab/bebida.md`
- Modify: `wiki/vocab/biblioteca.md`
- Modify: `wiki/vocab/bicicleta.md`
- Modify: `wiki/vocab/bien.md`
- Modify: `wiki/vocab/bienvenida.md`
- Modify: `wiki/vocab/bienvenido.md`
- Modify: `wiki/vocab/bigote.md`
- Modify: `wiki/vocab/bingo.md`
- Modify: `wiki/vocab/blanco.md`
- Modify: `wiki/vocab/blog.md`
- Modify: `wiki/vocab/blusa.md`
- Modify: `wiki/vocab/boleto.md`
- Modify: `wiki/vocab/bolsa.md`
- Modify: `wiki/vocab/bolsas.md`
- Modify: `wiki/vocab/bolso.md`
- Modify: `wiki/vocab/bonito.md`
- Modify: `wiki/vocab/borrador.md`
- Modify: `wiki/vocab/bota.md`
- Modify: `wiki/vocab/botella-de.md`
- Modify: `wiki/vocab/botella.md`
- Modify: `wiki/vocab/boxeo.md`
- Modify: `wiki/vocab/buen-tiempo.md`
- Modify: `wiki/vocab/buenas-noches.md`
- Modify: `wiki/vocab/buenas-noticias.md`
- Modify: `wiki/vocab/buenas-tardes.md`
- Modify: `wiki/vocab/bueno.md`
- Modify: `wiki/vocab/buenos-días.md`
- Modify: `wiki/vocab/básquetbol.md`
- Modify: `wiki/vocab/béisbol.md`
- Modify: `wiki/vocab/caballo.md`
- Modify: `wiki/vocab/cable.md`
- Modify: `wiki/vocab/cafetería.md`
- Modify: `wiki/vocab/café.md`
- Modify: `wiki/vocab/caja.md`
- Modify: `wiki/vocab/cajero-automático.md`
- Modify: `wiki/vocab/calcetín.md`
- Modify: `wiki/vocab/calendario.md`
- Modify: `wiki/vocab/calificación.md`
- Modify: `wiki/vocab/calle.md`
- Modify: `wiki/vocab/calor.md`
- Modify: `wiki/vocab/cambiar-de.md`
- Modify: `wiki/vocab/cambiar-dinero.md`
- Delete: `wiki/vocab/banera.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/banera.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
barco.md, basta-de.md, bastantes.md, batido.md, bañarse.md, bañera.md, baño.md, beber.md, bebida.md, biblioteca.md, bicicleta.md, bien.md, bienvenida.md, bienvenido.md, bigote.md, bingo.md, blanco.md, blog.md, blusa.md, boleto.md, bolsa.md, bolsas.md, bolso.md, bonito.md, borrador.md, bota.md, botella-de.md, botella.md, boxeo.md, buen-tiempo.md, buenas-noches.md, buenas-noticias.md, buenas-tardes.md, bueno.md, buenos-días.md, básquetbol.md, béisbol.md, caballo.md, cable.md, cafetería.md, café.md, caja.md, cajero-automático.md, calcetín.md, calendario.md, calificación.md, calle.md, calor.md, cambiar-de.md, cambiar-dinero.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `bañera.md` / `banera.md`:** `bañera.md` is the junk file (Category 1). Read the real content from `wiki/vocab/banera.md` and merge it into `wiki/vocab/bañera.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/banera.md`. Then remove the line `- [[banera]] ...` from `wiki/index.md` (search for the exact line starting with `- [[banera]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 3 (barco–cambiar-dinero)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 3
- 50 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (banera.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 5 begins.

---

## Task 5: Batch 4 — `caminar` .. `cine` (50 files)

**Files:**
- Modify: `wiki/vocab/caminar.md`
- Modify: `wiki/vocab/caminata.md`
- Modify: `wiki/vocab/camisa.md`
- Modify: `wiki/vocab/camiseta.md`
- Modify: `wiki/vocab/campamento.md`
- Modify: `wiki/vocab/campeón.md`
- Modify: `wiki/vocab/campo.md`
- Modify: `wiki/vocab/canadiense.md`
- Modify: `wiki/vocab/cansado.md`
- Modify: `wiki/vocab/cantar.md`
- Modify: `wiki/vocab/capital.md`
- Modify: `wiki/vocab/cargador.md`
- Modify: `wiki/vocab/cargar.md`
- Modify: `wiki/vocab/carne.md`
- Modify: `wiki/vocab/caro.md`
- Modify: `wiki/vocab/carta.md`
- Modify: `wiki/vocab/cartera.md`
- Modify: `wiki/vocab/casa.md`
- Modify: `wiki/vocab/castillo.md`
- Modify: `wiki/vocab/catedral.md`
- Modify: `wiki/vocab/catorce.md`
- Modify: `wiki/vocab/cebolla.md`
- Modify: `wiki/vocab/celebrar.md`
- Modify: `wiki/vocab/celular.md`
- Modify: `wiki/vocab/cena.md`
- Modify: `wiki/vocab/cenar.md`
- Modify: `wiki/vocab/centro-comercial.md`
- Modify: `wiki/vocab/centro.md`
- Modify: `wiki/vocab/cepillarse.md`
- Modify: `wiki/vocab/cepillo.md`
- Modify: `wiki/vocab/cerca-de.md`
- Modify: `wiki/vocab/cerrar.md`
- Modify: `wiki/vocab/cerveza.md`
- Modify: `wiki/vocab/champán.md`
- Modify: `wiki/vocab/chaqueta.md`
- Modify: `wiki/vocab/charco.md`
- Modify: `wiki/vocab/chef.md`
- Modify: `wiki/vocab/chica.md`
- Modify: `wiki/vocab/chico.md`
- Modify: `wiki/vocab/chicos.md`
- Modify: `wiki/vocab/chile.md`
- Modify: `wiki/vocab/chileno.md`
- Modify: `wiki/vocab/chino.md`
- Modify: `wiki/vocab/chismoso.md`
- Modify: `wiki/vocab/chocolate.md`
- Modify: `wiki/vocab/ciclismo.md`
- Modify: `wiki/vocab/ciclista.md`
- Modify: `wiki/vocab/ciencia-ficción.md`
- Modify: `wiki/vocab/cinco.md`
- Modify: `wiki/vocab/cine.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
caminar.md, caminata.md, camisa.md, camiseta.md, campamento.md, campeón.md, campo.md, canadiense.md, cansado.md, cantar.md, capital.md, cargador.md, cargar.md, carne.md, caro.md, carta.md, cartera.md, casa.md, castillo.md, catedral.md, catorce.md, cebolla.md, celebrar.md, celular.md, cena.md, cenar.md, centro-comercial.md, centro.md, cepillarse.md, cepillo.md, cerca-de.md, cerrar.md, cerveza.md, champán.md, chaqueta.md, charco.md, chef.md, chica.md, chico.md, chicos.md, chile.md, chileno.md, chino.md, chismoso.md, chocolate.md, ciclismo.md, ciclista.md, ciencia-ficción.md, cinco.md, cine.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 4 (caminar–cine)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 4
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 6 begins.

---

## Task 6: Batch 5 — `cita` .. `correo-electrónico` (50 files)

**Files:**
- Modify: `wiki/vocab/cita.md`
- Modify: `wiki/vocab/ciudad.md`
- Modify: `wiki/vocab/claro.md`
- Modify: `wiki/vocab/clase.md`
- Modify: `wiki/vocab/cliente.md`
- Modify: `wiki/vocab/club.md`
- Modify: `wiki/vocab/clásico.md`
- Modify: `wiki/vocab/clínica.md`
- Modify: `wiki/vocab/cocina.md`
- Modify: `wiki/vocab/cocinar.md`
- Modify: `wiki/vocab/colega.md`
- Modify: `wiki/vocab/colegio.md`
- Modify: `wiki/vocab/collar.md`
- Modify: `wiki/vocab/colombiano.md`
- Modify: `wiki/vocab/color.md`
- Modify: `wiki/vocab/comenzar.md`
- Modify: `wiki/vocab/comer.md`
- Modify: `wiki/vocab/comida-rápida.md`
- Modify: `wiki/vocab/comida.md`
- Modify: `wiki/vocab/como-yo.md`
- Modify: `wiki/vocab/compañera-de-trabajo.md`
- Modify: `wiki/vocab/compañero-de-cuarto.md`
- Modify: `wiki/vocab/compañero-de-trabajo.md`
- Modify: `wiki/vocab/compañero.md`
- Modify: `wiki/vocab/competencia.md`
- Modify: `wiki/vocab/competitivo.md`
- Modify: `wiki/vocab/completar.md`
- Modify: `wiki/vocab/completo.md`
- Modify: `wiki/vocab/comprar.md`
- Modify: `wiki/vocab/computadora.md`
- Modify: `wiki/vocab/con-azúcar.md`
- Modify: `wiki/vocab/con-hielo.md`
- Modify: `wiki/vocab/con-leche.md`
- Modify: `wiki/vocab/con-pollo.md`
- Modify: `wiki/vocab/con.md`
- Modify: `wiki/vocab/concierto.md`
- Modify: `wiki/vocab/concurso.md`
- Modify: `wiki/vocab/conductor.md`
- Modify: `wiki/vocab/conexión.md`
- Modify: `wiki/vocab/confiar-en.md`
- Modify: `wiki/vocab/conmigo.md`
- Modify: `wiki/vocab/conocer-a.md`
- Modify: `wiki/vocab/conocer.md`
- Modify: `wiki/vocab/conozco-a.md`
- Modify: `wiki/vocab/contador.md`
- Modify: `wiki/vocab/contento.md`
- Modify: `wiki/vocab/contestar.md`
- Modify: `wiki/vocab/copia.md`
- Modify: `wiki/vocab/corbata.md`
- Modify: `wiki/vocab/correo-electrónico.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
cita.md, ciudad.md, claro.md, clase.md, cliente.md, club.md, clásico.md, clínica.md, cocina.md, cocinar.md, colega.md, colegio.md, collar.md, colombiano.md, color.md, comenzar.md, comer.md, comida-rápida.md, comida.md, como-yo.md, compañera-de-trabajo.md, compañero-de-cuarto.md, compañero-de-trabajo.md, compañero.md, competencia.md, competitivo.md, completar.md, completo.md, comprar.md, computadora.md, con-azúcar.md, con-hielo.md, con-leche.md, con-pollo.md, con.md, concierto.md, concurso.md, conductor.md, conexión.md, confiar-en.md, conmigo.md, conocer-a.md, conocer.md, conozco-a.md, contador.md, contento.md, contestar.md, copia.md, corbata.md, correo-electrónico.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 5 (cita–correo-electrónico)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 5
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 7 begins.

---

## Task 7: Batch 6 — `correr` .. `desconectar` (50 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/correr.md`
- Modify: `wiki/vocab/cosa.md`
- Modify: `wiki/vocab/costa.md`
- Modify: `wiki/vocab/creativo.md`
- Modify: `wiki/vocab/crema.md`
- Modify: `wiki/vocab/creo-que.md`
- Modify: `wiki/vocab/cuaderno.md`
- Modify: `wiki/vocab/cuadra.md`
- Modify: `wiki/vocab/cuarenta.md`
- Modify: `wiki/vocab/cuatro.md`
- Modify: `wiki/vocab/cuenta.md`
- Modify: `wiki/vocab/cumpleaños.md`
- Modify: `wiki/vocab/curso.md`
- Modify: `wiki/vocab/cuál.md`
- Modify: `wiki/vocab/cuáles.md`
- Modify: `wiki/vocab/cuándo.md`
- Modify: `wiki/vocab/cuánta.md`
- Modify: `wiki/vocab/cuántas.md`
- Modify: `wiki/vocab/cuánto-cuesta.md`
- Modify: `wiki/vocab/cuánto-cuestan.md`
- Modify: `wiki/vocab/cuánto.md`
- Modify: `wiki/vocab/cuántos-años.md`
- Modify: `wiki/vocab/cuántos.md`
- Modify: `wiki/vocab/cámara.md`
- Modify: `wiki/vocab/cóctel.md`
- Modify: `wiki/vocab/código-postal.md`
- Modify: `wiki/vocab/cómo-es.md`
- Modify: `wiki/vocab/cómo-estás.md`
- Modify: `wiki/vocab/cómo-te-llamas.md`
- Modify: `wiki/vocab/cómo.md`
- Modify: `wiki/vocab/cómodo.md`
- Modify: `wiki/vocab/de-ahí.md`
- Modify: `wiki/vocab/de-allá.md`
- Modify: `wiki/vocab/de-cumpleaños.md`
- Modify: `wiki/vocab/de-dónde-eres.md`
- Modify: `wiki/vocab/de-nada.md`
- Modify: `wiki/vocab/debajo-de.md`
- Modify: `wiki/vocab/decoración.md`
- Modify: `wiki/vocab/delicioso.md`
- Modify: `wiki/vocab/demasiados.md`
- Modify: `wiki/vocab/dentista.md`
- Modify: `wiki/vocab/depende.md`
- Modify: `wiki/vocab/deporte.md`
- Modify: `wiki/vocab/derecho.md`
- Modify: `wiki/vocab/desafortunadamente.md`
- Modify: `wiki/vocab/desastre.md`
- Modify: `wiki/vocab/desayunar.md`
- Modify: `wiki/vocab/desayuno.md`
- Modify: `wiki/vocab/descansar.md`
- Modify: `wiki/vocab/desconectar.md`
- Delete: `wiki/vocab/coctel.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/coctel.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
correr.md, cosa.md, costa.md, creativo.md, crema.md, creo-que.md, cuaderno.md, cuadra.md, cuarenta.md, cuatro.md, cuenta.md, cumpleaños.md, curso.md, cuál.md, cuáles.md, cuándo.md, cuánta.md, cuántas.md, cuánto-cuesta.md, cuánto-cuestan.md, cuánto.md, cuántos-años.md, cuántos.md, cámara.md, cóctel.md, código-postal.md, cómo-es.md, cómo-estás.md, cómo-te-llamas.md, cómo.md, cómodo.md, de-ahí.md, de-allá.md, de-cumpleaños.md, de-dónde-eres.md, de-nada.md, debajo-de.md, decoración.md, delicioso.md, demasiados.md, dentista.md, depende.md, deporte.md, derecho.md, desafortunadamente.md, desastre.md, desayunar.md, desayuno.md, descansar.md, desconectar.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Distinct word, not a duplicate — `cuándo.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/cuándo.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- **Duplicate pair — `cóctel.md` / `coctel.md`:** `cóctel.md` is the junk file (Category 1). Read the real content from `wiki/vocab/coctel.md` and merge it into `wiki/vocab/cóctel.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/coctel.md`. Then remove the line `- [[coctel]] ...` from `wiki/index.md` (search for the exact line starting with `- [[coctel]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 6 (correr–desconectar)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 6
- 50 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (coctel.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 8 begins.

---

## Task 8: Batch 7 — `desde-hace` .. `dólar` (50 files)

**Files:**
- Modify: `wiki/vocab/desde-hace.md`
- Modify: `wiki/vocab/desierto.md`
- Modify: `wiki/vocab/desodorante.md`
- Modify: `wiki/vocab/despejado.md`
- Modify: `wiki/vocab/despierto.md`
- Modify: `wiki/vocab/después-de.md`
- Modify: `wiki/vocab/después.md`
- Modify: `wiki/vocab/destino.md`
- Modify: `wiki/vocab/detergente.md`
- Modify: `wiki/vocab/diario.md`
- Modify: `wiki/vocab/dibujar.md`
- Modify: `wiki/vocab/diccionario.md`
- Modify: `wiki/vocab/diciembre.md`
- Modify: `wiki/vocab/diecinueve.md`
- Modify: `wiki/vocab/dieciocho.md`
- Modify: `wiki/vocab/diecisiete.md`
- Modify: `wiki/vocab/dieciséis.md`
- Modify: `wiki/vocab/diente.md`
- Modify: `wiki/vocab/dieta.md`
- Modify: `wiki/vocab/diez.md`
- Modify: `wiki/vocab/diferente.md`
- Modify: `wiki/vocab/difícil.md`
- Modify: `wiki/vocab/dinero.md`
- Modify: `wiki/vocab/dirección.md`
- Modify: `wiki/vocab/director.md`
- Modify: `wiki/vocab/discoteca.md`
- Modify: `wiki/vocab/disculpa.md`
- Modify: `wiki/vocab/disculpe.md`
- Modify: `wiki/vocab/disculpen.md`
- Modify: `wiki/vocab/disfrutar.md`
- Modify: `wiki/vocab/divertido.md`
- Modify: `wiki/vocab/diálogo.md`
- Modify: `wiki/vocab/dj.md`
- Modify: `wiki/vocab/doce.md`
- Modify: `wiki/vocab/doctor.md`
- Modify: `wiki/vocab/documento.md`
- Modify: `wiki/vocab/doler.md`
- Modify: `wiki/vocab/dolor-de-estómago.md`
- Modify: `wiki/vocab/dolor.md`
- Modify: `wiki/vocab/domingo.md`
- Modify: `wiki/vocab/dos-veces-por.md`
- Modify: `wiki/vocab/dos.md`
- Modify: `wiki/vocab/ducharse.md`
- Modify: `wiki/vocab/dulce.md`
- Modify: `wiki/vocab/dulces.md`
- Modify: `wiki/vocab/durante.md`
- Modify: `wiki/vocab/duraznos.md`
- Modify: `wiki/vocab/duro.md`
- Modify: `wiki/vocab/día.md`
- Modify: `wiki/vocab/dólar.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
desde-hace.md, desierto.md, desodorante.md, despejado.md, despierto.md, después-de.md, después.md, destino.md, detergente.md, diario.md, dibujar.md, diccionario.md, diciembre.md, diecinueve.md, dieciocho.md, diecisiete.md, dieciséis.md, diente.md, dieta.md, diez.md, diferente.md, difícil.md, dinero.md, dirección.md, director.md, discoteca.md, disculpa.md, disculpe.md, disculpen.md, disfrutar.md, divertido.md, diálogo.md, dj.md, doce.md, doctor.md, documento.md, doler.md, dolor-de-estómago.md, dolor.md, domingo.md, dos-veces-por.md, dos.md, ducharse.md, dulce.md, dulces.md, durante.md, duraznos.md, duro.md, día.md, dólar.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 7 (desde-hace–dólar)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 7
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 9 begins.

---

## Task 9: Batch 8 — `dónde` .. `es` (50 files, 2 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/dónde.md`
- Modify: `wiki/vocab/egoísta.md`
- Modify: `wiki/vocab/ejercicio.md`
- Modify: `wiki/vocab/el-extranjero.md`
- Modify: `wiki/vocab/el.md`
- Modify: `wiki/vocab/elegante.md`
- Modify: `wiki/vocab/ella.md`
- Modify: `wiki/vocab/ellas.md`
- Modify: `wiki/vocab/ellos.md`
- Modify: `wiki/vocab/emergencia.md`
- Modify: `wiki/vocab/emocionado.md`
- Modify: `wiki/vocab/empezar-a.md`
- Modify: `wiki/vocab/empieza.md`
- Modify: `wiki/vocab/empleado.md`
- Modify: `wiki/vocab/empresa.md`
- Modify: `wiki/vocab/en-casa.md`
- Modify: `wiki/vocab/en-coche.md`
- Modify: `wiki/vocab/en-común.md`
- Modify: `wiki/vocab/en-general.md`
- Modify: `wiki/vocab/en-grupo.md`
- Modify: `wiki/vocab/en-línea.md`
- Modify: `wiki/vocab/en-punto.md`
- Modify: `wiki/vocab/en-realidad.md`
- Modify: `wiki/vocab/en-tren.md`
- Modify: `wiki/vocab/en-vez-de.md`
- Modify: `wiki/vocab/encantada.md`
- Modify: `wiki/vocab/encantado.md`
- Modify: `wiki/vocab/encantar.md`
- Modify: `wiki/vocab/enchilada.md`
- Modify: `wiki/vocab/encima-de.md`
- Modify: `wiki/vocab/energía.md`
- Modify: `wiki/vocab/enero.md`
- Modify: `wiki/vocab/enfermedad.md`
- Modify: `wiki/vocab/enfermo.md`
- Modify: `wiki/vocab/enfrente-de.md`
- Modify: `wiki/vocab/enojado.md`
- Modify: `wiki/vocab/enorme.md`
- Modify: `wiki/vocab/ensalada.md`
- Modify: `wiki/vocab/enseñar.md`
- Modify: `wiki/vocab/entonces.md`
- Modify: `wiki/vocab/entrada.md`
- Modify: `wiki/vocab/entre.md`
- Modify: `wiki/vocab/entrenador.md`
- Modify: `wiki/vocab/equipo.md`
- Modify: `wiki/vocab/eres-de.md`
- Modify: `wiki/vocab/es-de.md`
- Modify: `wiki/vocab/es-divertido.md`
- Modify: `wiki/vocab/es-mentira.md`
- Modify: `wiki/vocab/es-verdad.md`
- Modify: `wiki/vocab/es.md`
- Delete: `wiki/vocab/egoista.md`
- Delete: `wiki/vocab/en-comun.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/egoista.md`, `wiki/vocab/en-comun.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
dónde.md, egoísta.md, ejercicio.md, el-extranjero.md, el.md, elegante.md, ella.md, ellas.md, ellos.md, emergencia.md, emocionado.md, empezar-a.md, empieza.md, empleado.md, empresa.md, en-casa.md, en-coche.md, en-común.md, en-general.md, en-grupo.md, en-línea.md, en-punto.md, en-realidad.md, en-tren.md, en-vez-de.md, encantada.md, encantado.md, encantar.md, enchilada.md, encima-de.md, energía.md, enero.md, enfermedad.md, enfermo.md, enfrente-de.md, enojado.md, enorme.md, ensalada.md, enseñar.md, entonces.md, entrada.md, entre.md, entrenador.md, equipo.md, eres-de.md, es-de.md, es-divertido.md, es-mentira.md, es-verdad.md, es.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `egoísta.md` / `egoista.md`:** `egoísta.md` is the junk file (Category 1). Read the real content from `wiki/vocab/egoista.md` and merge it into `wiki/vocab/egoísta.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/egoista.md`. Then remove the line `- [[egoista]] ...` from `wiki/index.md` (search for the exact line starting with `- [[egoista]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Distinct word, not a duplicate — `el.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/el.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- **Duplicate pair — `en-común.md` / `en-comun.md`:** `en-común.md` is the junk file (Category 1). Read the real content from `wiki/vocab/en-comun.md` and merge it into `wiki/vocab/en-común.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/en-comun.md`. Then remove the line `- [[en-comun]] ...` from `wiki/index.md` (search for the exact line starting with `- [[en-comun]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 8 (dónde–es)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 8
- 50 files corrected (type/pattern/example rewritten)
- 2 duplicate files removed (egoista.md, en-comun.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 10 begins.

---

## Task 10: Batch 9 — `escribir` .. `famoso` (50 files)

**Files:**
- Modify: `wiki/vocab/escribir.md`
- Modify: `wiki/vocab/escritor.md`
- Modify: `wiki/vocab/escuchar.md`
- Modify: `wiki/vocab/escuela.md`
- Modify: `wiki/vocab/espacio.md`
- Modify: `wiki/vocab/españa.md`
- Modify: `wiki/vocab/español.md`
- Modify: `wiki/vocab/especia.md`
- Modify: `wiki/vocab/especial.md`
- Modify: `wiki/vocab/especialmente.md`
- Modify: `wiki/vocab/espera.md`
- Modify: `wiki/vocab/esperar-a.md`
- Modify: `wiki/vocab/esperar.md`
- Modify: `wiki/vocab/esposa.md`
- Modify: `wiki/vocab/esquiar.md`
- Modify: `wiki/vocab/estacionamiento.md`
- Modify: `wiki/vocab/estación-de-metro.md`
- Modify: `wiki/vocab/estación-de-tren.md`
- Modify: `wiki/vocab/estación.md`
- Modify: `wiki/vocab/estadounidense.md`
- Modify: `wiki/vocab/estar-de-acuerdo.md`
- Modify: `wiki/vocab/estar-seguro.md`
- Modify: `wiki/vocab/estatua.md`
- Modify: `wiki/vocab/este.md`
- Modify: `wiki/vocab/estrés.md`
- Modify: `wiki/vocab/estudiante.md`
- Modify: `wiki/vocab/estudias.md`
- Modify: `wiki/vocab/estudio.md`
- Modify: `wiki/vocab/está-bien.md`
- Modify: `wiki/vocab/está-bueno.md`
- Modify: `wiki/vocab/está.md`
- Modify: `wiki/vocab/estómago.md`
- Modify: `wiki/vocab/euro.md`
- Modify: `wiki/vocab/evento.md`
- Modify: `wiki/vocab/ex.md`
- Modify: `wiki/vocab/exacto.md`
- Modify: `wiki/vocab/examen-médico.md`
- Modify: `wiki/vocab/examen.md`
- Modify: `wiki/vocab/excelente.md`
- Modify: `wiki/vocab/excusa.md`
- Modify: `wiki/vocab/experiencia.md`
- Modify: `wiki/vocab/explicar.md`
- Modify: `wiki/vocab/explorar.md`
- Modify: `wiki/vocab/exposición.md`
- Modify: `wiki/vocab/extranjero.md`
- Modify: `wiki/vocab/extraño.md`
- Modify: `wiki/vocab/exótico.md`
- Modify: `wiki/vocab/falda.md`
- Modify: `wiki/vocab/familia.md`
- Modify: `wiki/vocab/famoso.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
escribir.md, escritor.md, escuchar.md, escuela.md, espacio.md, españa.md, español.md, especia.md, especial.md, especialmente.md, espera.md, esperar-a.md, esperar.md, esposa.md, esquiar.md, estacionamiento.md, estación-de-metro.md, estación-de-tren.md, estación.md, estadounidense.md, estar-de-acuerdo.md, estar-seguro.md, estatua.md, este.md, estrés.md, estudiante.md, estudias.md, estudio.md, está-bien.md, está-bueno.md, está.md, estómago.md, euro.md, evento.md, ex.md, exacto.md, examen-médico.md, examen.md, excelente.md, excusa.md, experiencia.md, explicar.md, explorar.md, exposición.md, extranjero.md, extraño.md, exótico.md, falda.md, familia.md, famoso.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 9 (escribir–famoso)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 9
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 11 begins.

---

## Task 11: Batch 10 — `fantasía` .. `grande` (50 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/fantasía.md`
- Modify: `wiki/vocab/fantástico.md`
- Modify: `wiki/vocab/farmacia.md`
- Modify: `wiki/vocab/favorito.md`
- Modify: `wiki/vocab/febrero.md`
- Modify: `wiki/vocab/fecha-de-entrega.md`
- Modify: `wiki/vocab/felicidad.md`
- Modify: `wiki/vocab/feliz-cumpleaños.md`
- Modify: `wiki/vocab/feliz.md`
- Modify: `wiki/vocab/feo.md`
- Modify: `wiki/vocab/feria.md`
- Modify: `wiki/vocab/festival.md`
- Modify: `wiki/vocab/fiesta.md`
- Modify: `wiki/vocab/fin-de-semana.md`
- Modify: `wiki/vocab/final.md`
- Modify: `wiki/vocab/finalmente.md`
- Modify: `wiki/vocab/firma.md`
- Modify: `wiki/vocab/flaco.md`
- Modify: `wiki/vocab/flamenco.md`
- Modify: `wiki/vocab/foto.md`
- Modify: `wiki/vocab/fotografía.md`
- Modify: `wiki/vocab/fotógrafo.md`
- Modify: `wiki/vocab/francia.md`
- Modify: `wiki/vocab/francés.md`
- Modify: `wiki/vocab/frecuentemente.md`
- Modify: `wiki/vocab/frijol.md`
- Modify: `wiki/vocab/frito.md`
- Modify: `wiki/vocab/fruta.md`
- Modify: `wiki/vocab/frío.md`
- Modify: `wiki/vocab/fuente.md`
- Modify: `wiki/vocab/fuera.md`
- Modify: `wiki/vocab/fumar.md`
- Modify: `wiki/vocab/fábrica.md`
- Modify: `wiki/vocab/fácil.md`
- Modify: `wiki/vocab/físico.md`
- Modify: `wiki/vocab/fútbol.md`
- Modify: `wiki/vocab/gato.md`
- Modify: `wiki/vocab/generalmente.md`
- Modify: `wiki/vocab/genial.md`
- Modify: `wiki/vocab/gente.md`
- Modify: `wiki/vocab/geografía.md`
- Modify: `wiki/vocab/gerente.md`
- Modify: `wiki/vocab/gimnasia.md`
- Modify: `wiki/vocab/gimnasio.md`
- Modify: `wiki/vocab/golf.md`
- Modify: `wiki/vocab/gorra.md`
- Modify: `wiki/vocab/gracias-por.md`
- Modify: `wiki/vocab/gracias.md`
- Modify: `wiki/vocab/graciosa.md`
- Modify: `wiki/vocab/grande.md`
- Delete: `wiki/vocab/fisico.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/fisico.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
fantasía.md, fantástico.md, farmacia.md, favorito.md, febrero.md, fecha-de-entrega.md, felicidad.md, feliz-cumpleaños.md, feliz.md, feo.md, feria.md, festival.md, fiesta.md, fin-de-semana.md, final.md, finalmente.md, firma.md, flaco.md, flamenco.md, foto.md, fotografía.md, fotógrafo.md, francia.md, francés.md, frecuentemente.md, frijol.md, frito.md, fruta.md, frío.md, fuente.md, fuera.md, fumar.md, fábrica.md, fácil.md, físico.md, fútbol.md, gato.md, generalmente.md, genial.md, gente.md, geografía.md, gerente.md, gimnasia.md, gimnasio.md, golf.md, gorra.md, gracias-por.md, gracias.md, graciosa.md, grande.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `físico.md` / `fisico.md`:** `físico.md` is the junk file (Category 1). Read the real content from `wiki/vocab/fisico.md` and merge it into `wiki/vocab/físico.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/fisico.md`. Then remove the line `- [[fisico]] ...` from `wiki/index.md` (search for the exact line starting with `- [[fisico]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 10 (fantasía–grande)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 10
- 50 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (fisico.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 12 begins.

---

## Task 12: Batch 11 — `gris` .. `incómodo` (50 files)

**Files:**
- Modify: `wiki/vocab/gris.md`
- Modify: `wiki/vocab/guapo.md`
- Modify: `wiki/vocab/guau.md`
- Modify: `wiki/vocab/guitarra.md`
- Modify: `wiki/vocab/hablar.md`
- Modify: `wiki/vocab/hablas.md`
- Modify: `wiki/vocab/hace-sol.md`
- Modify: `wiki/vocab/hace.md`
- Modify: `wiki/vocab/hacer-ejercicio.md`
- Modify: `wiki/vocab/hacer-fila.md`
- Modify: `wiki/vocab/hacer-la-compra.md`
- Modify: `wiki/vocab/hacer-las-maletas.md`
- Modify: `wiki/vocab/hacer-un-viaje.md`
- Modify: `wiki/vocab/hacer-una-fiesta.md`
- Modify: `wiki/vocab/hamburguesa.md`
- Modify: `wiki/vocab/hasta-luego.md`
- Modify: `wiki/vocab/hasta-pronto.md`
- Modify: `wiki/vocab/hasta.md`
- Modify: `wiki/vocab/hay-que.md`
- Modify: `wiki/vocab/hay.md`
- Modify: `wiki/vocab/helado.md`
- Modify: `wiki/vocab/hermana.md`
- Modify: `wiki/vocab/hermano.md`
- Modify: `wiki/vocab/hermanos.md`
- Modify: `wiki/vocab/hermoso.md`
- Modify: `wiki/vocab/hielo.md`
- Modify: `wiki/vocab/hija.md`
- Modify: `wiki/vocab/hijo.md`
- Modify: `wiki/vocab/hijos.md`
- Modify: `wiki/vocab/historia.md`
- Modify: `wiki/vocab/hockey.md`
- Modify: `wiki/vocab/hola.md`
- Modify: `wiki/vocab/hombre.md`
- Modify: `wiki/vocab/honestamente.md`
- Modify: `wiki/vocab/hora.md`
- Modify: `wiki/vocab/horario.md`
- Modify: `wiki/vocab/horrible.md`
- Modify: `wiki/vocab/hospital.md`
- Modify: `wiki/vocab/hotel.md`
- Modify: `wiki/vocab/hoy.md`
- Modify: `wiki/vocab/huevo.md`
- Modify: `wiki/vocab/idea.md`
- Modify: `wiki/vocab/identificación.md`
- Modify: `wiki/vocab/idioma.md`
- Modify: `wiki/vocab/iglesia.md`
- Modify: `wiki/vocab/impaciente.md`
- Modify: `wiki/vocab/importante.md`
- Modify: `wiki/vocab/incorrecto.md`
- Modify: `wiki/vocab/increíble.md`
- Modify: `wiki/vocab/incómodo.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
gris.md, guapo.md, guau.md, guitarra.md, hablar.md, hablas.md, hace-sol.md, hace.md, hacer-ejercicio.md, hacer-fila.md, hacer-la-compra.md, hacer-las-maletas.md, hacer-un-viaje.md, hacer-una-fiesta.md, hamburguesa.md, hasta-luego.md, hasta-pronto.md, hasta.md, hay-que.md, hay.md, helado.md, hermana.md, hermano.md, hermanos.md, hermoso.md, hielo.md, hija.md, hijo.md, hijos.md, historia.md, hockey.md, hola.md, hombre.md, honestamente.md, hora.md, horario.md, horrible.md, hospital.md, hotel.md, hoy.md, huevo.md, idea.md, identificación.md, idioma.md, iglesia.md, impaciente.md, importante.md, incorrecto.md, increíble.md, incómodo.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 11 (gris–incómodo)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 11
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 13 begins.

---

## Task 13: Batch 12 — `información` .. `lavarse` (50 files)

**Files:**
- Modify: `wiki/vocab/información.md`
- Modify: `wiki/vocab/infusión.md`
- Modify: `wiki/vocab/ingeniero.md`
- Modify: `wiki/vocab/inglés.md`
- Modify: `wiki/vocab/ingrediente.md`
- Modify: `wiki/vocab/insecto.md`
- Modify: `wiki/vocab/instrucción.md`
- Modify: `wiki/vocab/instructor.md`
- Modify: `wiki/vocab/instrumento.md`
- Modify: `wiki/vocab/inteligente.md`
- Modify: `wiki/vocab/interesante.md`
- Modify: `wiki/vocab/internet.md`
- Modify: `wiki/vocab/introvertido.md`
- Modify: `wiki/vocab/invierno.md`
- Modify: `wiki/vocab/invitación.md`
- Modify: `wiki/vocab/invitado.md`
- Modify: `wiki/vocab/invitar-a.md`
- Modify: `wiki/vocab/ir-a.md`
- Modify: `wiki/vocab/isla.md`
- Modify: `wiki/vocab/italiano.md`
- Modify: `wiki/vocab/izquierdo.md`
- Modify: `wiki/vocab/japonés.md`
- Modify: `wiki/vocab/jardín.md`
- Modify: `wiki/vocab/jeans.md`
- Modify: `wiki/vocab/jefa.md`
- Modify: `wiki/vocab/jefe.md`
- Modify: `wiki/vocab/joven.md`
- Modify: `wiki/vocab/juego.md`
- Modify: `wiki/vocab/jueves.md`
- Modify: `wiki/vocab/jugador.md`
- Modify: `wiki/vocab/jugar-a.md`
- Modify: `wiki/vocab/jugar.md`
- Modify: `wiki/vocab/jugo.md`
- Modify: `wiki/vocab/juguete.md`
- Modify: `wiki/vocab/julio.md`
- Modify: `wiki/vocab/junio.md`
- Modify: `wiki/vocab/juntos.md`
- Modify: `wiki/vocab/karaoke.md`
- Modify: `wiki/vocab/karate.md`
- Modify: `wiki/vocab/kilo-de.md`
- Modify: `wiki/vocab/kilo.md`
- Modify: `wiki/vocab/kilos-de.md`
- Modify: `wiki/vocab/kilómetro.md`
- Modify: `wiki/vocab/la.md`
- Modify: `wiki/vocab/lago.md`
- Modify: `wiki/vocab/lamentablemente.md`
- Modify: `wiki/vocab/las.md`
- Modify: `wiki/vocab/lavadora.md`
- Modify: `wiki/vocab/lavar.md`
- Modify: `wiki/vocab/lavarse.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
información.md, infusión.md, ingeniero.md, inglés.md, ingrediente.md, insecto.md, instrucción.md, instructor.md, instrumento.md, inteligente.md, interesante.md, internet.md, introvertido.md, invierno.md, invitación.md, invitado.md, invitar-a.md, ir-a.md, isla.md, italiano.md, izquierdo.md, japonés.md, jardín.md, jeans.md, jefa.md, jefe.md, joven.md, juego.md, jueves.md, jugador.md, jugar-a.md, jugar.md, jugo.md, juguete.md, julio.md, junio.md, juntos.md, karaoke.md, karate.md, kilo-de.md, kilo.md, kilos-de.md, kilómetro.md, la.md, lago.md, lamentablemente.md, las.md, lavadora.md, lavar.md, lavarse.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 12 (información–lavarse)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 12
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 14 begins.

---

## Task 14: Batch 13 — `lección` .. `mayo` (50 files)

**Files:**
- Modify: `wiki/vocab/lección.md`
- Modify: `wiki/vocab/leche.md`
- Modify: `wiki/vocab/lechuga.md`
- Modify: `wiki/vocab/leer.md`
- Modify: `wiki/vocab/lejos-de.md`
- Modify: `wiki/vocab/levantarse.md`
- Modify: `wiki/vocab/libre.md`
- Modify: `wiki/vocab/librería.md`
- Modify: `wiki/vocab/libro.md`
- Modify: `wiki/vocab/lima.md`
- Modify: `wiki/vocab/limonada.md`
- Modify: `wiki/vocab/limpio.md`
- Modify: `wiki/vocab/limón.md`
- Modify: `wiki/vocab/lista.md`
- Modify: `wiki/vocab/listo.md`
- Modify: `wiki/vocab/literatura.md`
- Modify: `wiki/vocab/litro.md`
- Modify: `wiki/vocab/llamar-a.md`
- Modify: `wiki/vocab/llamarse.md`
- Modify: `wiki/vocab/llave.md`
- Modify: `wiki/vocab/llover.md`
- Modify: `wiki/vocab/lluvia.md`
- Modify: `wiki/vocab/lo-siento.md`
- Modify: `wiki/vocab/los.md`
- Modify: `wiki/vocab/luego.md`
- Modify: `wiki/vocab/lugar.md`
- Modify: `wiki/vocab/lunes.md`
- Modify: `wiki/vocab/lámpara.md`
- Modify: `wiki/vocab/lápiz.md`
- Modify: `wiki/vocab/madre.md`
- Modify: `wiki/vocab/maestro.md`
- Modify: `wiki/vocab/magnífico.md`
- Modify: `wiki/vocab/mal.md`
- Modify: `wiki/vocab/maleta.md`
- Modify: `wiki/vocab/malo.md`
- Modify: `wiki/vocab/mamá.md`
- Modify: `wiki/vocab/manejar.md`
- Modify: `wiki/vocab/mango.md`
- Modify: `wiki/vocab/mangos.md`
- Modify: `wiki/vocab/mano.md`
- Modify: `wiki/vocab/manzana.md`
- Modify: `wiki/vocab/mapa.md`
- Modify: `wiki/vocab/mar.md`
- Modify: `wiki/vocab/marca.md`
- Modify: `wiki/vocab/marrón.md`
- Modify: `wiki/vocab/martes.md`
- Modify: `wiki/vocab/marzo.md`
- Modify: `wiki/vocab/mascota.md`
- Modify: `wiki/vocab/matemáticas.md`
- Modify: `wiki/vocab/mayo.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
lección.md, leche.md, lechuga.md, leer.md, lejos-de.md, levantarse.md, libre.md, librería.md, libro.md, lima.md, limonada.md, limpio.md, limón.md, lista.md, listo.md, literatura.md, litro.md, llamar-a.md, llamarse.md, llave.md, llover.md, lluvia.md, lo-siento.md, los.md, luego.md, lugar.md, lunes.md, lámpara.md, lápiz.md, madre.md, maestro.md, magnífico.md, mal.md, maleta.md, malo.md, mamá.md, manejar.md, mango.md, mangos.md, mano.md, manzana.md, mapa.md, mar.md, marca.md, marrón.md, martes.md, marzo.md, mascota.md, matemáticas.md, mayo.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 13 (lección–mayo)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 13
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 15 begins.

---

## Task 15: Batch 14 — `mayonesa` .. `muy` (50 files)

**Files:**
- Modify: `wiki/vocab/mayonesa.md`
- Modify: `wiki/vocab/maíz.md`
- Modify: `wiki/vocab/mañana.md`
- Modify: `wiki/vocab/me-alegro.md`
- Modify: `wiki/vocab/me-puede-ayudar.md`
- Modify: `wiki/vocab/media.md`
- Modify: `wiki/vocab/medianoche.md`
- Modify: `wiki/vocab/medicina.md`
- Modify: `wiki/vocab/medio.md`
- Modify: `wiki/vocab/mejor-amigo.md`
- Modify: `wiki/vocab/menos.md`
- Modify: `wiki/vocab/mensaje.md`
- Modify: `wiki/vocab/mercado.md`
- Modify: `wiki/vocab/mercados.md`
- Modify: `wiki/vocab/merienda.md`
- Modify: `wiki/vocab/mermelada.md`
- Modify: `wiki/vocab/mes.md`
- Modify: `wiki/vocab/mesa.md`
- Modify: `wiki/vocab/mesero.md`
- Modify: `wiki/vocab/metro.md`
- Modify: `wiki/vocab/mexicano.md`
- Modify: `wiki/vocab/mi-mejor-amiga.md`
- Modify: `wiki/vocab/mi-mejor-amigo.md`
- Modify: `wiki/vocab/mi.md`
- Modify: `wiki/vocab/mientras.md`
- Modify: `wiki/vocab/mil.md`
- Modify: `wiki/vocab/minuto.md`
- Modify: `wiki/vocab/mirar.md`
- Modify: `wiki/vocab/mismo.md`
- Modify: `wiki/vocab/miércoles.md`
- Modify: `wiki/vocab/moderno.md`
- Modify: `wiki/vocab/moneda.md`
- Modify: `wiki/vocab/montar-en-bicicleta.md`
- Modify: `wiki/vocab/montaña.md`
- Modify: `wiki/vocab/monumento.md`
- Modify: `wiki/vocab/morado.md`
- Modify: `wiki/vocab/moreno.md`
- Modify: `wiki/vocab/mosquito.md`
- Modify: `wiki/vocab/mostrar.md`
- Modify: `wiki/vocab/moto.md`
- Modify: `wiki/vocab/muchas-gracias.md`
- Modify: `wiki/vocab/mucho-gusto.md`
- Modify: `wiki/vocab/mucho.md`
- Modify: `wiki/vocab/muchos.md`
- Modify: `wiki/vocab/mujer.md`
- Modify: `wiki/vocab/multinacional.md`
- Modify: `wiki/vocab/museo.md`
- Modify: `wiki/vocab/musical.md`
- Modify: `wiki/vocab/muy-bien.md`
- Modify: `wiki/vocab/muy.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
mayonesa.md, maíz.md, mañana.md, me-alegro.md, me-puede-ayudar.md, media.md, medianoche.md, medicina.md, medio.md, mejor-amigo.md, menos.md, mensaje.md, mercado.md, mercados.md, merienda.md, mermelada.md, mes.md, mesa.md, mesero.md, metro.md, mexicano.md, mi-mejor-amiga.md, mi-mejor-amigo.md, mi.md, mientras.md, mil.md, minuto.md, mirar.md, mismo.md, miércoles.md, moderno.md, moneda.md, montar-en-bicicleta.md, montaña.md, monumento.md, morado.md, moreno.md, mosquito.md, mostrar.md, moto.md, muchas-gracias.md, mucho-gusto.md, mucho.md, muchos.md, mujer.md, multinacional.md, museo.md, musical.md, muy-bien.md, muy.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 14 (mayonesa–muy)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 14
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 16 begins.

---

## Task 16: Batch 15 — `más-de` .. `nuestra` (50 files)

**Files:**
- Modify: `wiki/vocab/más-de.md`
- Modify: `wiki/vocab/más-o-menos.md`
- Modify: `wiki/vocab/más.md`
- Modify: `wiki/vocab/médico.md`
- Modify: `wiki/vocab/música-en-vivo.md`
- Modify: `wiki/vocab/música.md`
- Modify: `wiki/vocab/músico.md`
- Modify: `wiki/vocab/nada.md`
- Modify: `wiki/vocab/nadar.md`
- Modify: `wiki/vocab/nadie.md`
- Modify: `wiki/vocab/naranja.md`
- Modify: `wiki/vocab/naranjas.md`
- Modify: `wiki/vocab/natación.md`
- Modify: `wiki/vocab/naturaleza.md`
- Modify: `wiki/vocab/navegar.md`
- Modify: `wiki/vocab/necesario.md`
- Modify: `wiki/vocab/necesitar.md`
- Modify: `wiki/vocab/necesitas.md`
- Modify: `wiki/vocab/necesito.md`
- Modify: `wiki/vocab/negativo.md`
- Modify: `wiki/vocab/negocio.md`
- Modify: `wiki/vocab/negro.md`
- Modify: `wiki/vocab/nervioso.md`
- Modify: `wiki/vocab/nevar.md`
- Modify: `wiki/vocab/ni-idea.md`
- Modify: `wiki/vocab/nieve.md`
- Modify: `wiki/vocab/ninguna.md`
- Modify: `wiki/vocab/ningún.md`
- Modify: `wiki/vocab/nivel.md`
- Modify: `wiki/vocab/no-crees.md`
- Modify: `wiki/vocab/no-encuentro.md`
- Modify: `wiki/vocab/no-entiendo.md`
- Modify: `wiki/vocab/no-hace.md`
- Modify: `wiki/vocab/no-hay.md`
- Modify: `wiki/vocab/no-importa.md`
- Modify: `wiki/vocab/no-sé.md`
- Modify: `wiki/vocab/no.md`
- Modify: `wiki/vocab/noche.md`
- Modify: `wiki/vocab/nombre.md`
- Modify: `wiki/vocab/normal.md`
- Modify: `wiki/vocab/normalmente.md`
- Modify: `wiki/vocab/nosotras.md`
- Modify: `wiki/vocab/nosotros.md`
- Modify: `wiki/vocab/nota.md`
- Modify: `wiki/vocab/novela.md`
- Modify: `wiki/vocab/novia.md`
- Modify: `wiki/vocab/noviembre.md`
- Modify: `wiki/vocab/novio.md`
- Modify: `wiki/vocab/nublado.md`
- Modify: `wiki/vocab/nuestra.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
más-de.md, más-o-menos.md, más.md, médico.md, música-en-vivo.md, música.md, músico.md, nada.md, nadar.md, nadie.md, naranja.md, naranjas.md, natación.md, naturaleza.md, navegar.md, necesario.md, necesitar.md, necesitas.md, necesito.md, negativo.md, negocio.md, negro.md, nervioso.md, nevar.md, ni-idea.md, nieve.md, ninguna.md, ningún.md, nivel.md, no-crees.md, no-encuentro.md, no-entiendo.md, no-hace.md, no-hay.md, no-importa.md, no-sé.md, no.md, noche.md, nombre.md, normal.md, normalmente.md, nosotras.md, nosotros.md, nota.md, novela.md, novia.md, noviembre.md, novio.md, nublado.md, nuestra.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 15 (más-de–nuestra)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 15
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 17 begins.

---

## Task 17: Batch 16 — `nuestras` .. `pastilla` (50 files)

**Files:**
- Modify: `wiki/vocab/nuestras.md`
- Modify: `wiki/vocab/nuestro.md`
- Modify: `wiki/vocab/nuestros.md`
- Modify: `wiki/vocab/nueve.md`
- Modify: `wiki/vocab/nuevo.md`
- Modify: `wiki/vocab/nunca.md`
- Modify: `wiki/vocab/número.md`
- Modify: `wiki/vocab/o.md`
- Modify: `wiki/vocab/ocho.md`
- Modify: `wiki/vocab/octubre.md`
- Modify: `wiki/vocab/ocupado.md`
- Modify: `wiki/vocab/oficina-de-correos.md`
- Modify: `wiki/vocab/oficina-de-información.md`
- Modify: `wiki/vocab/oficina.md`
- Modify: `wiki/vocab/ojo.md`
- Modify: `wiki/vocab/once.md`
- Modify: `wiki/vocab/opinión.md`
- Modify: `wiki/vocab/optimista.md`
- Modify: `wiki/vocab/ordenar.md`
- Modify: `wiki/vocab/organizar.md`
- Modify: `wiki/vocab/orgánico.md`
- Modify: `wiki/vocab/original.md`
- Modify: `wiki/vocab/otoño.md`
- Modify: `wiki/vocab/otra-vez.md`
- Modify: `wiki/vocab/oye.md`
- Modify: `wiki/vocab/paciente.md`
- Modify: `wiki/vocab/padre.md`
- Modify: `wiki/vocab/padres.md`
- Modify: `wiki/vocab/paella.md`
- Modify: `wiki/vocab/pagar.md`
- Modify: `wiki/vocab/pan.md`
- Modify: `wiki/vocab/panameño.md`
- Modify: `wiki/vocab/pantalla.md`
- Modify: `wiki/vocab/pantalones.md`
- Modify: `wiki/vocab/papa.md`
- Modify: `wiki/vocab/papel.md`
- Modify: `wiki/vocab/papá.md`
- Modify: `wiki/vocab/parada-de-taxi.md`
- Modify: `wiki/vocab/parece-que.md`
- Modify: `wiki/vocab/pareja.md`
- Modify: `wiki/vocab/parque.md`
- Modify: `wiki/vocab/parques.md`
- Modify: `wiki/vocab/participar.md`
- Modify: `wiki/vocab/partido.md`
- Modify: `wiki/vocab/pasaporte.md`
- Modify: `wiki/vocab/pasar.md`
- Modify: `wiki/vocab/pasatiempo.md`
- Modify: `wiki/vocab/pasta.md`
- Modify: `wiki/vocab/pastel.md`
- Modify: `wiki/vocab/pastilla.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
nuestras.md, nuestro.md, nuestros.md, nueve.md, nuevo.md, nunca.md, número.md, o.md, ocho.md, octubre.md, ocupado.md, oficina-de-correos.md, oficina-de-información.md, oficina.md, ojo.md, once.md, opinión.md, optimista.md, ordenar.md, organizar.md, orgánico.md, original.md, otoño.md, otra-vez.md, oye.md, paciente.md, padre.md, padres.md, paella.md, pagar.md, pan.md, panameño.md, pantalla.md, pantalones.md, papa.md, papel.md, papá.md, parada-de-taxi.md, parece-que.md, pareja.md, parque.md, parques.md, participar.md, partido.md, pasaporte.md, pasar.md, pasatiempo.md, pasta.md, pastel.md, pastilla.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Distinct word, not a duplicate — `papa.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/papa.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- **Distinct word, not a duplicate — `papá.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/papá.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 16 (nuestras–pastilla)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 16
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 18 begins.

---

## Task 18: Batch 17 — `patinar` .. `pollo` (50 files, 2 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/patinar.md`
- Modify: `wiki/vocab/patineta.md`
- Modify: `wiki/vocab/patio.md`
- Modify: `wiki/vocab/país.md`
- Modify: `wiki/vocab/pañuelo.md`
- Modify: `wiki/vocab/peinarse.md`
- Modify: `wiki/vocab/peligroso.md`
- Modify: `wiki/vocab/pelirrojo.md`
- Modify: `wiki/vocab/peluquería.md`
- Modify: `wiki/vocab/película.md`
- Modify: `wiki/vocab/pequeño.md`
- Modify: `wiki/vocab/pera.md`
- Modify: `wiki/vocab/perdido.md`
- Modify: `wiki/vocab/perdona.md`
- Modify: `wiki/vocab/perdone.md`
- Modify: `wiki/vocab/perdón.md`
- Modify: `wiki/vocab/perezoso.md`
- Modify: `wiki/vocab/perfecto.md`
- Modify: `wiki/vocab/pero.md`
- Modify: `wiki/vocab/perro.md`
- Modify: `wiki/vocab/persona.md`
- Modify: `wiki/vocab/personaje.md`
- Modify: `wiki/vocab/peruano.md`
- Modify: `wiki/vocab/pesado.md`
- Modify: `wiki/vocab/pescado.md`
- Modify: `wiki/vocab/pescar.md`
- Modify: `wiki/vocab/peso.md`
- Modify: `wiki/vocab/pez.md`
- Modify: `wiki/vocab/piano.md`
- Modify: `wiki/vocab/pilates.md`
- Modify: `wiki/vocab/pimienta.md`
- Modify: `wiki/vocab/pimiento.md`
- Modify: `wiki/vocab/pingüino.md`
- Modify: `wiki/vocab/pintar.md`
- Modify: `wiki/vocab/piscina.md`
- Modify: `wiki/vocab/pista-de-baile.md`
- Modify: `wiki/vocab/pizza.md`
- Modify: `wiki/vocab/pizzería.md`
- Modify: `wiki/vocab/piña.md`
- Modify: `wiki/vocab/piñas.md`
- Modify: `wiki/vocab/plan.md`
- Modify: `wiki/vocab/planta.md`
- Modify: `wiki/vocab/plato.md`
- Modify: `wiki/vocab/playa.md`
- Modify: `wiki/vocab/plaza.md`
- Modify: `wiki/vocab/plátano.md`
- Modify: `wiki/vocab/pocos.md`
- Modify: `wiki/vocab/poema.md`
- Modify: `wiki/vocab/poesía.md`
- Modify: `wiki/vocab/pollo.md`
- Delete: `wiki/vocab/peluqueria.md`
- Delete: `wiki/vocab/pina.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/peluqueria.md`, `wiki/vocab/pina.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
patinar.md, patineta.md, patio.md, país.md, pañuelo.md, peinarse.md, peligroso.md, pelirrojo.md, peluquería.md, película.md, pequeño.md, pera.md, perdido.md, perdona.md, perdone.md, perdón.md, perezoso.md, perfecto.md, pero.md, perro.md, persona.md, personaje.md, peruano.md, pesado.md, pescado.md, pescar.md, peso.md, pez.md, piano.md, pilates.md, pimienta.md, pimiento.md, pingüino.md, pintar.md, piscina.md, pista-de-baile.md, pizza.md, pizzería.md, piña.md, piñas.md, plan.md, planta.md, plato.md, playa.md, plaza.md, plátano.md, pocos.md, poema.md, poesía.md, pollo.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `peluquería.md` / `peluqueria.md`:** `peluquería.md` is the junk file (Category 1). Read the real content from `wiki/vocab/peluqueria.md` and merge it into `wiki/vocab/peluquería.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/peluqueria.md`. Then remove the line `- [[peluqueria]] ...` from `wiki/index.md` (search for the exact line starting with `- [[peluqueria]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Duplicate pair — `piña.md` / `pina.md`:** `piña.md` is the junk file (Category 1). Read the real content from `wiki/vocab/pina.md` and merge it into `wiki/vocab/piña.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/pina.md`. Then remove the line `- [[pina]] ...` from `wiki/index.md` (search for the exact line starting with `- [[pina]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 17 (patinar–pollo)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 17
- 50 files corrected (type/pattern/example rewritten)
- 2 duplicate files removed (peluqueria.md, pina.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 19 begins.

---

## Task 19: Batch 18 — `pop` .. `quiere` (50 files)

**Files:**
- Modify: `wiki/vocab/pop.md`
- Modify: `wiki/vocab/popular.md`
- Modify: `wiki/vocab/por-allí.md`
- Modify: `wiki/vocab/por-aquí.md`
- Modify: `wiki/vocab/por-ejemplo.md`
- Modify: `wiki/vocab/por-eso.md`
- Modify: `wiki/vocab/por-favor.md`
- Modify: `wiki/vocab/por-la-mañana.md`
- Modify: `wiki/vocab/por-la-noche.md`
- Modify: `wiki/vocab/por-la.md`
- Modify: `wiki/vocab/por-qué.md`
- Modify: `wiki/vocab/porque.md`
- Modify: `wiki/vocab/portugués.md`
- Modify: `wiki/vocab/postal.md`
- Modify: `wiki/vocab/postre.md`
- Modify: `wiki/vocab/practicar.md`
- Modify: `wiki/vocab/precio.md`
- Modify: `wiki/vocab/pregunta.md`
- Modify: `wiki/vocab/preocupado.md`
- Modify: `wiki/vocab/preocuparse.md`
- Modify: `wiki/vocab/preparar.md`
- Modify: `wiki/vocab/presentación.md`
- Modify: `wiki/vocab/presionar.md`
- Modify: `wiki/vocab/prima.md`
- Modify: `wiki/vocab/primavera.md`
- Modify: `wiki/vocab/primero.md`
- Modify: `wiki/vocab/primo.md`
- Modify: `wiki/vocab/principal.md`
- Modify: `wiki/vocab/problema.md`
- Modify: `wiki/vocab/producto.md`
- Modify: `wiki/vocab/profesional.md`
- Modify: `wiki/vocab/profesor.md`
- Modify: `wiki/vocab/programa.md`
- Modify: `wiki/vocab/pronto.md`
- Modify: `wiki/vocab/protagonista.md`
- Modify: `wiki/vocab/proyecto.md`
- Modify: `wiki/vocab/próximo.md`
- Modify: `wiki/vocab/pueblo.md`
- Modify: `wiki/vocab/puerta.md`
- Modify: `wiki/vocab/puerto.md`
- Modify: `wiki/vocab/página-web.md`
- Modify: `wiki/vocab/pájaro.md`
- Modify: `wiki/vocab/pódcast.md`
- Modify: `wiki/vocab/que-viene.md`
- Modify: `wiki/vocab/quedarse-dormido.md`
- Modify: `wiki/vocab/quedarse.md`
- Modify: `wiki/vocab/quejarse.md`
- Modify: `wiki/vocab/querido.md`
- Modify: `wiki/vocab/queso.md`
- Modify: `wiki/vocab/quiere.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
pop.md, popular.md, por-allí.md, por-aquí.md, por-ejemplo.md, por-eso.md, por-favor.md, por-la-mañana.md, por-la-noche.md, por-la.md, por-qué.md, porque.md, portugués.md, postal.md, postre.md, practicar.md, precio.md, pregunta.md, preocupado.md, preocuparse.md, preparar.md, presentación.md, presionar.md, prima.md, primavera.md, primero.md, primo.md, principal.md, problema.md, producto.md, profesional.md, profesor.md, programa.md, pronto.md, protagonista.md, proyecto.md, próximo.md, pueblo.md, puerta.md, puerto.md, página-web.md, pájaro.md, pódcast.md, que-viene.md, quedarse-dormido.md, quedarse.md, quejarse.md, querido.md, queso.md, quiere.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 18 (pop–quiere)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 18
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 20 begins.

---

## Task 20: Batch 19 — `quieres` .. `romántico` (50 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/quieres.md`
- Modify: `wiki/vocab/quiero.md`
- Modify: `wiki/vocab/quince.md`
- Modify: `wiki/vocab/quién.md`
- Modify: `wiki/vocab/quiénes.md`
- Modify: `wiki/vocab/qué-alivio.md`
- Modify: `wiki/vocab/qué-bien.md`
- Modify: `wiki/vocab/qué-emoción.md`
- Modify: `wiki/vocab/qué-haces.md`
- Modify: `wiki/vocab/qué-interesante.md`
- Modify: `wiki/vocab/qué-lástima.md`
- Modify: `wiki/vocab/qué-mala-suerte.md`
- Modify: `wiki/vocab/qué-pena.md`
- Modify: `wiki/vocab/qué-suerte.md`
- Modify: `wiki/vocab/qué-tal.md`
- Modify: `wiki/vocab/qué-tiempo-hace.md`
- Modify: `wiki/vocab/qué-tonto.md`
- Modify: `wiki/vocab/química.md`
- Modify: `wiki/vocab/raqueta.md`
- Modify: `wiki/vocab/receta.md`
- Modify: `wiki/vocab/recibir.md`
- Modify: `wiki/vocab/recital.md`
- Modify: `wiki/vocab/recoger.md`
- Modify: `wiki/vocab/recomendar.md`
- Modify: `wiki/vocab/red-social.md`
- Modify: `wiki/vocab/refresco.md`
- Modify: `wiki/vocab/regalo.md`
- Modify: `wiki/vocab/regla.md`
- Modify: `wiki/vocab/regresar.md`
- Modify: `wiki/vocab/relajado.md`
- Modify: `wiki/vocab/relajante.md`
- Modify: `wiki/vocab/relajarse.md`
- Modify: `wiki/vocab/rellenar.md`
- Modify: `wiki/vocab/reloj.md`
- Modify: `wiki/vocab/reparar.md`
- Modify: `wiki/vocab/reserva.md`
- Modify: `wiki/vocab/reservar.md`
- Modify: `wiki/vocab/resolver.md`
- Modify: `wiki/vocab/responder.md`
- Modify: `wiki/vocab/responsable.md`
- Modify: `wiki/vocab/respuesta.md`
- Modify: `wiki/vocab/restaurante.md`
- Modify: `wiki/vocab/retrasado.md`
- Modify: `wiki/vocab/reunión.md`
- Modify: `wiki/vocab/rico.md`
- Modify: `wiki/vocab/rival.md`
- Modify: `wiki/vocab/rock.md`
- Modify: `wiki/vocab/rodilla.md`
- Modify: `wiki/vocab/rojo.md`
- Modify: `wiki/vocab/romántico.md`
- Delete: `wiki/vocab/que-alivio.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/que-alivio.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
quieres.md, quiero.md, quince.md, quién.md, quiénes.md, qué-alivio.md, qué-bien.md, qué-emoción.md, qué-haces.md, qué-interesante.md, qué-lástima.md, qué-mala-suerte.md, qué-pena.md, qué-suerte.md, qué-tal.md, qué-tiempo-hace.md, qué-tonto.md, química.md, raqueta.md, receta.md, recibir.md, recital.md, recoger.md, recomendar.md, red-social.md, refresco.md, regalo.md, regla.md, regresar.md, relajado.md, relajante.md, relajarse.md, rellenar.md, reloj.md, reparar.md, reserva.md, reservar.md, resolver.md, responder.md, responsable.md, respuesta.md, restaurante.md, retrasado.md, reunión.md, rico.md, rival.md, rock.md, rodilla.md, rojo.md, romántico.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `qué-alivio.md` / `que-alivio.md`:** `qué-alivio.md` is the junk file (Category 1). Read the real content from `wiki/vocab/que-alivio.md` and merge it into `wiki/vocab/qué-alivio.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/que-alivio.md`. Then remove the line `- [[que-alivio]] ...` from `wiki/index.md` (search for the exact line starting with `- [[que-alivio]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 19 (quieres–romántico)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 19
- 50 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (que-alivio.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 21 begins.

---

## Task 21: Batch 20 — `ropa` .. `son-de` (50 files, 2 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/ropa.md`
- Modify: `wiki/vocab/rosa.md`
- Modify: `wiki/vocab/roto.md`
- Modify: `wiki/vocab/rubio.md`
- Modify: `wiki/vocab/ruso.md`
- Modify: `wiki/vocab/rápido.md`
- Modify: `wiki/vocab/río.md`
- Modify: `wiki/vocab/sal.md`
- Modify: `wiki/vocab/salida.md`
- Modify: `wiki/vocab/salir-de.md`
- Modify: `wiki/vocab/salmón.md`
- Modify: `wiki/vocab/salsa.md`
- Modify: `wiki/vocab/salud.md`
- Modify: `wiki/vocab/saludable.md`
- Modify: `wiki/vocab/sandalia.md`
- Modify: `wiki/vocab/sandía.md`
- Modify: `wiki/vocab/sandías.md`
- Modify: `wiki/vocab/sartén.md`
- Modify: `wiki/vocab/secretario.md`
- Modify: `wiki/vocab/secreto.md`
- Modify: `wiki/vocab/seis.md`
- Modify: `wiki/vocab/semana.md`
- Modify: `wiki/vocab/septiembre.md`
- Modify: `wiki/vocab/seria.md`
- Modify: `wiki/vocab/serie.md`
- Modify: `wiki/vocab/serio.md`
- Modify: `wiki/vocab/serpiente.md`
- Modify: `wiki/vocab/señor.md`
- Modify: `wiki/vocab/señora.md`
- Modify: `wiki/vocab/shorts.md`
- Modify: `wiki/vocab/siempre.md`
- Modify: `wiki/vocab/siete.md`
- Modify: `wiki/vocab/simple.md`
- Modify: `wiki/vocab/simpática.md`
- Modify: `wiki/vocab/simpático.md`
- Modify: `wiki/vocab/simpáticos.md`
- Modify: `wiki/vocab/sin-gluten.md`
- Modify: `wiki/vocab/sin-parar.md`
- Modify: `wiki/vocab/sin.md`
- Modify: `wiki/vocab/sistema.md`
- Modify: `wiki/vocab/sobre.md`
- Modify: `wiki/vocab/sobrina.md`
- Modify: `wiki/vocab/sociable.md`
- Modify: `wiki/vocab/sol.md`
- Modify: `wiki/vocab/solamente.md`
- Modify: `wiki/vocab/solo.md`
- Modify: `wiki/vocab/solución.md`
- Modify: `wiki/vocab/sombrero.md`
- Modify: `wiki/vocab/somos.md`
- Modify: `wiki/vocab/son-de.md`
- Delete: `wiki/vocab/sandia.md`
- Delete: `wiki/vocab/sarten.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/sandia.md`, `wiki/vocab/sarten.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
ropa.md, rosa.md, roto.md, rubio.md, ruso.md, rápido.md, río.md, sal.md, salida.md, salir-de.md, salmón.md, salsa.md, salud.md, saludable.md, sandalia.md, sandía.md, sandías.md, sartén.md, secretario.md, secreto.md, seis.md, semana.md, septiembre.md, seria.md, serie.md, serio.md, serpiente.md, señor.md, señora.md, shorts.md, siempre.md, siete.md, simple.md, simpática.md, simpático.md, simpáticos.md, sin-gluten.md, sin-parar.md, sin.md, sistema.md, sobre.md, sobrina.md, sociable.md, sol.md, solamente.md, solo.md, solución.md, sombrero.md, somos.md, son-de.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `sandía.md` / `sandia.md`:** `sandía.md` is the junk file (Category 1). Read the real content from `wiki/vocab/sandia.md` and merge it into `wiki/vocab/sandía.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/sandia.md`. Then remove the line `- [[sandia]] ...` from `wiki/index.md` (search for the exact line starting with `- [[sandia]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Duplicate pair — `sartén.md` / `sarten.md`:** `sartén.md` is the junk file (Category 1). Read the real content from `wiki/vocab/sarten.md` and merge it into `wiki/vocab/sartén.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/sarten.md`. Then remove the line `- [[sarten]] ...` from `wiki/index.md` (search for the exact line starting with `- [[sarten]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 20 (ropa–son-de)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 20
- 50 files corrected (type/pattern/example rewritten)
- 2 duplicate files removed (sandia.md, sarten.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 22 begins.

---

## Task 22: Batch 21 — `sopa` .. `terraza` (50 files, 2 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/sopa.md`
- Modify: `wiki/vocab/sorprendente.md`
- Modify: `wiki/vocab/sorprendido.md`
- Modify: `wiki/vocab/souvenir.md`
- Modify: `wiki/vocab/soy-de.md`
- Modify: `wiki/vocab/soy.md`
- Modify: `wiki/vocab/su.md`
- Modify: `wiki/vocab/sucio.md`
- Modify: `wiki/vocab/sudamericano.md`
- Modify: `wiki/vocab/sueldo.md`
- Modify: `wiki/vocab/sugerencia.md`
- Modify: `wiki/vocab/supermercado.md`
- Modify: `wiki/vocab/sushi.md`
- Modify: `wiki/vocab/suéter.md`
- Modify: `wiki/vocab/sábado.md`
- Modify: `wiki/vocab/sándwich.md`
- Modify: `wiki/vocab/sí-o-sí.md`
- Modify: `wiki/vocab/sí.md`
- Modify: `wiki/vocab/súper.md`
- Modify: `wiki/vocab/tableta.md`
- Modify: `wiki/vocab/taco.md`
- Modify: `wiki/vocab/talla.md`
- Modify: `wiki/vocab/taller.md`
- Modify: `wiki/vocab/tango.md`
- Modify: `wiki/vocab/tantos.md`
- Modify: `wiki/vocab/tarde.md`
- Modify: `wiki/vocab/tarea.md`
- Modify: `wiki/vocab/tarjeta-de-crédito.md`
- Modify: `wiki/vocab/tarta.md`
- Modify: `wiki/vocab/taxi.md`
- Modify: `wiki/vocab/taxista.md`
- Modify: `wiki/vocab/taza.md`
- Modify: `wiki/vocab/te-quiero.md`
- Modify: `wiki/vocab/teatro.md`
- Modify: `wiki/vocab/tecnología.md`
- Modify: `wiki/vocab/televisión.md`
- Modify: `wiki/vocab/teléfono.md`
- Modify: `wiki/vocab/temperatura.md`
- Modify: `wiki/vocab/temprano.md`
- Modify: `wiki/vocab/tener-hambre.md`
- Modify: `wiki/vocab/tener-prisa.md`
- Modify: `wiki/vocab/tener-que.md`
- Modify: `wiki/vocab/tener-razón.md`
- Modify: `wiki/vocab/tener-sueño.md`
- Modify: `wiki/vocab/tengo-que.md`
- Modify: `wiki/vocab/tengo.md`
- Modify: `wiki/vocab/tenis-de-mesa.md`
- Modify: `wiki/vocab/tenis.md`
- Modify: `wiki/vocab/terminar-de.md`
- Modify: `wiki/vocab/terraza.md`
- Delete: `wiki/vocab/si-o-si.md`
- Delete: `wiki/vocab/tecnologia.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/si-o-si.md`, `wiki/vocab/tecnologia.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
sopa.md, sorprendente.md, sorprendido.md, souvenir.md, soy-de.md, soy.md, su.md, sucio.md, sudamericano.md, sueldo.md, sugerencia.md, supermercado.md, sushi.md, suéter.md, sábado.md, sándwich.md, sí-o-sí.md, sí.md, súper.md, tableta.md, taco.md, talla.md, taller.md, tango.md, tantos.md, tarde.md, tarea.md, tarjeta-de-crédito.md, tarta.md, taxi.md, taxista.md, taza.md, te-quiero.md, teatro.md, tecnología.md, televisión.md, teléfono.md, temperatura.md, temprano.md, tener-hambre.md, tener-prisa.md, tener-que.md, tener-razón.md, tener-sueño.md, tengo-que.md, tengo.md, tenis-de-mesa.md, tenis.md, terminar-de.md, terraza.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `sí-o-sí.md` / `si-o-si.md`:** `sí-o-sí.md` is the junk file (Category 1). Read the real content from `wiki/vocab/si-o-si.md` and merge it into `wiki/vocab/sí-o-sí.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/si-o-si.md`. Then remove the line `- [[si-o-si]] ...` from `wiki/index.md` (search for the exact line starting with `- [[si-o-si]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Duplicate pair — `tecnología.md` / `tecnologia.md`:** `tecnología.md` is the junk file (Category 1). Read the real content from `wiki/vocab/tecnologia.md` and merge it into `wiki/vocab/tecnología.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/tecnologia.md`. Then remove the line `- [[tecnologia]] ...` from `wiki/index.md` (search for the exact line starting with `- [[tecnologia]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 21 (sopa–terraza)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 21
- 50 files corrected (type/pattern/example rewritten)
- 2 duplicate files removed (si-o-si.md, tecnologia.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 23 begins.

---

## Task 23: Batch 22 — `terrible` .. `uno-de` (50 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/terrible.md`
- Modify: `wiki/vocab/tiempo-libre.md`
- Modify: `wiki/vocab/tiempo.md`
- Modify: `wiki/vocab/tienda.md`
- Modify: `wiki/vocab/tiene.md`
- Modify: `wiki/vocab/tienen.md`
- Modify: `wiki/vocab/tienes-que.md`
- Modify: `wiki/vocab/tipo-de.md`
- Modify: `wiki/vocab/tocar.md`
- Modify: `wiki/vocab/todo-el-mundo.md`
- Modify: `wiki/vocab/todo.md`
- Modify: `wiki/vocab/todos-los-días.md`
- Modify: `wiki/vocab/tomar-clases.md`
- Modify: `wiki/vocab/tomar.md`
- Modify: `wiki/vocab/tomate.md`
- Modify: `wiki/vocab/tortilla.md`
- Modify: `wiki/vocab/tour.md`
- Modify: `wiki/vocab/trabajador.md`
- Modify: `wiki/vocab/trabajar.md`
- Modify: `wiki/vocab/trabajo.md`
- Modify: `wiki/vocab/tradicional.md`
- Modify: `wiki/vocab/traje-de-baño.md`
- Modify: `wiki/vocab/traje.md`
- Modify: `wiki/vocab/tranquila.md`
- Modify: `wiki/vocab/tranquilo.md`
- Modify: `wiki/vocab/trece.md`
- Modify: `wiki/vocab/treinta.md`
- Modify: `wiki/vocab/tren.md`
- Modify: `wiki/vocab/tres.md`
- Modify: `wiki/vocab/triste.md`
- Modify: `wiki/vocab/tu.md`
- Modify: `wiki/vocab/turismo.md`
- Modify: `wiki/vocab/turista.md`
- Modify: `wiki/vocab/té.md`
- Modify: `wiki/vocab/técnico.md`
- Modify: `wiki/vocab/tía.md`
- Modify: `wiki/vocab/tímida.md`
- Modify: `wiki/vocab/tío.md`
- Modify: `wiki/vocab/típico.md`
- Modify: `wiki/vocab/tú.md`
- Modify: `wiki/vocab/un-par-de.md`
- Modify: `wiki/vocab/un-poco-de.md`
- Modify: `wiki/vocab/un-poco.md`
- Modify: `wiki/vocab/un-rato.md`
- Modify: `wiki/vocab/un.md`
- Modify: `wiki/vocab/una-vez-por.md`
- Modify: `wiki/vocab/una.md`
- Modify: `wiki/vocab/uniforme.md`
- Modify: `wiki/vocab/universidad.md`
- Modify: `wiki/vocab/uno-de.md`
- Delete: `wiki/vocab/traje-de-bano.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/traje-de-bano.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
terrible.md, tiempo-libre.md, tiempo.md, tienda.md, tiene.md, tienen.md, tienes-que.md, tipo-de.md, tocar.md, todo-el-mundo.md, todo.md, todos-los-días.md, tomar-clases.md, tomar.md, tomate.md, tortilla.md, tour.md, trabajador.md, trabajar.md, trabajo.md, tradicional.md, traje-de-baño.md, traje.md, tranquila.md, tranquilo.md, trece.md, treinta.md, tren.md, tres.md, triste.md, tu.md, turismo.md, turista.md, té.md, técnico.md, tía.md, tímida.md, tío.md, típico.md, tú.md, un-par-de.md, un-poco-de.md, un-poco.md, un-rato.md, un.md, una-vez-por.md, una.md, uniforme.md, universidad.md, uno-de.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Duplicate pair — `traje-de-baño.md` / `traje-de-bano.md`:** `traje-de-baño.md` is the junk file (Category 1). Read the real content from `wiki/vocab/traje-de-bano.md` and merge it into `wiki/vocab/traje-de-baño.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/traje-de-bano.md`. Then remove the line `- [[traje-de-bano]] ...` from `wiki/index.md` (search for the exact line starting with `- [[traje-de-bano]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- **Distinct word, not a duplicate — `tu.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/tu.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- **Distinct word, not a duplicate — `tú.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/tú.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 22 (terrible–uno-de)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 22
- 50 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (traje-de-bano.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 24 begins.

---

## Task 24: Batch 23 — `uno` .. `ya-no` (50 files)

**Files:**
- Modify: `wiki/vocab/uno.md`
- Modify: `wiki/vocab/urgente.md`
- Modify: `wiki/vocab/urgentemente.md`
- Modify: `wiki/vocab/usar.md`
- Modify: `wiki/vocab/uso.md`
- Modify: `wiki/vocab/usted.md`
- Modify: `wiki/vocab/ustedes.md`
- Modify: `wiki/vocab/va-a-estar-bien.md`
- Modify: `wiki/vocab/vaca.md`
- Modify: `wiki/vocab/vacaciones.md`
- Modify: `wiki/vocab/vacío.md`
- Modify: `wiki/vocab/varios.md`
- Modify: `wiki/vocab/vaso-de.md`
- Modify: `wiki/vocab/vaso.md`
- Modify: `wiki/vocab/vegetariano.md`
- Modify: `wiki/vocab/veinte.md`
- Modify: `wiki/vocab/veintiuno.md`
- Modify: `wiki/vocab/vendedor.md`
- Modify: `wiki/vocab/vender.md`
- Modify: `wiki/vocab/venezolano.md`
- Modify: `wiki/vocab/ventana.md`
- Modify: `wiki/vocab/verano.md`
- Modify: `wiki/vocab/verdad.md`
- Modify: `wiki/vocab/verde.md`
- Modify: `wiki/vocab/verdura.md`
- Modify: `wiki/vocab/verificar.md`
- Modify: `wiki/vocab/vestido.md`
- Modify: `wiki/vocab/vez.md`
- Modify: `wiki/vocab/viajar.md`
- Modify: `wiki/vocab/vida.md`
- Modify: `wiki/vocab/videojuego.md`
- Modify: `wiki/vocab/viejo.md`
- Modify: `wiki/vocab/viento.md`
- Modify: `wiki/vocab/viernes.md`
- Modify: `wiki/vocab/vino.md`
- Modify: `wiki/vocab/violín.md`
- Modify: `wiki/vocab/virus.md`
- Modify: `wiki/vocab/visitar.md`
- Modify: `wiki/vocab/vitamina.md`
- Modify: `wiki/vocab/vivir.md`
- Modify: `wiki/vocab/voluntario.md`
- Modify: `wiki/vocab/vuelo.md`
- Modify: `wiki/vocab/vóleibol.md`
- Modify: `wiki/vocab/wifi.md`
- Modify: `wiki/vocab/y-cuarto.md`
- Modify: `wiki/vocab/y-media.md`
- Modify: `wiki/vocab/y-tú.md`
- Modify: `wiki/vocab/y-usted.md`
- Modify: `wiki/vocab/y.md`
- Modify: `wiki/vocab/ya-no.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 50 files per the content-fix procedure**

Files in this batch:
```
uno.md, urgente.md, urgentemente.md, usar.md, uso.md, usted.md, ustedes.md, va-a-estar-bien.md, vaca.md, vacaciones.md, vacío.md, varios.md, vaso-de.md, vaso.md, vegetariano.md, veinte.md, veintiuno.md, vendedor.md, vender.md, venezolano.md, ventana.md, verano.md, verdad.md, verde.md, verdura.md, verificar.md, vestido.md, vez.md, viajar.md, vida.md, videojuego.md, viejo.md, viento.md, viernes.md, vino.md, violín.md, virus.md, visitar.md, vitamina.md, vivir.md, voluntario.md, vuelo.md, vóleibol.md, wifi.md, y-cuarto.md, y-media.md, y-tú.md, y-usted.md, y.md, ya-no.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 23 (uno–ya-no)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 23
- 50 files corrected (type/pattern/example rewritten)
- 0 duplicate files removed
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable as long as it lands before Task 25 begins.

---

## Task 25: Batch 24 — `yo-también` .. `útil` (11 files, 1 duplicate pair(s))

**Files:**
- Modify: `wiki/vocab/yo-también.md`
- Modify: `wiki/vocab/yo.md`
- Modify: `wiki/vocab/yoga.md`
- Modify: `wiki/vocab/yogur.md`
- Modify: `wiki/vocab/zapato.md`
- Modify: `wiki/vocab/zona.md`
- Modify: `wiki/vocab/zoológico.md`
- Modify: `wiki/vocab/árabe.md`
- Modify: `wiki/vocab/él.md`
- Modify: `wiki/vocab/últimamente.md`
- Modify: `wiki/vocab/útil.md`
- Delete: `wiki/vocab/ultimamente.md`
- Modify: `wiki/index.md`

**Interfaces:**
- Consumes: the content-fix procedure and duplicate-pair rules defined in Global Constraints above.
- Consumes: real content currently in `wiki/vocab/ultimamente.md` (pre-existing, non-junk files — must still exist unedited when this task runs).
- Produces: rewritten vocab files, a `fix:` commit, and a `wiki/log.md` entry. No later task depends on this task's output.

- [ ] **Step 1: Rewrite each of the 11 files per the content-fix procedure**

Files in this batch:
```
yo-también.md, yo.md, yoga.md, yogur.md, zapato.md, zona.md, zoológico.md, árabe.md, él.md, últimamente.md, útil.md
```

Apply steps 1–7 from "Content-fix procedure" (Global Constraints) to each file.

- **Distinct word, not a duplicate — `él.md` (Category 2):** apply the standard content-fix procedure independently to `wiki/vocab/él.md`. Do NOT merge, delete, or touch any other file, and do NOT edit `wiki/index.md` for this file — it is a genuinely distinct word from its accent-pair counterpart.

- **Duplicate pair — `últimamente.md` / `ultimamente.md`:** `últimamente.md` is the junk file (Category 1). Read the real content from `wiki/vocab/ultimamente.md` and merge it into `wiki/vocab/últimamente.md` (apply the standard content-fix procedure to the merged content — correct `type`/`Pattern`/`Example` as needed, keep the accented filename as the canonical page). Then delete `wiki/vocab/ultimamente.md`. Then remove the line `- [[ultimamente]] ...` from `wiki/index.md` (search for the exact line starting with `- [[ultimamente]]` and delete it — do not rely on a line number, as earlier batches may have shifted them).

- [ ] **Step 2: Run the batch verification command**

Use the "Batch verification command" template from Global Constraints, substituting this batch's exact file list from Step 1 (for any Category 1 pair, verify the surviving accented/merged file — the deleted unaccented source no longer exists to check). Expected: no `STILL JUNK` output.

- [ ] **Step 3: Commit and push**

```bash
cd /Users/laowuisme/Documents/MyWork/spanish-wiki
git add wiki/vocab/ wiki/index.md
git commit -m "fix: correct vocab placeholder content, batch 24 (yo-también–útil)"
git push
```

- [ ] **Step 4: Append log entry**

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] fix | vocab placeholder cleanup batch 24
- 11 files corrected (type/pattern/example rewritten)
- 1 duplicate file removed (ultimamente.md)
```
Commit this log update together with Step 3, or as a small follow-up commit — either is acceptable — this is the final batch task.

---

## Self-Review Notes (completed during plan authoring)

1. **Spec coverage:** Every junk file (1,161) is covered across Tasks 2–25 (24 batches × ~50, last batch 11). All 16 Category 1 pairs and all 7 Category 2 files are called out explicitly in their respective batch task, with exact source/target filenames and exact index.md removal instructions. The excluded files (`si-o-si.md` real content source, `cuando.md`, and the 444 other non-junk files) are never listed as Modify targets in any task.
2. **Placeholder scan:** No "TBD"/"handle appropriately"/"similar to Task N" — every task lists its exact filenames, exact commit message, and exact log entry text. The only per-file variability (the actual Spanish content: real examples, corrected patterns) is inherent creative/linguistic work governed by the fully-specified 7-step procedure, not a vague instruction.
3. **Type consistency:** Frontmatter fields (`cefr`, `stage`, `type`, `last_updated`) and body sections (`**Meaning:**`, `**Pattern:**`, `**Example:**`) match the Vocab Atom format in `/Users/laowuisme/Documents/MyWork/spanish-wiki/CLAUDE.md` in every task.

## Execution Handoff

24 batch tasks (Tasks 2–25) are independent of each other and well-suited to fresh-subagent-per-task execution, since each batch's own commit/push/log makes it independently reviewable.
