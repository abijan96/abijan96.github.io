// Gate C — browser acceptance checklist, automated where possible.
// Requires: npm install puppeteer-core (not bundled; run once before use).
// Points at a locally installed Chrome/Edge — see `candidates` below.
import puppeteer from "puppeteer-core";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const filePath = "file://" + path.join(__dirname, "..", "index.html").replace(/\\/g, "/");

function findChrome() {
  const candidates = [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  ];
  const fs = require("fs");
  for (const c of candidates) if (fs.existsSync(c)) return c;
  throw new Error("No browser found");
}
const { existsSync } = await import("node:fs");
const candidates = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
];
const execPath = candidates.find(c => existsSync(c));
if (!execPath) throw new Error("No Chrome/Edge found");
console.log("Using browser:", execPath);

const results = [];
function check(name, cond, detail) {
  results.push({ name, pass: !!cond, detail: detail || "" });
}

const browser = await puppeteer.launch({ executablePath: execPath, headless: "new" });
try {
  const page = await browser.newPage();
  const consoleErrors = [];
  page.on("console", msg => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", err => consoleErrors.push(String(err)));

  // 1. Load default (Overview) tab
  await page.goto(filePath, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 400));
  const hash1 = await page.evaluate(() => location.hash);
  check("Default landing tab is #overview", hash1 === "#overview", `got ${hash1}`);
  const overviewVisible = await page.evaluate(() => document.getElementById("panel-overview").classList.contains("active"));
  check("Overview panel active on load", overviewVisible);

  // 2. All four tabs render content
  for (const stage of ["thirtyDay", "ninetyDay", "sixMonth", "overview"]) {
    await page.click(`#tab-${stage}`);
    await new Promise(r => setTimeout(r, 250));
    const html = await page.evaluate((s) => document.getElementById("panel-" + s).innerHTML.length, stage);
    check(`Tab ${stage} renders non-empty content`, html > 500, `innerHTML length ${html}`);
  }

  // 3. Hash routing direct load
  await page.goto(filePath + "#6-month", { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 300));
  const sixActive = await page.evaluate(() => document.getElementById("panel-sixMonth").classList.contains("active"));
  check("Direct load with #6-month activates 6-Month panel", sixActive);

  // 4. Canvas count (charts actually created)
  await page.goto(filePath, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 300));
  let totalCanvases = 0;
  for (const stage of ["overview", "thirtyDay", "ninetyDay", "sixMonth"]) {
    await page.click(`#tab-${stage}`);
    await new Promise(r => setTimeout(r, 300));
    const n = await page.evaluate(() => document.querySelectorAll("canvas").length);
    totalCanvases = Math.max(totalCanvases, n);
    check(`Tab ${stage} has canvases`, n > 0, `${n} canvases`);
  }

  // 5. FY chips on 30-Day
  await page.click("#tab-thirtyDay");
  await new Promise(r => setTimeout(r, 300));
  await page.click('button[data-fy="FY26"]');
  await new Promise(r => setTimeout(r, 300));
  const fy26Text = await page.evaluate(() => document.getElementById("fyContent").innerText);
  check("FY26 chip shows Improvements panel (not Roadblocks)", fy26Text.includes("Improvements"), fy26Text.slice(0, 200));

  // 6. Flags present exactly where expected
  await page.click("#tab-thirtyDay");
  await new Promise(r => setTimeout(r, 250));
  const flag30 = await page.evaluate(() => {
    const details = document.querySelector("#panel-thirtyDay details.datatable");
    return details ? details.innerText : "";
  });

  // 7. No personal names / only approved bracketed roles anywhere on page
  const bodyText = await page.evaluate(() => document.body.innerText);
  const bannedNames = ["Ashley Hudson", "Wei Zhang", "Nathaniel Thompson", "Jennifer Knowlton", "Ben Riggles"];
  const foundNames = bannedNames.filter(n => bodyText.includes(n));
  check("No personal names visible in rendered DOM", foundNames.length === 0, foundNames.join(","));
  const bracketMatches = bodyText.match(/\[[^\]]+\]/g) || [];
  const badBrackets = bracketMatches.filter(b => !["[My manager]", "[a trusted senior contact]"].includes(b));
  check("Only approved bracketed roles visible", badBrackets.length === 0, badBrackets.join(","));

  // 8. Banned words check on rendered text
  const bannedWords = ["AI-coded", "ingestion", "calibration", "uncalibrated", "Likert"];
  const foundBanned = bannedWords.filter(w => bodyText.includes(w));
  check("No banned words visible in rendered DOM", foundBanned.length === 0, foundBanned.join(","));
  check("No 'blend' variant visible in rendered DOM", !/\bblend(ed|ing)?\b/i.test(bodyText));

  // 9. Dot markers present and have tooltip text
  await page.click("#tab-thirtyDay");
  await new Promise(r => setTimeout(r, 250));
  const dotCount = await page.evaluate(() => document.querySelectorAll(".dot").length);
  check("30-Day tab has dot markers for changed figures", dotCount > 0, `${dotCount} dots`);
  const dotTitle = await page.evaluate(() => {
    const dot = document.querySelector(".dot");
    return dot ? dot.getAttribute("title") : null;
  });
  check("Dot marker tooltip shows both published and updated values",
    dotTitle && dotTitle.includes("Published report") && dotTitle.includes("Updated"), dotTitle);

  // 10. Responsive check at 375px width
  await page.setViewport({ width: 375, height: 800 });
  await new Promise(r => setTimeout(r, 300));
  const hOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 5);
  check("No horizontal overflow at 375px", !hOverflow, `scrollWidth vs clientWidth`);
  await page.setViewport({ width: 1200, height: 900 });

  // 11. Keyboard: tabs reachable and operable
  await page.goto(filePath, { waitUntil: "networkidle0" });
  await page.focus("#tab-overview");
  await page.keyboard.press("ArrowRight");
  const focusedId = await page.evaluate(() => document.activeElement.id);
  check("Arrow-right moves focus to next tab", focusedId === "tab-thirtyDay", focusedId);

  // 12. CDN failure fallback
  const blockHandler = req => {
    if (req.url().includes("chart.js") || req.url().includes("chartjs-plugin-datalabels")) req.abort();
    else req.continue();
  };
  page.on("request", blockHandler);
  await page.setRequestInterception(true);
  await page.goto(filePath, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 400));
  const noticeVisible = await page.evaluate(() => {
    const n = document.querySelector(".notice");
    return n && n.offsetParent !== null;
  });
  check("CDN-failure notice appears when Chart.js blocked", noticeVisible);
  const detailsOpen = await page.evaluate(() => {
    const arr = [...document.querySelectorAll("details.datatable")];
    return arr.length > 0 && arr.every(d => d.open);
  });
  check("All data-table <details> auto-open on CDN failure", detailsOpen);
  await page.setRequestInterception(false);
  page.off("request", blockHandler);

  // 13. Console errors (from the normal, non-blocked load)
  consoleErrors.length = 0;
  await page.goto(filePath, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 500));
  for (const stage of ["thirtyDay", "ninetyDay", "sixMonth", "overview"]) {
    await page.click(`#tab-${stage}`);
    await new Promise(r => setTimeout(r, 300));
  }
  check("No console errors during normal use", consoleErrors.length === 0, consoleErrors.join(" | "));

} finally {
  await browser.close();
}

console.log("\n=== GATE C RESULTS ===");
let failCount = 0;
for (const r of results) {
  console.log(`${r.pass ? "PASS" : "FAIL"} — ${r.name}${r.detail ? " (" + r.detail + ")" : ""}`);
  if (!r.pass) failCount++;
}
console.log(`\n${results.length - failCount}/${results.length} checks passed`);
if (failCount > 0) process.exitCode = 1;
