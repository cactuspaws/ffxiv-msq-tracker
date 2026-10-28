# MSQ Journey

A mobile-first, unofficial Final Fantasy XIV main-scenario quest tracker.

## Status

**Work in progress.** The interface and local progress engine are committed in `index.html`. The verified, ordered quest dataset from **Soul Searching** through the end of post-Dawntrail is not installed yet. Until `quests.json` is populated, the UI explicitly displays that the quest database is missing. Do not interpret zero remaining quests as completed progress.

## Quest data format

Add `quests.json` at the repository root. It must be a JSON array, ordered by actual MSQ progression, with unique string IDs:

```json
[
  {"id":"ffxiv-quest-id","name":"Soul Searching","expansion":"Post-Stormblood"}
]
```

Include only the required main scenario path, with every quest from the starting quest onward. Verify the source and ordering, including patch quests, before publishing. The app deliberately does not manufacture quest titles or counts.

## Features

- One-tap quest completion; completed quests move to a separate crossed-out section
- Fixed daily target until the next local calendar day, with deadline-adjusted pacing
- Option to detach checkoffs from the day's completion count
- Browser `localStorage` persistence
- Date-specific daily history
- JSON backup and restore
- Editable deadline (temporary default January 1, 2027)
- Responsive layout, no build tools or backend

## Hosting

GitHub Pages: **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. The published URL should be `https://cactuspaws.github.io/ffxiv-msq-tracker/`.

## Important

Browser storage is device- and browser-specific, and is not automatically synced. Export backups regularly. The date-detachment toggle affects newly completed quests, not previously completed ones. Changing the deadline recalculates today's target.

## Generate the full quest database

The repository includes a GitHub Actions workflow named **Update MSQ quest database**. Open **Actions**, select that workflow, and choose **Run workflow**. It downloads the community wiki's ordered MSQ tables, extracts quests starting at Soul Searching, validates milestones and a minimum expected count, and commits `quests.json` if validation succeeds. If it fails, check the Actions log; no partial database is committed.

Quest source: https://ffxiv.consolegameswiki.com/wiki/Main_Scenario_Quests (community-maintained, subject to change).

**Before relying on the tracker**, verify that `quests.json` exists and that the first/last quest and expansion totals are correct. The generator has not yet been verified by a successful GitHub Actions run.
