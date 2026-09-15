#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

function walk(d, acc = []) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if ([".git", "node_modules", "scripts", ".cursor"].includes(e.name)) continue;
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p, acc);
    else if (e.name.endsWith(".html")) acc.push(p);
  }
  return acc;
}

const files = walk(".");
const report = { noindex: [], httpCanon: [], httpHref: [], aggregate: [], missingTitle: [], missingH1: [], missingCanon: [], multiH1: [] };

for (const f of files) {
  const c = fs.readFileSync(f, "utf8");
  const rel = f.replace(/\\/g, "/");
  if (/name=["']robots["'][^>]*noindex/i.test(c) || /content=["'][^"']*noindex/i.test(c)) {
    report.noindex.push(rel);
  }
  const can = c.match(/rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || c.match(/href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
  if (!can) report.missingCanon.push(rel);
  else if (can[1].startsWith("http://")) report.httpCanon.push({ rel, href: can[1] });
  if (/href=["']http:\/\/angelgranit\.com/i.test(c)) report.httpHref.push(rel);
  if (/AggregateRating/i.test(c) && /application\/ld\+json/i.test(c)) report.aggregate.push(rel);
  if (!/<title>/i.test(c)) report.missingTitle.push(rel);
  const h1s = c.match(/<h1\b[^>]*>/gi) || [];
  if (h1s.length === 0) report.missingH1.push(rel);
  if (h1s.length > 1) report.multiH1.push({ rel, n: h1s.length });
}

console.log(JSON.stringify({
  files: files.length,
  noindex: report.noindex,
  httpCanon: report.httpCanon,
  httpHrefCount: report.httpHref.length,
  httpHrefSample: report.httpHref.slice(0, 15),
  aggregateInLdJson: report.aggregate,
  missingTitle: report.missingTitle.slice(0, 20),
  missingH1: report.missingH1.slice(0, 30),
  missingCanonCount: report.missingCanon.length,
  missingCanonSample: report.missingCanon.slice(0, 20),
  multiH1: report.multiH1.slice(0, 20),
}, null, 2));
