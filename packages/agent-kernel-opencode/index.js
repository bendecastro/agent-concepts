import { readFileSync } from "node:fs";

// OpenCode V2's Plugin.define returns this descriptor unchanged.
export default {
  id: "agent-kernel",
  async setup(ctx) {
    const text = readFileSync(new URL("./AGENT-KERNEL.md", import.meta.url), "utf8");
    await ctx.session.hook("context", (event) => {
      event.system.push({ type: "text", text });
    });
  },
};
