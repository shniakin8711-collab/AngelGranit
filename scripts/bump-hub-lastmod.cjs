const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const TODAY = "2026-09-15";
const HUBS = new Set([
  "https://angelgranit.com/",
  "https://angelgranit.com/uslugi/",
  "https://angelgranit.com/kontakty/",
  "https://angelgranit.com/ceny/",
  "https://angelgranit.com/o-kompanii/",
  "https://angelgranit.com/geo/",
  "https://angelgranit.com/ai/",
  "https://angelgranit.com/vlog/",
]);

const sitemapPath = path.join(ROOT, "sitemap.xml");
let xml = fs.readFileSync(sitemapPath, "utf8");
let bumped = 0;

xml = xml.replace(
  /<url>\s*<loc>([^<]+)<\/loc>\s*<lastmod>[^<]*<\/lastmod>/g,
  (block, loc) => {
    if (!HUBS.has(loc)) return block;
    bumped += 1;
    return block.replace(/<lastmod>[^<]*<\/lastmod>/, `<lastmod>${TODAY}</lastmod>`);
  }
);

fs.writeFileSync(sitemapPath, xml);
console.log(JSON.stringify({ bumped, today: TODAY }, null, 2));
