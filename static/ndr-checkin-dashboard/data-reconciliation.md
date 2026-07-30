# Data Reconciliation Report — NDR New-Employee Check-In Dashboard

Status: **Final.** This is the internal ingestion record (file inventory, rubric,
merge arithmetic, open questions and their resolutions). It is kept in the repo but
not linked from the dashboard. The dashboard itself uses plain-language framing for
a stakeholder audience — this document is the technical backing for those numbers.

---

## 1. Inventory

All four expected source locations plus their immediate parent folders were swept.

| Location | Files found | Status |
|---|---|---|
| `6 month Check in\6-month Check-In Notes` | 12 `.docx` | 6 baseline-covered files (one, `12.13.24.docx`, contains 4 concatenated sessions — see §2), 2 blank, 4 new |
| `30 Day Notes\FY 25` | 13 `.docx` | All 13 baseline-covered, 0 new |
| `30 Day Notes\FY 26` | 14 `.docx` | 6 baseline-covered, **8 new** |
| `90 Days` | `90-Day Survey Links.gsheet.xlsx` | Fully parsed; no new rows (§4) |
| Parent folders (6-Month, 30-Day, 90-Day) | Analyst work product only (scripts, PDFs, chart images, `session_dataset.json`) | No additional session data; used for calibration only, not counted as source files |
| No `FY 24` or `FY 27` subfolder anywhere | — | Confirms FY24 is report-only (no source folder) and no FY27 cohort exists yet |

**12 new sessions total: 8 in 30-Day (all FY26), 4 in 6-Month.**

## 2. Resolved: the two "missing" 6-Month baseline files

`12.13.24.docx` is not a single session — it's a running log containing **four**
dated check-ins appended into one file: 12/13/24, 1/31/25, 3/24/25, and a fourth,
**5/21/25, which the published `sessionsTable` never counted**. Full text confirms
5/21/25 is a genuine fragment (no question structure, cuts off mid-sentence) —
correctly excluded by the original analysts on the same basis as the two blank
templates (5/28/25, 9/17/25). All 8 baseline sessions are now accounted for and
were used in calibration (§3).

## 3. Rubric — the single standard used for all 12 new sessions

Two calibration passes (an automated script re-run, and two manual rubric variants
against a 9-session 30-Day sample and all 8 baseline 6-Month sessions) each failed
to reproduce the published percentages within tolerance, in inconsistent directions
per question — evidence the published numbers reflect session-by-session editorial
judgment not fully recoverable as a fixed rule. Given that, the adopted standard
(directional accuracy over false precision) is: **experience questions (Q1 job
expectations, Q2 challenged/bored, Q3 welcomed, Q5-6 communication/team help, Q8
culture) are coded positive unless the session records actual negative evidence —
frustration, an unresolved complaint, or a stated limitation — not merely a hedge,
a pending item, or a suggestion; needs questions (Q4 roadblocks, Q7 training, Q9
goals, Q10 expertise, Q11 adjustments) are coded mixed whenever a real request or
concern is present, even if minor or already resolved.** Two standing rulings
apply within that frame: Q4's "No Roadblocks" KPI counts only answers describing
an actual impediment to work (a mentioned-but-resolved-and-non-blocking issue still
counts toward Q4's *sentiment* row and appears in `roadblockDetails`, just not
against the KPI); Q8 is coded mixed only on genuine dissatisfaction, since the
question explicitly invites improvement ideas as a normal part of answering it.
All 12 new sessions were coded once under this standard; results below. The
automated-script divergence (up to 20 points off baseline, one question's polarity
inverted) remains a flag for the analyst team to review independently — out of
scope here, not corrected or used.

## 4. 90-Day: verified, unchanged

Full parse of all 54 rows in the workbook (48 valid + 2 near-uniform "strongly
disagree" rows excluded as evident test submissions + 4 blank/abandoned rows)
reproduces the published per-question means and % positive almost exactly (largest
gap: 0.06 on one mean; every % positive matches exactly). Last valid response is
dated 2026-02-04, inside the published "through Feb 2026" window. **No new 90-Day
data exists. Nothing in this stage changes.**

## 5. Dedupe check

All 12 new-session dates were checked against the full baseline date list for each
stage (28 dates for 30-Day, 8 for 6-Month). **No collisions.**

- 30-Day new: 2/27/26, 3/3/26, 3/5/26, 3/27/26, 4/15/26, 6/15/26, 7/10/26, 7/24/26
- 6-Month new: 4/22/26, 5/6/26, 6/19/26, 7/17/26

## 6. FY boundary note

`7/10/26`, `7/24/26` (30-Day) and `7/17/26` (6-Month) fall in July 2026. They're
grouped under FY26 here, matching their physical folder location and the existing
FY26 date-range convention, but if NDR's fiscal year runs July–June, these three
sessions may belong to FY27 under the analysts' own convention. Grouping can be
revisited; not changed here.

## 7. Final merged numbers

Session-weighted blend: `merged = round((published × published_n + new × new_n) / total_n)`,
whole percentages throughout. Full arithmetic is in `scripts/final_merge.py`
(run it to reproduce every number below).

### 30-Day (28 published sessions + 8 new = 36)

| KPI | Published | New sessions only | **Merged** |
|---|---|---|---|
| Job Matches Expectations | 88 | 100 | **91** |
| Felt Welcomed | 100 | 100 | **100** |
| Engaged (Not Bored) | 96 | 100 | **97** |
| Communication Effective | 92 | 100 | **94** |
| Team Helped Onboarding | 96 | 100 | **97** |
| Culture Satisfaction | 87 | 100 | **90** |
| No Roadblocks | 72 | 62 | **70** |

Sentiment by question (positive/mixed): Q1 91/9, Q2 97/3, Q3 100/0, **Q4 33/67
(flagged)**, Q5-6 94/6, Q7 65/35 (clears baseline flag), Q8 90/10, Q9 84/16, Q10
77/23, Q11 66/34 (clears baseline flag). Only Q4 remains flagged.

Roadblock breakdown: None 70, IT/System 18, HR/Benefits 8, Training Gaps 4.

FY26 (6 published + 8 new = 14 sessions): Job Match 98, Welcomed 100, Engaged 100,
Communication 98, Team Support 100, Culture 96, No Roadblocks 70. Sessions 6→14,
participants ~8→~19, date range extends to July 2025 – July 2026.

thirtyDay top level: sessions 28→36, participants ~60→~71, date range extends to
Sept 2023 – July 2026.

### 6-Month (8 published sessions + 4 new = 12)

| KPI | Published | New sessions only | **Merged** |
|---|---|---|---|
| Job Matches Expectations | 100 | 100 | **100** |
| Felt Welcomed | 100 | 75 | **92** |
| Engaged (Not Bored) | 100 | 100 | **100** |
| Communication Effective | 100 | 100 | **100** |
| Team Helped Onboarding | 100 | 100 | **100** |
| Culture Satisfaction | 75 | 100 | **83** |
| No Roadblocks | 67 | 75 | **70** |

Note the direction: under the first-draft (superseded) rubric, Culture Satisfaction
had appeared to fall to 50. Under the final adopted rubric — which does not count a
scheduling-constraint comment ("wanted to volunteer, but the times haven't worked
out") or a cross-unit-visibility wish as dissatisfaction — both substantive new Q8
answers code positive, so Culture Satisfaction **rises** to 83, not down to 50. This
is the single biggest swing in the whole exercise from adopting the final rubric
over the earlier draft.

Sentiment by question: Q1 100/0, Q2 100/0, Q3 92/8, **Q4 30/70 (flagged)**, Q5-6
100/0, Q7 67/33 (clears baseline flag), Q8 83/17, Q9 78/22, Q10 67/33 (clears
baseline flag), **Q11 47/53 (flagged, unchanged)**.

Roadblock breakdown: None 70, Leadership Transitions 11, System/Tech 19 (the one
new facilities-layout roadblock — two work locations for a single role — is folded
into System/Tech to stay within the existing 3-slice donut rather than adding a
4th; this is a judgment call, not user-ruled, but its impact on any single slice is
≤5 points either way).

sixMonth top level: sessions 8→12, participants ~28→~33, responses captured 31→36,
date range extends to Mar 2024 – July 2026.

### Journey `mappedMetrics` (final)

| Metric | d30 (was → now) | d90 | m6 (was → now) |
|---|---|---|---|
| Job expectations | 88 → 91 | 97.9 | 100 → 100 |
| Welcomed / belonging | 100 → 100 | 95.8 | 100 → 92 |
| Engaged & challenged | 96 → 97 | 95.8 | 100 → 100 |
| Communication | 92 → 94 | 100 | 100 → 100 |
| Team support | 96 → 97 | 100 | 100 → 100 |
| Culture satisfaction | 87 → 90 | null | 75 → 83 |
| No roadblocks | 72 → 70 | 87.2 | 67 → 70 |

Net picture: nearly every metric holds steady or improves slightly with the new
sessions folded in. The one real, still-visible pattern: **Felt Welcomed / belonging
softens by 6 months** (100 at 30-day and ~96 at 90-day, down to 92 at 6-month) and
**No Roadblocks dips at 30 days before recovering** (70 → 87.2 → 70) — a much milder
version of the original "U-shape" story, not a collapse.

## 8. Remaining open questions from the first pass — resolved by default

Per standing instruction, defaults apply where the alternative reading changes a
number by ≤5 points; all did:

- New unit "ND P&P" seen in one session — added to `unitsRepresented`.
- "Team Helped Onboarding" KPI proxy (Q6-alone vs. combined Q5-6) — doesn't affect
  the merged number since new sessions are 100% positive under either reading.
- 30-Day Q11 baseline boundary quirk (flag:true at exactly 60/40) — not altered;
  the merged value (66/34) is clearly inside bounds either way.
- 6-Month roadblock-category slice for the new facilities issue — folded into
  System/Tech (§7).

## 9. Anonymization

No personal name from any source file (baseline or new) appears anywhere in the
dashboard, the data file, or this report. All references are by date, unit, or role.

## 10. What changed in the deliverable itself

Per final instructions, the dashboard drops per-row caveat chips and hedging
banners in favor of one pattern: a small dot marker on any figure that differs
from its published-report value, a single footer legend line, and a tooltip
showing both values on hover/focus. "Journey" is renamed "Overview" and is the
default landing tab. All qualitative percentages are whole numbers; survey scores
keep 2 decimals; nothing else carries decimals. Two new recommendation cards were
added (30-Day: verify a flagged retirement-contribution withholding rate; 6-Month:
address a split-facility/two-building operational issue) since both are concrete,
traceable findings from the new sessions that a stakeholder-facing recommendations
section should surface. Two new anonymized quotes were added to the 6-Month
Notable Quotes grid to keep that section representative of all 12 sessions now
behind the stage, not just the original 8.

## 11. July 2026 addendum — 90-Day survey refresh, dot mechanic retired

Source: `90-day New Hire Survey as of 7.30.26.xlsx` (single sheet, raw Qualtrics
export, 66 rows) — the sole authoritative 90-Day dataset as of this addendum,
superseding every prior 90-Day figure in this report and in the dashboard.
Exclusions: 1 row flagged `Survey Preview` by Qualtrics' own `Status` field
(a genuine test submission — more reliable than the heuristic pattern-matching
used for the original baseline), plus 4 rows with zero questions answered
(abandoned starts). **59 valid responses**, up from the prior baseline's 48.
The question set, scale, and scoring rules (SA=5…SD=1; Q5 Yes/No=5/1; Q10
reverse-scored) are unchanged from the original baseline — verified by direct
comparison of row-2 question text before recomputing anything.

Every 90-Day-derived figure was recomputed from this file alone: overall score
4.47→**4.44**, positive rate 96%→**94%**, YoY improvement (2024→2025) unchanged
in shape (all areas improved) but now **all eleven** areas improve (previously
ten of eleven, with manager communication showing a small decline) — manager
communication's gain is now +0.01, essentially flat rather than negative. No
roadblocks (Q10) is now the one question below the 4.0 target, at 3.88 — new
third color band (red, "needs attention," under 4.0) added to the 90-Day score
chart to reflect this. Overview's Journey-at-a-Glance 90-Day column, the Three
Trends to Watch chart, and the recurring-concerns 90-Day cells were all
recomputed from the same refreshed figures; 30-Day and 6-Month data are
untouched (Gate B re-run confirms both their anchors and the new 90-Day anchors
in a single pass).

Separately, the published-vs-updated dot mechanic (dot markers, tooltip pairs,
the About-popover legend, and the 6-Month session table's "added since" row
badges — the same distinction in a different shape) was retired dashboard-wide
per explicit instruction. Every figure now carries a single current value;
there is nothing left in `NDR_DATA` for a report to be "published against."
The About popover's versioning language is now just "Data through July 30, 2026."
