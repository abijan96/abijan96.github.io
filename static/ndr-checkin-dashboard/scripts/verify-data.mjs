// Gate B — machine-verified data integrity.
// Parses NDR_DATA back out of the built index.html and asserts invariants.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const html = readFileSync(path.join(__dirname, "..", "index.html"), "utf8");

const match = html.match(/const NDR_DATA = (\{[\s\S]*?\n\});\s*\n<\/script>/);
if (!match) throw new Error("Could not locate NDR_DATA object literal in index.html");
const NDR_DATA = new Function("return " + match[1])();

let count = 0;
function assert(cond, msg) {
  count++;
  if (!cond) {
    console.error("FAIL:", msg);
    process.exitCode = 1;
  }
}

// ---- Structure ----
assert(NDR_DATA.thirtyDay && NDR_DATA.ninetyDay && NDR_DATA.sixMonth && NDR_DATA.overview,
  "3 stage objects + overview present");
assert(NDR_DATA.thirtyDay.kpis.length === 7, "7 KPIs at 30-Day");
assert(NDR_DATA.sixMonth.kpis.length === 7, "7 KPIs at 6-Month");
assert(NDR_DATA.thirtyDay.sentiment.length === 10, "10 sentiment rows at 30-Day");
assert(NDR_DATA.sixMonth.sentiment.length === 10, "10 sentiment rows at 6-Month");
assert(NDR_DATA.ninetyDay.questionScores.length === 11, "11 question scores at 90-Day");
assert(NDR_DATA.overview.mappedMetrics.length === 7, "7 Overview mapped metrics");
assert(NDR_DATA.overview.recurringConcerns.length === 9, "9 recurring-concern rows (8 baseline + 1 new: payroll deduction accuracy)");

// ---- Invariants ----
for (const stage of ["thirtyDay", "sixMonth"]) {
  const d = NDR_DATA[stage];
  for (const s of d.sentiment) {
    assert(s.positive + s.mixed === 100, `${stage} sentiment ${s.q} sums to 100 (got ${s.positive}+${s.mixed})`);
    if (s.pubPositive !== undefined) {
      assert(s.pubPositive + s.pubMixed === 100, `${stage} sentiment ${s.q} published sums to 100`);
    }
    const expectFlag = s.positive < 60 || s.mixed > 40;
    assert(s.flag === expectFlag, `${stage} sentiment ${s.q} flag matches rule (positive<60 or mixed>40): flag=${s.flag} positive=${s.positive} mixed=${s.mixed}`);
  }
  for (const k of d.kpis) {
    assert(k.pct >= 0 && k.pct <= 100, `${stage} KPI ${k.label} within 0-100 (got ${k.pct})`);
    if (k.pub !== undefined) assert(k.pub >= 0 && k.pub <= 100, `${stage} KPI ${k.label} published within 0-100`);
  }
  const rbSum = d.roadblockBreakdown.reduce((a, r) => a + r.pct, 0);
  assert(rbSum === 100, `${stage} roadblock breakdown sums to 100 (got ${rbSum})`);
  const rbPubVals = d.roadblockBreakdown.filter(r => r.pub !== undefined);
  if (rbPubVals.length === d.roadblockBreakdown.length) {
    const pubSum = rbPubVals.reduce((a, r) => a + r.pub, 0);
    assert(pubSum === 100, `${stage} roadblock breakdown published sums to 100 (got ${pubSum})`);
  }
}
for (const q of NDR_DATA.ninetyDay.questionScores) {
  assert(q.score >= 1 && q.score <= 5, `90-Day ${q.q} score within 1-5 (got ${q.score})`);
  assert(q.positivePct >= 0 && q.positivePct <= 100, `90-Day ${q.q} positivePct within 0-100`);
}
for (const row of NDR_DATA.ninetyDay.responseDistribution.rows) {
  // Each category is independently rounded from n=48 integer counts in the
  // published report (not a complementary pair I compute), so a rounding
  // artifact of +/-1 point is expected and is NOT a transcription error --
  // §2 says copy published numbers verbatim, not force them to sum exactly.
  const sum = row.sa + row.a + row.d + row.sd;
  assert(sum >= 98 && sum <= 102, `90-Day response distribution ${row.q} sums within rounding tolerance of 100 (got ${sum})`);
}

// ---- Overview mappedMetrics equal their cited (merged) sources ----
const t = NDR_DATA.thirtyDay, s6 = NDR_DATA.sixMonth, n90 = NDR_DATA.ninetyDay;
const kpiByLabel = arr => Object.fromEntries(arr.map(k => [k.label, k.pct]));
const tK = kpiByLabel(t.kpis), sK = kpiByLabel(s6.kpis);
const checks = [
  ["Job expectations", tK["Job Matches Expectations"], 98, sK["Job Matches Expectations"]],
  ["Welcomed / belonging", tK["Felt Welcomed"], 96, sK["Felt Welcomed"]],
  ["Engaged & challenged", tK["Engaged (Not Bored)"], 96, sK["Engaged (Not Bored)"]],
  ["Communication", tK["Communication Effective"], 100, sK["Communication Effective"]],
  ["Team support", tK["Team Helped Onboarding"], 100, sK["Team Helped Onboarding"]],
  ["Culture satisfaction", tK["Culture Satisfaction"], null, sK["Culture Satisfaction"]],
  ["No roadblocks", tK["No Roadblocks"], 87, sK["No Roadblocks"]],
];
for (const [metric, d30, d90, m6] of checks) {
  const row = NDR_DATA.overview.mappedMetrics.find(r => r.metric === metric);
  assert(!!row, `Overview row exists for ${metric}`);
  assert(row.d30 === d30, `Overview ${metric} d30 matches 30-Day KPI (${row.d30} vs ${d30})`);
  assert(row.d90 === d90, `Overview ${metric} d90 matches 90-Day source (${row.d90} vs ${d90})`);
  assert(row.m6 === m6, `Overview ${metric} m6 matches 6-Month KPI (${row.m6} vs ${m6})`);
}
assert(NDR_DATA.overview.mappedMetrics.find(r => r.metric === "Culture satisfaction").d90 === null,
  "Culture satisfaction's 90-day value is null, not 0");

// ---- Published-vs-updated pair present for every dotted (changed) figure ----
for (const stage of ["thirtyDay", "sixMonth"]) {
  const d = NDR_DATA[stage];
  for (const k of d.kpis) {
    if (k.pub !== undefined) assert(typeof k.pub === "number", `${stage} KPI ${k.label} has a published pair`);
  }
  for (const sRow of d.sentiment) {
    if (sRow.pubPositive !== undefined) {
      assert(typeof sRow.pubPositive === "number" && typeof sRow.pubMixed === "number",
        `${stage} sentiment ${sRow.q} has a complete published pair`);
    }
  }
  for (const r of d.roadblockBreakdown) {
    // roadblock breakdown may legitimately be unchanged; no hard requirement here
  }
}
assert(NDR_DATA.thirtyDay.sessionsPub === 28, "30-Day session count published pair = 28");
assert(NDR_DATA.sixMonth.sessionsPub === 8, "6-Month session count published pair = 8");

// ---- Baseline anchors (published-report values, unchanged where ingestion didn't touch them) ----
assert(n90.overallScore === 4.47, "90-Day overall score unchanged at 4.47");
assert(n90.positiveRatePct === 96, "90-Day positive rate unchanged at 96");
assert(n90.validResponses === 48, "90-Day valid responses unchanged at 48");
const deltas = n90.yoy.deltas.map(d => d.delta).sort((a, b) => b - a);
assert(deltas.filter(x => x === 0.35).length === 3, "3 YoY deltas of +0.35");
assert(deltas[deltas.length - 1] === -0.14, "1 YoY delta of -0.14");
const trendScores = n90.overallTrend.points.map(p => p.score);
assert(JSON.stringify(trendScores) === JSON.stringify([4.79, 4.34, 4.55, 4.64]), "trend scores unchanged 4.79/4.34/4.55/4.64");
const trendN = n90.overallTrend.points.map(p => p.responses);
assert(JSON.stringify(trendN) === JSON.stringify([3, 19, 25, 1]), "trend n unchanged 3/19/25/1");

// 30-Day merged anchors (from data-reconciliation.md §7)
assert(tK["Job Matches Expectations"] === 91, "30-Day merged Job Match = 91");
assert(tK["No Roadblocks"] === 70, "30-Day merged No Roadblocks = 70");
assert(t.kpis.find(k => k.label === "Job Matches Expectations").pub === 88, "30-Day published Job Match = 88 preserved");
assert(t.kpis.find(k => k.label === "No Roadblocks").pub === 72, "30-Day published No Roadblocks = 72 preserved");

// 6-Month merged anchors
assert(sK["Culture Satisfaction"] === 83, "6-Month merged Culture Satisfaction = 83");
assert(s6.kpis.find(k => k.label === "Culture Satisfaction").pub === 75, "6-Month published Culture Satisfaction = 75 preserved");
assert(sK["No Roadblocks"] === 70, "6-Month merged No Roadblocks = 70");

// ---- Flags: exactly which rows are flagged ----
const t30Flags = t.sentiment.filter(s => s.flag).map(s => s.q);
assert(JSON.stringify(t30Flags) === JSON.stringify(["Q4"]), `30-Day flags exactly Q4 (got ${t30Flags})`);
const s6Flags = s6.sentiment.filter(s => s.flag).map(s => s.q);
assert(JSON.stringify(s6Flags) === JSON.stringify(["Q4", "Q11"]), `6-Month flags exactly Q4, Q11 (got ${s6Flags})`);

// ---- Name scan: no personal names anywhere in the data (heuristic: no bracket
// content other than the two approved bracketed roles; scan quote/theme/text fields) ----
const ALLOWED_BRACKETS = new Set(["[My manager]", "[a trusted senior contact]"]);
function collectStrings(obj, out) {
  if (typeof obj === "string") { out.push(obj); return; }
  if (Array.isArray(obj)) { obj.forEach(v => collectStrings(v, out)); return; }
  if (obj && typeof obj === "object") { Object.values(obj).forEach(v => collectStrings(v, out)); }
}
const allStrings = [];
collectStrings(NDR_DATA, allStrings);
const bracketPattern = /\[[^\]]+\]/g;
let badBrackets = [];
for (const s of allStrings) {
  const found = s.match(bracketPattern) || [];
  for (const b of found) if (!ALLOWED_BRACKETS.has(b)) badBrackets.push(b);
}
assert(badBrackets.length === 0, `no unexpected bracketed content (found: ${badBrackets.join(", ")})`);

// Known personal names from source files that must never appear
const BANNED_NAMES = [
  "Ashley Hudson", "Wei Zhang", "Nathaniel Thompson", "Emily Casanova", "Ed Standen",
  "Christine Doolittle", "Veronica Mendoza", "Chris Woodward", "Brett Walter",
  "Nikki Herndon", "Gemma Stanton", "Scott Pattison", "Verodia Charlestin",
  "Jeff Faust", "Jennifer Knowlton", "Ben Riggles", "Barbara Dominguez", "Martha Reilly",
  "Ciara Donovan", "Jinah Song", "Mary Porter", "JJ Gregg", "Stephen Bird", "Partha Choudhury",
  "Lisa Nichols", "Brendan Daly", "Heather Buelow",
];
const joined = allStrings.join(" \n ");
const foundNames = BANNED_NAMES.filter(n => joined.includes(n));
assert(foundNames.length === 0, `no personal names present (found: ${foundNames.join(", ")})`);

// ---- Banned UI words (leadership-facing copy) ----
const BANNED_WORDS = ["AI-coded", "ingestion", "calibration", "uncalibrated", "Likert"];
const foundBanned = BANNED_WORDS.filter(w => joined.includes(w));
assert(foundBanned.length === 0, `no banned words in dashboard copy (found: ${foundBanned.join(", ")})`);
// "blend"/"blended" banned as a standalone UI word; allow "blocks" etc. (word-boundary check)
assert(!/\bblend(ed|ing)?\b/i.test(joined), "no 'blend' variant in dashboard copy");

console.log(`PASS ${count} assertions`);
