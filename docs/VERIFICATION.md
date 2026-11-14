# UGREEN Hackathon 2026 — Round 1 verification notes

## Sources checked 2026-10-25 (page-text fetch only, no live browser, no sign-in)
- Devpost: https://ugreenhackathon.devpost.com/ — authoritative for submission rules.
- UGREEN page: https://ai.ugreen.com/pages/ugreen-hackathon
- Starter kit: https://ai.ugreen.com/pages/hackathon-starter-kit (capability scope + package structure)

## Discrepancy found (follow Devpost)
- The UGREEN marketing page's "Preliminary Submission" list mentions a prototype walkthrough video (up to 3 min).
- Devpost explicitly states: "Round 1 does not require a separate code repository link, or a demo link/video."
- Resolution: this package follows Devpost (no video, no repo link). If the parent wants belt-and-braces, a video can be added later — but it is NOT required per Devpost.

## Rule compliance
- Proposal: 10 questions answered, 486 substantive words (limit 500), PDF 5,584 bytes (limit 1 MB).
- Package ZIP: 9,736 bytes (limit 10 MB), 6 files + 2 dirs (limit 100 files), largest file 8,502 bytes (limit 1 MB/file).
- Contents: SKILL.md + README.md + 4 linked references only. No scripts, executables, binaries, manifests, credentials, keys, or personal data (grep-checked).
- Frontmatter: name `duplicate-family-triage` (23 chars, lowercase hyphenated, valid), description 627 chars (limit 1,024).
- Skill newly developed during the hackathon; no prior Skill/material reused.

## What was actually tested
- Local dry-run prototype (local-prototype/, NOT in the ZIP): exact SHA-256 pair + resized copy grouped as one family with original as keeper; different image separate; corrupt JPEG skipped; .txt ignored; nothing moved or deleted. Verified twice (Codex run + independent re-run).
- NOT tested (cannot be without finalist NAS access): UGOS installation, Uliya trigger wiring, real photo libraries, album-membership updates, quarantine restore on iDX6011 Pro. Stated honestly in proposal Q8 and SKILL.md.

## Not done (needs parent / hao)
- NOT submitted. Devpost submission itself needs live-browser work (sign-in + form upload) — out of scope for this subagent.
- Official UGOS Skill Creation Tool archive was NOT downloaded (requires browser download from the starter-kit page); the package follows the Devpost + starter-kit written spec instead. If selected as finalist, run the tool's own checker ("Help me check this skill") before Round 2.
