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


BUILD_PI = r'''#!/usr/bin/env python3
import json, sys
for line in sys.stdin:
    with open("prompts.txt", "a") as f:
        f.write(json.loads(line)["message"] + "\n")
    for event in ({"type": "agent_start"},
                  {"type": "message_end", "message": {"role": "assistant",
                   "content": [{"type": "text", "text": "Please confirm the source? Still waiting?"}]}},
                  {"type": "agent_settled"}):
        print(json.dumps(event), flush=True)
'''


def run_driver(tmp_path, script, phase, first_reply):
    fake = tmp_path / "fake-pi"
    fake.write_text(script)
    fake.chmod(0o755)
    env = {**os.environ, "STRANGER_PI": str(fake), "STRANGER_LOG_DIR": str(tmp_path / "logs"),
           "MODEL": "p/m", "THINKING": "low"}
    subprocess.run([sys.executable, str(DRIVER), phase, "Start", "Scripted answer.", "0.2", "20"],
                   cwd=tmp_path, env=env, check=True, timeout=30)
    return (tmp_path / "prompts.txt").read_text().splitlines()


def test_build_phase_answers_a_stop_that_is_not_a_question(tmp_path):
    script = FAKE_PI.replace('replies = ["Which layout?", "Is that test seam okay?", "Done."]',
                             'replies = ["Please authenticate gh or confirm the source.", "Done.", "Done."]')
    assert run_driver(tmp_path, script, "build", None) == ["Start", "Scripted answer."]


def test_plan_phase_does_not_answer_a_stop_that_is_not_a_question(tmp_path):
    script = FAKE_PI.replace('replies = ["Which layout?", "Is that test seam okay?", "Done."]',
                             'replies = ["Please authenticate gh or confirm the source.", "Done.", "Done."]')
    assert run_driver(tmp_path, script, "plan", None) == ["Start"]


def test_answers_stop_after_three(tmp_path):
    assert run_driver(tmp_path, BUILD_PI, "plan", None) == [
        "Start", "Scripted answer.", "Yes, that's fine. Go ahead.", "Yes, that's fine. Go ahead."]


def test_plan_phase_answers_a_numbered_choice_without_a_question_mark(tmp_path):
    # Attempt 3 of the 2026-11-27 rerun: the planner's dependency question ended
    # "Reply `1` or `2`." with no "?", and the driver ended the phase unanswered.
    script = FAKE_PI.replace('replies = ["Which layout?", "Is that test seam okay?", "Done."]',
                             'replies = ["1. **Recommended:** add it.\\n2. Do not.\\n\\nReply `1` or `2`.", "Done.", "Done."]')
    assert run_driver(tmp_path, script, "plan", None) == ["Start", "Scripted answer."]


def test_follow_up_answer_comes_from_the_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("STRANGER_FOLLOW_UP", "Not sure yet; anything else is fine.")
    assert run_driver(tmp_path, BUILD_PI, "plan", None) == [
        "Start", "Scripted answer.", "Not sure yet; anything else is fine.", "Not sure yet; anything else is fine."]
