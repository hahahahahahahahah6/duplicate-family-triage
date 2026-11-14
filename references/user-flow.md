# User flow — conversation script

## Opening

Ask exactly three things, then stop and wait:

1. "Which folders should I scan for duplicates?"
2. "Which folder should I use as quarantine for copies you approve?"
3. "Do you want to confirm each family one by one, or approve families in bulk?"

Repeat the folders back verbatim and confirm access before scanning. If the user names no folders, do not proceed.

## Presenting the plan

Show one block per family, in plain language:

- Keeper: path, and why it won (one keeper-rule reason).
- Other copies: each path, match type (exact or near), and why it lost.
- Space: bytes reclaimable if this family's non-keepers were quarantined.
- Album flags: any album membership that needs the keeper to take the non-keeper's place, or "album membership could not be verified — recommended: leave alone".

Then ask: "Which families should I quarantine? Name them, say 'all', or say 'none'."

## After quarantine

Deliver a final summary with five numbers: families found, families quarantined, families left alone, families rejected, bytes reclaimable. Then explain restoration in one sentence: quarantined copies keep their original folder path inside the quarantine folder and can be moved back to exactly where they came from.

## When to stop instead of proceeding

- The user did not name folders: stop, ask again.
- A folder does not exist or access is denied: report that path, stop.
- No duplicates found: say so plainly, stop.
- Album membership cannot be verified for a family: mark it "leave alone", explain why, continue with other families.
- The user confirms nothing: move nothing, still deliver the report.
- A keeper fails verification after a move: stop immediately, report the keeper, restore that family's quarantined files.
