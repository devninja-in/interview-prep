#!/usr/bin/env node
/**
 * Copy the static book site into dist/ for Cloudflare Workers assets.
 * Keeps .git and repo metadata out of the upload.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DIST = path.join(ROOT, "dist");

const ENTRIES = ["index.html", "read.html", "css", "js", "assets"];

function copy(src, dest) {
  const st = fs.statSync(src);
  if (st.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      copy(path.join(src, name), path.join(dest, name));
    }
    return;
  }
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });

for (const entry of ENTRIES) {
  const src = path.join(ROOT, entry);
  if (!fs.existsSync(src)) {
    throw new Error(`Missing required path: ${entry}`);
  }
  copy(src, path.join(DIST, entry));
}

fs.copyFileSync(path.join(ROOT, "index.html"), path.join(DIST, "404.html"));

const files = [];
(function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (fs.statSync(p).isDirectory()) walk(p);
    else files.push(p);
  }
})(DIST);

const bytes = files.reduce((n, f) => n + fs.statSync(f).size, 0);
console.log(`Built dist/ with ${files.length} files (${(bytes / 1024 / 1024).toFixed(1)} MiB)`);
