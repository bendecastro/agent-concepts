#!/usr/bin/env node
// `agent-concepts kernel install|remove <file>`: runs install.py beside this file,
// so the marked-block logic has one implementation. Needs python3 on PATH.
"use strict";
const { spawnSync } = require("node:child_process");
const path = require("node:path");

const usage = "usage: agent-concepts kernel install|remove <instructions-file>\n";
const [group, action, file, ...extra] = process.argv.slice(2);
if (group !== "kernel" || !["install", "remove"].includes(action) || !file || extra.length) {
  process.stderr.write(usage);
  process.exit(2);
}
const installer = path.join(__dirname, "install.py");
const args = ["-I", installer, path.resolve(file)];
if (action === "remove") args.push("--remove");
const result = spawnSync("python3", args, { stdio: "inherit" });
if (result.error) {
  process.stderr.write(`agent-concepts: cannot run python3 (${result.error.message}); install Python 3\n`);
  process.exit(1);
}
process.exit(result.status === null ? 1 : result.status);
