# NDR New-Employee Check-In Dashboard

A single-file, static dashboard for Notre Dame Research leadership summarizing
new-employee feedback across three onboarding check-in stages — 30-Day, 90-Day,
and 6-Month — plus a cross-stage Overview.

## What it is

- `index.html` — the complete dashboard. Everything (styles, logic, data) is in
  this one file. No build step, no server required.
- Data sources: NDR 30-Day Check-In, 90-Day Onboarding Survey, and 6-Month
  Check-In feedback from new hires, Sept 2023 through mid-2026. There is a
  single current value for every figure — no published-vs-updated distinction.
- Personal names are removed throughout; quotes are anonymized to bracketed
  roles or omitted where a role reference wasn't available in the source.

## Files in this repo

| File | Purpose |
|---|---|
| `index.html` | The dashboard (ship this) |
| `README.md` | This file |
| `data-reconciliation.md` | Internal record of how session notes/survey data collected after the published reports were folded in — file inventory, rubric, and the arithmetic behind every updated number. Not linked from the dashboard. |
| `scripts/verify-data.mjs` | Data-integrity check — run with `node scripts/verify-data.mjs` |
| `scripts/gate-c.mjs` | Browser acceptance check (needs `npm install puppeteer-core` first, and a local Chrome/Edge install) |

## Deploy to GitHub Pages

1. Create a GitHub repo (e.g. `ndr-checkin-dashboard`), add `index.html` (and
   `README.md` if you want it visible), push to `main`.
2. Repo **Settings → Pages → Source: "Deploy from a branch" → `main` / `root`
   → Save**.
3. The dashboard goes live at `https://<username>.github.io/ndr-checkin-dashboard/`
   within a minute or two.

On a free GitHub plan, Pages requires the repo to be public — which is why
names are anonymized throughout. Keep it that way if you fork or extend this.

## Updating the data

There's no database and no build step — `NDR_DATA` is a plain JavaScript object
literal near the top of `index.html`. To update a number, edit it there
directly, then re-run `node scripts/verify-data.mjs` to confirm nothing broke
(sentiment rows still sum to 100, KPIs stay in range, flags match the stated
rule, etc.) before publishing.
