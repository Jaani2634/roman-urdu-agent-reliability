#!/usr/bin/env python3
"""Clean re-run (Stage 4 fix): ONE attempt per task/condition, temperature 0,
maxOutputTokens 1024, finishReason + full raw response recorded.
Retries happen ONLY for API errors, and every retry is logged in the record.
Records are append-only: once a pair has a successful record it is never overwritten.
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.expanduser("~/workspace/research-topic1"))
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
from run_experiment import TASKS

BASE = os.path.expanduser("~/workspace/research-topic1")
OUT = os.path.join(BASE, "clean-results.jsonl")
RAW = os.path.join(BASE, "clean-raw.jsonl")
MODEL = "gemini-3.5-flash-lite"
TEMPERATURE = 0
MAX_TOKENS = 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused")


def call_api(prompt):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": MAX_TOKENS, "temperature": TEMPERATURE},
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=data, method="POST")
    req.add_header("User-Agent", "Muse-Gemini-Test/1.0")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.gemini",
                             allowed_hosts=["generativelanguage.googleapis.com"])
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=90) as resp:
        return read_json_response(resp)


def main():
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                d = json.loads(line)
                done.add((d["task"], d["condition"]))
            except Exception:
                pass
    print(f"resuming: {len(done)} pairs already recorded", flush=True)
    n = 0
    for tid, cat, bench, real, expected, rule in TASKS:
        for cond, prompt in (("benchmark", bench), ("real", real)):
            if (tid, cond) in done:
                continue
            errors = []
            result = None
            attempts = 0
            latency = None
            for a in range(1, 6):
                attempts = a
                t0 = time.time()
                try:
                    result = call_api(prompt)
                    latency = round(time.time() - t0, 2)
                    # validate shape
                    _ = result["candidates"][0]["content"]["parts"][0]["text"]
                    break
                except Exception as e:
                    errors.append(f"attempt {a}: {type(e).__name__}: {str(e)[:120]}")
                    result = None
                    time.sleep(8)
            if result is None:
                rec = {"task": tid, "category": cat, "condition": cond, "prompt": prompt,
                       "expected": expected, "response": None, "finish_reason": None,
                       "latency_s": None, "tokens": None, "attempts": attempts,
                       "api_errors": errors, "error": "FAILED after 5 attempts",
                       "model": MODEL, "temperature": TEMPERATURE,
                       "max_output_tokens": MAX_TOKENS,
                       "date": "2026-11-05", "auto_score": None}
                with open(OUT, "a") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"{tid}/{cond} FAILED after {attempts} attempts", flush=True)
                continue
            cand = result["candidates"][0]
            text = cand["content"]["parts"][0]["text"]
            rec = {"task": tid, "category": cat, "condition": cond, "prompt": prompt,
                   "expected": expected, "response": text,
                   "finish_reason": cand.get("finishReason"),
                   "latency_s": latency,
                   "tokens": result.get("usageMetadata", {}).get("totalTokenCount"),
                   "attempts": attempts, "api_errors": errors, "error": None,
                   "model": MODEL, "temperature": TEMPERATURE,
                   "max_output_tokens": MAX_TOKENS,
                   "date": "2026-11-05", "auto_score": None}
            with open(OUT, "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            with open(RAW, "a") as f:
                f.write(json.dumps({"task": tid, "condition": cond, "raw": result},
                                   ensure_ascii=False) + "\n")
            n += 1
            print(f"{tid}/{cond} OK attempts={attempts} finish={rec['finish_reason']} "
                  f"lat={latency}s tok={rec['tokens']} len={len(text)}", flush=True)
            time.sleep(2)
    print("DONE", n, "new successful records", flush=True)


if __name__ == "__main__":
    main()
