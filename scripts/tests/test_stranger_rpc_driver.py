"""The stranger RPC driver answers each question once, then stops when the agent goes quiet."""
import json
import os
import subprocess
import sys
from pathlib import Path

DRIVER = Path(__file__).resolve().parents[1] / "stranger_rpc_driver.py"

FAKE_PI = r'''#!/usr/bin/env python3
import json, sys
replies = ["Which layout?", "Is that test seam okay?", "Done."]
for n, line in enumerate(sys.stdin):
    prompt = json.loads(line)["message"]
    with open("prompts.txt", "a") as f:
        f.write(prompt + "\n")
    for event in ({"type": "agent_start"},
                  {"type": "message_end", "message": {"role": "assistant",
                   "content": [{"type": "text", "text": replies[min(n, 2)]}]}},
                  {"type": "agent_settled"}):
        print(json.dumps(event), flush=True)
'''


def test_driver_answers_each_question_then_stops(tmp_path):
    fake = tmp_path / "fake-pi"
    fake.write_text(FAKE_PI)
    fake.chmod(0o755)
    env = {**os.environ, "STRANGER_PI": str(fake), "STRANGER_LOG_DIR": str(tmp_path / "logs"),
           "MODEL": "p/m", "THINKING": "low"}
    subprocess.run([sys.executable, str(DRIVER), "plan", "Plan it", "Use the proposed layout.", "0.2", "20"],
                   cwd=tmp_path, env=env, check=True, timeout=30)
    assert (tmp_path / "prompts.txt").read_text().splitlines() == [
        "Plan it", "Use the proposed layout.", "Yes, that's fine. Go ahead."]
    assert (tmp_path / "logs" / "plan" / "final.txt").read_text() == "Done."
    records = [json.loads(line) for line in (tmp_path / "logs/plan/rpc.jsonl").read_text().splitlines()]
    assert sum(r["type"] == "agent_settled" for r in records) == 3
