#!/usr/bin/env node
/**
 * Submit URLs to IndexNow (Bing + partners).
 * Usage: node scripts/submit-indexnow.cjs
 *        node scripts/submit-indexnow.cjs https://angelgranit.com/geo/
 */
const https = require("https");

const KEY = "c593bf749008c91d834f592f72c23c05";
const HOST = "angelgranit.com";
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

const DEFAULT_URLS = [
  `https://${HOST}/`,
  `https://${HOST}/uslugi/`,
  `https://${HOST}/uslugi/ritualnye-uslugi/`,
  `https://${HOST}/uslugi/organizaciya-pohoron/`,
  `https://${HOST}/uslugi/katafalk/`,
  `https://${HOST}/uslugi/granitnye-pamyatniki/`,
  `https://${HOST}/ceny/`,
  `https://${HOST}/kontakty/`,
  `https://${HOST}/o-kompanii/`,
  `https://${HOST}/otzyvy/`,
  `https://${HOST}/nashi-raboty/`,
  `https://${HOST}/vlog/`,
  `https://${HOST}/geo/`,
  `https://${HOST}/ai/`,
  `https://${HOST}/AI.md`,
  `https://${HOST}/llms.txt`,
  `https://${HOST}/sitemap.xml`,
];

const extra = process.argv.slice(2).filter((u) => /^https:\/\//i.test(u));
const urlList = [...new Set([...DEFAULT_URLS, ...extra])];

const body = JSON.stringify({
  host: HOST,
  key: KEY,
  keyLocation: KEY_LOCATION,
  urlList,
});

const req = https.request(
  {
    hostname: "api.indexnow.org",
    path: "/indexnow",
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Content-Length": Buffer.byteLength(body),
    },
  },
  (res) => {
    let data = "";
    res.on("data", (c) => (data += c));
    res.on("end", () => {
      console.log("IndexNow status:", res.statusCode);
      if (data) console.log(data);
      console.log("Submitted", urlList.length, "URLs");
      // 200/202 = accepted
      if (res.statusCode !== 200 && res.statusCode !== 202) process.exit(1);
    });
  }
);
req.on("error", (e) => {
  console.error(e);
  process.exit(1);
});
req.write(body);
req.end();
