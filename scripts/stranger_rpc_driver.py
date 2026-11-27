"""Drive one Pi RPC session for the stranger test: send a prompt, answer questions, wait until quiet.

Usage: stranger_rpc_driver.py PHASE PROMPT ANSWER QUIET_SECONDS LIMIT_SECONDS [PI_ARGS...]

A long-lived RPC process is used instead of `pi -p` because the pipeline's background
children wake the parent after its first reply; a print-mode process would already have
exited. The first time the agent stops with a question (or, in the build phase, stops at
all) it receives ANSWER; up to two later questions receive FOLLOW_UP, a neutral go-ahead.
Project AGENTS.md files load as they would for a stranger; the sandbox masks the global ones.
STRANGER_PI (default `pi`) is split like a shell command, so it can name the pi_sandbox.py wrapper.
Writes rpc.jsonl, stderr.txt and final.txt under $STRANGER_LOG_DIR/PHASE (default /box/logs).
"""
import json
import os
import queue
import shlex
import subprocess
import sys
import threading
import time

FOLLOW_UP = "Yes, that's fine. Go ahead."
MAX_ANSWERS = 3


def assistant_text(message):
    content = message.get("content")
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") for part in content or [] if isinstance(part, dict))


def main(argv):
    phase, prompt, answer, quiet, limit = argv[0], argv[1], argv[2], float(argv[3]), float(argv[4])
    log_dir = os.path.join(os.environ.get("STRANGER_LOG_DIR", "/box/logs"), phase)
    os.makedirs(log_dir, exist_ok=True)
    log = open(os.path.join(log_dir, "rpc.jsonl"), "a", encoding="utf-8")
    command = [*shlex.split(os.environ.get("STRANGER_PI", "pi")), "--mode", "rpc", "-ne", "--no-mcp",
               "--no-prompt-templates", "--model", os.environ["MODEL"], "--thinking", os.environ["THINKING"],
               "--session-dir", os.path.join(log_dir, "session"), *argv[5:]]
    stderr = open(os.path.join(log_dir, "stderr.txt"), "a", encoding="utf-8")
    pi = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
    events = queue.Queue()

    def read():
        buffer = b""
        for chunk in iter(lambda: pi.stdout.read1(65536), b""):
            buffer += chunk
            while b"\n" in buffer:  # split on LF only; JSON may contain U+2028
                line, buffer = buffer.split(b"\n", 1)
                log.write(line.decode("utf-8", "replace") + "\n")
                log.flush()
                try:
                    events.put(json.loads(line))
                except ValueError:
                    pass
        events.put(None)

    threading.Thread(target=read, daemon=True).start()

    def send(record):
        pi.stdin.write((json.dumps(record) + "\n").encode())
        pi.stdin.flush()

    send({"id": "p0", "type": "prompt", "message": prompt})
    start = last = time.monotonic()
    settled, answers, final = False, 0, ""
    while time.monotonic() - start < limit:
        try:
            event = events.get(timeout=min(5, quiet))
        except queue.Empty:
            if settled and time.monotonic() - last > quiet:
                asked = "?" in final[-600:]
                if answers < MAX_ANSWERS and (asked or (phase == "build" and answers == 0)):
                    reply = answer if answers == 0 and answer else FOLLOW_UP
                    answers += 1
                    settled, last = False, time.monotonic()
                    print(f"[{phase}] answer {answers}", flush=True)
                    send({"id": f"p{answers}", "type": "prompt", "message": reply})
                    continue
                break
            continue
        if event is None:
            print(f"[{phase}] pi exited", flush=True)
            break
        kind, last = event.get("type"), time.monotonic()
        if kind == "agent_settled":
            settled = True
        elif kind in ("agent_start", "message_start", "tool_execution_start"):
            settled = False
        if kind == "message_end" and event.get("message", {}).get("role") == "assistant":
            final = assistant_text(event["message"])
        elif kind == "extension_ui_request" and event.get("method") == "confirm":
            send({"type": "extension_ui_response", "id": event["id"], "confirmed": True})
            print(f"[{phase}] confirmed: {event.get('title')}", flush=True)
        elif kind == "extension_ui_request" and event.get("method") in ("select", "input", "editor"):
            send({"type": "extension_ui_response", "id": event["id"], "cancelled": True})
            print(f"[{phase}] cancelled {event.get('method')}: {event.get('title')}", flush=True)
    else:
        print(f"[{phase}] time limit", flush=True)
    with open(os.path.join(log_dir, "final.txt"), "w", encoding="utf-8") as handle:
        handle.write(final)
    pi.stdin.close()
    try:
        pi.wait(30)
    except subprocess.TimeoutExpired:
        pi.kill()
    return answers


if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    main(sys.argv[1:])
