#!/usr/bin/env node
/**
 * Differentiate GEO titles/H1 from SEO/uslugi cannibalization, then regenerate.
 */
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const MANIFEST = path.join(ROOT, "geo", "manifest.json");

const data = JSON.parse(fs.readFileSync(MANIFEST, "utf8"));

function stripGeoSuffix(s) {
  return String(s)
    .replace(/\s*[—–|-]\s*(кратко|краткий ответ|GEO)[^|]*$/i, "")
    .replace(/\s*\|\s*AngelGranit\s*$/i, "")
    .replace(/\s*[—–|-]\s*GEO AngelGranit\s*$/i, "")
    .replace(/\s*[—–|-]\s*AngelGranit\s*$/i, "")
    .trim();
}

for (const page of data.pages) {
  const topic = stripGeoSuffix(page.h1);
  page.h1 = `${topic} — кратко`;
  page.title = `${topic} — краткий ответ для ИИ | AngelGranit`;
  if (!/^Краткий ответ/i.test(page.description)) {
    page.description = `Краткий ответ (GEO), не дубль SEO: ${page.description}`;
  }
  // Ensure description stays reasonable length
  if (page.description.length > 165) {
    page.description = page.description.slice(0, 162).replace(/\s+\S*$/, "") + "…";
  }
}

data.hub.title = "GEO · краткие ответы для людей и ИИ — не дубль SEO | AngelGranit";
data.hub.description =
  "50 кратких GEO-ответов AngelGranit для ChatGPT/Claude/Gemini/Perplexity. Не заменяют /uslugi/ и /seo/: канон услуг — в каталоге, SEO-лендинги — в /seo/, здесь только answer-first.";

fs.writeFileSync(MANIFEST, JSON.stringify(data, null, 2) + "\n", "utf8");
console.log("Manifest differentiated:", data.pages.length, "pages");
