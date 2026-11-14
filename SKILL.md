---
name: duplicate-family-triage
description: USE FOR: finding exact and near-duplicate photos and videos on a UGREEN AI NAS, grouping copies into families, choosing the best original to keep, and quarantining the rest only after user confirmation to reclaim storage safely. Trigger phrases include "triage my duplicates", "find duplicate photos", "clean up duplicate files", "which copies can I delete", and "reclaim space from duplicates". DO NOT USE FOR: deleting files without confirmation, organizing files into categories, editing or enhancing photos, searching for a specific photo, transcribing audio, or any task outside the folders the user explicitly authorizes.
---

# Duplicate Family Triage

## User goal

Help a NAS owner reclaim storage from repeated imports — phone backups, SD-card imports, chat downloads, edited exports — without ever risking the only good original. The result is a readable report: one family per set of copies, one clearly justified keeper per family, and every other copy either quarantined (reversible for 30 days) or deliberately left alone. Nothing is deleted by this Skill, ever.

## Required inputs

- **Folders to scan**: one or more folder paths named by the user. No folder is scanned unless the user names it.
- **Quarantine folder**: a folder the user names for quarantined copies, or the default the NAS offers. Quarantine is the only folder this Skill ever writes to, plus the report location below.
- **Confirmation scope**: per-family confirmation (default) or bulk confirmation for families the user explicitly approves together.
- **Retention**: quarantine retention, default 30 days, after which the user — not the Skill — decides whether quarantined copies are deleted.

If any input is missing, ask for it and stop. Do not guess folders, do not scan the whole NAS, and do not substitute similar content.

## Supported NAS capabilities used

This Skill uses only capabilities in the official UGREEN capability scope for this Hackathon:

- **Files** — find, browse, organize, and deduplicate files in authorized folders. Used in Steps 1, 2, 3, and 5.
- **Albums** — find photos by person, location, or time, and organize albums. Used in Step 4 to check that the keeper keeps its album membership before anything moves.
- **Uliya conversation** — the interface for every question, plan, confirmation, and report. No step runs silently.

No other capability is used. If a step would need a capability outside this list, stop that step, tell the user, and continue only with what is supported.

## Workflow

Each step must use the actual output of the previous step. Never refer vaguely to "that directory from before": always carry the concrete folder path, file path, and family list forward.

### Step 1 — Confirm scope (Files, Uliya)

1. Ask the user for the folders to scan and the quarantine folder.
2. Repeat the exact paths back and confirm read access on the scanned folders and write access on the quarantine folder.
3. If a path does not exist or access is denied, report exactly which path failed and stop. Do not scan anything else.

### Step 2 — Scan and group (Files)

1. Enumerate every photo and video file in the authorized folders only. Skip symlinks and unreadable files; list every skipped file in the report with its reason.
2. Group **exact duplicates** by content hash: files with identical content belong to one family.
3. Group **near duplicates** for photos by perceptual hash, comparing only within the same orientation group (landscape, portrait, square) to reduce false matches. Resized, recompressed, or re-exported copies of the same photo belong to the same family as the original.
4. For videos in this version, group exact matches only. Do not claim video similarity matching.
5. A file that matches nothing is a single-member family: it is reported as unique and never touched.

### Step 3 — Pick the keeper (Files)

Rank every family by the keeper rule in `references/keeper-rules.md`, in order: non-derived original first, then highest resolution, then largest file, then earliest date, then a deterministic tiebreak. Record, for every non-keeper, the exact reason it lost (for example: "edited export", "smaller pixel count", "later date"). The keeper rule is the whole justification the user sees — never present a keeper without its reason.

### Step 4 — Check albums before moving anything (Albums)

For each family with more than one member, check album membership: if a non-keeper belongs to an album and the keeper does not, flag it in the plan and keep the keeper in that album's place. If album membership cannot be verified for a family, mark that family "leave alone" in the plan and explain why. Never break a shared album.

### Step 5 — Present the plan and get confirmation (Uliya)

Present, per family: the keeper path, every other member path with its reason, the bytes reclaimable if the non-keepers were quarantined, and any album flags from Step 4. Then wait for the user's confirmation: per family, or in bulk only for families the user explicitly names together. If the user confirms nothing, nothing moves and the report still records the plan. If the user rejects a family, that family is left alone and marked rejected in the report.

### Step 6 — Quarantine, verify, report (Files, Uliya)

1. Move only confirmed families' non-keepers into the quarantine folder, preserving each file's original folder path inside quarantine so restoration is unambiguous.
2. After moving, verify every keeper is still present and byte-identical to before the move. If any keeper fails verification, stop immediately, report exactly which keeper failed, and restore quarantined files for that family.
3. Write the report (see below) and deliver a final summary: families found, families quarantined, families left alone, bytes reclaimable, and how to restore any quarantined file.

## Completion and failure handling

- **Complete** means: the report exists, every confirmed family was quarantined and its keeper verified, and the user received the final summary. Say so explicitly, with the counts.
- **No duplicates found** means: say "No duplicate families were found in the folders you named" and stop. Do not invent families, do not scan other folders, do not suggest deleting unique files.
- **No result for a step** (for example, a folder is empty, album membership is unavailable, or a file cannot be read): say exactly what was missing, list the affected files or families, and stop that branch. Never substitute similar or unrelated content.
- **User confirmation required** before: moving any file, quarantining any file, and changing any album membership. There is no step in this Skill that moves, deletes, or shares a file without confirmation.
- **Never delete**: this Skill has no delete step. Deleting quarantined copies after retention is the user's own later decision, outside this Skill.
- **Never share externally**: no file, path, hash, or report content leaves the NAS. No external service is called.

## Report format

The report lists, per family: family id, keeper path and keeper reason, each non-keeper path with its reason, match type (exact or near), album flags, decision (quarantined / left alone / rejected), and bytes reclaimable. It ends with totals and a skipped-files section (path and reason for every unreadable or skipped file). Keep the report in plain language a non-technical owner can audit.

## Validation status

This Skill was specified and its grouping logic was proven with a local dry-run prototype on test images (exact pair plus resized copy grouped as one family; a different image kept separate; a corrupt file skipped; a non-image file ignored). Installation on UGOS, Uliya trigger wiring, real photo-library behavior, album-membership updates, and quarantine restore on a UGREEN AI NAS iDX6011 Pro are not yet tested, because the official NAS test environment is provided only to Finalists. Finalist testing will use the two core cases and one edge case in `references/testing-plan.md`.

## References

- `references/keeper-rules.md` — the keeper ranking rule and worked examples.
- `references/user-flow.md` — the conversation script: what to ask, what to show, and when to stop.
- `references/safety-and-testing.md` — safety rules, failure handling, and the Finalist test plan.
- `references/disclosures.md` — third-party components, principal functionality developed for this Hackathon, and AI tools used.
