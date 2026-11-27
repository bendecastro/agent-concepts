import { readFileSync } from "node:fs";

export default function (pi) {
  const kernel = readFileSync(new URL("./AGENT-KERNEL.md", import.meta.url), "utf8");
  pi.on("before_agent_start", (event) => {
    event.systemPromptOptions.sections["agent-kernel"] = kernel;
  });
}
