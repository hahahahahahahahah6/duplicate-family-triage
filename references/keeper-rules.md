# Keeper rules

Rank each duplicate family in this exact order. The first rule that separates two files decides. The winner is the keeper; every other member's report reason names the rule that eliminated it.

1. **Non-derived original first.** A file whose name suggests it is a screenshot, export, copy, or edit (for example: "screenshot", "export", "copy", "edited") loses to a file without such a hint. Rationale: the original is the file most likely to hold full quality and original metadata.
2. **Highest resolution.** For photos, the largest pixel count wins. Rationale: a resized copy cannot regain detail the original holds.
3. **Largest file size.** If resolution ties, the larger file wins. Rationale: at equal dimensions, the larger file is usually less compressed.
4. **Earliest date.** If size ties, the earliest modification date wins. Rationale: the earliest copy is most likely the first import, not a later re-save.
5. **Deterministic tiebreak.** If everything above ties, the shortest path wins, then the alphabetically first path. Rationale: the result must be identical on every run, so the user can audit it.

## Worked examples

- `Photos/2025/beach.jpg` (4000x3000, 5.2 MB) vs `Downloads/beach_copy.jpg` (identical content): rule 1 keeps the original; the copy is reported as "exact duplicate, derived filename hint".
- `Photos/2025/beach.jpg` vs `Exports/beach_export.jpg` (2000x1500 recompressed version of the same photo): rule 1, then rule 2, keep the original; the export is reported as "near duplicate, smaller pixel count".
- Two identical files with no filename hints and equal size: rule 4 keeps the earlier one; rule 5 breaks any remaining tie deterministically.

## Deliberate conservatism

- Burst-mode sequences and near-identical scans are the known confusion risk. Near-duplicate grouping uses a conservative perceptual-hash threshold and compares only within the same orientation group, and every grouped family still needs the user's confirmation before anything moves. When in doubt, the Skill reports the family but recommends "leave alone".
- Videos: exact matches only in this version. A video that merely looks similar is never grouped.
