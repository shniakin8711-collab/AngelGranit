const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
let scanned = 0;
let fixed = 0;

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "node_modules") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
      continue;
    }
    if (!entry.name.endsWith(".html")) continue;
    scanned += 1;
    let html = fs.readFileSync(full, "utf8");
    const next = html.replace(/5а<a href="tel:/g, '5а · <a href="tel:');
    if (next !== html) {
      fs.writeFileSync(full, next);
      fixed += 1;
    }
  }
}

walk(ROOT);
console.log(JSON.stringify({ scanned, fixed }, null, 2));
