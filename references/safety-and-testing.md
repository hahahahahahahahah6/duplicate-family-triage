# Safety and testing

## Safety rules (non-negotiable)

1. Never delete a file. Quarantine is the strongest action this Skill takes, and it is reversible.
2. Never move, quarantine, or change album membership for any file without the user's explicit confirmation for that family.
3. Never scan, read, or write outside the folders the user named, except the quarantine folder for approved copies and the report location.
4. Never send any file, path, hash, or report content to any external service or person.
5. Never use credentials, keys, or personal data. This package contains none, and no step asks the user for any.
6. If any rule above conflicts with completing a step, the rule wins and the step stops.

## Known limits and risks

- Perceptual matching can confuse burst photos or near-identical scans. Mitigations: conservative threshold, orientation grouping, per-family confirmation, and a "leave alone" recommendation when uncertain.
- Video similarity is not implemented in this version; videos match exactly only.
- Album membership verification depends on the NAS Albums capability behaving on the real device; unverified families default to "leave alone".
- Large libraries may take a long time to scan. The Skill reports progress per folder and never times out silently: if a scan cannot finish, it says which folder was incomplete.

## Finalist test plan (to run on the assigned UGREEN AI NAS iDX6011 Pro)

- **Core case 1:** a library containing exact copies, a resized copy, and an edited export of one photo must yield exactly one family with the original as keeper.
- **Core case 2:** confirming quarantine for one family only must leave all other families untouched, with the keeper byte-identical after the move, and the quarantined copy restorable to its original path.
- **Edge case:** a burst-mode sequence of near-identical but distinct photos must NOT be grouped as duplicates.

## Local validation already done (not on NAS hardware)

A local dry-run prototype implementing the same grouping and keeper logic was run on synthetic test images: an exact JPEG pair plus a resized copy grouped into one family with the original as keeper; a visually different image kept separate; a corrupt JPEG listed as skipped without crashing; a text file ignored. The prototype moved and deleted nothing. It is not part of the submitted package, because the submission standard prohibits scripts in the package.
