# Duplicate Family Triage

A UGOS Skill for the [UGREEN Hackathon 2026](https://ugreenhackathon.devpost.com/) (Automate Your Workflow track). Your NAS fills up with the same photo five times: the phone backup, the SD-card import, the chat download, the edited export. This Skill finds those copies, groups them into families, picks the best original to keep, and — only after you say so, family by family — moves the rest to a quarantine folder you can undo for 30 days. It never deletes anything.

Devpost entry: https://devpost.com/software/duplicate-family-triage

## Status — read this first

**This is a dry-run prototype, not a tested NAS product.** The grouping logic was proven with a local prototype on synthetic test images (see [Measured results](#measured-results) below). Installation on UGOS, Uliya trigger wiring, real photo libraries, album-membership updates, and quarantine restore on the UGREEN AI NAS iDX6011 Pro have **not** been tested — the official NAS test environment is provided only to Finalists, and that testing is Finalist-stage work. Nothing on this page claims otherwise.

## How it works

1. Tell it which folders to scan and which folder to use as quarantine.
2. Read the plan: one family at a time, with the keeper, why it won, and how much space each family would free.
3. Confirm the families you want quarantined — one by one, or in bulk for families you name together.
4. Read the final summary and the report. Anything quarantined can be moved back to exactly where it came from.

## What it will never do

- Delete a file, move a file without your confirmation, or scan a folder you did not name.
- Break an album: if album membership cannot be verified for a family, that family is left alone.
- Send anything off your NAS. Matching runs locally; no external service is involved.

## Contents

- `SKILL.md` — the full Skill specification (workflow, keeper rule, report format).
- `references/` — keeper rules, conversation script, safety rules and the Finalist test plan, disclosures.
- `prototype/` — the local dry-run prototype that proves the grouping and keeper logic:
  - `dedup.py` — read-only scanner: exact matches by SHA-256, near-duplicates by 8×8 average perceptual hash within the same orientation group. Dry-run only; it never moves, changes, or deletes a file.
  - `make_fixtures.py`, `make_fixtures2.py` — deterministic generators for the two test sets.
  - `fixtures/`, `fixtures2/` — the test images (originals, byte-identical copies, half-size re-exports, unique images, corrupt files, a non-image file).
  - `runs/` — verbatim logs of the runs below.
- `docs/VERIFICATION.md` — what was checked for the Round 1 submission, and what was not tested.

## Try the prototype

Requires Python 3 and Pillow (`pip install Pillow`).

```bash
python3 prototype/dedup.py prototype/fixtures
python3 prototype/dedup.py prototype/fixtures2
python3 prototype/dedup.py prototype/fixtures2 --json
```

## Measured results

Runs on 2026-11-14, local dry-run only. No file was moved, changed, or deleted in any run.

**Small set (the original verification set, re-run 2026-11-14):** 4 images scanned in 0.42 s — 1 exact SHA-256 pair and 1 half-size re-export grouped into one family with the original as keeper (12,598 bytes reclaimable); 1 different image kept separate; 1 corrupt JPEG skipped; 1 non-image file ignored.

**Larger set (25 files, 22 images, built 2026-11-14 to mimic repeated imports — 6 originals, each with one byte-identical copy and one half-size re-export, plus 4 unique images, 2 corrupt files, 1 non-image file):** scanned in 0.25 s. All 6 exact copies found by SHA-256. 5 of 6 re-exports grouped as near-duplicates by perceptual hash. 2 corrupt files skipped, 1 non-image file ignored, nothing moved or deleted.

**What the prototype got wrong — and why the safety design exists:** the perceptual hash merged one genuinely different image (a smooth gradient that looks almost identical to another scene at 8×8 resolution) into the wrong family, and the keeper rule then picked the wrong keeper for that family. A second re-export (a dot pattern at half size) was missed and left as a single. So the tool's own report of 86,857 reclaimable bytes is inflated by the false-positive family; the verified-correct figure is **68,086 bytes**. This is exactly why nothing moves without per-family confirmation and why quarantine is reversible for 30 days: matching is imperfect, so the design never lets a guess delete — or even move — a file on its own. The report flags every keeper with its reason, so a wrong keeper is visible before anything happens.

**Still not built / not tested:** UGOS installation, Uliya trigger wiring, real photo libraries, album-membership updates, and quarantine restore on the UGREEN AI NAS iDX6011 Pro. Those are Finalist-stage tests only.

## License

MIT — see [LICENSE](LICENSE).
