#!/usr/bin/env python3
"""Recompute every headline number in the paper from the supplementary CSVs.

Reads 02_raw_responses.csv and 03_scoring_sheet.csv from this directory and
prints: headline success rates per condition, category rates, Fisher's exact
test (two-sided, pure stdlib via math.comb), latency distribution (min, Q1,
median, Q3, max) per condition, token totals per condition, retry counts and
split-response counts. No third-party packages needed.

Expected output (paper v8):
  benchmark 35/37 = 94.6%, real 34/38 = 89.5%, overall 69/75 = 92.0%,
  Fisher p = 0.67; tokens benchmark 6245, real 7152, total 13397;
  28 of 80 runs needed at least one retry; 23 of 75 responses split.
"""
import csv, math, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))


def q(p, xs):
    xs = sorted(xs)
    i = (len(xs) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def fisher_two_sided(a, b, c, d):
    # 2x2 table [[a, b], [c, d]]; two-sided p by summing probabilities of
    # tables no more likely than the observed one (Fisher's exact test).
    n = a + b + c + d
    r1, r2 = a + b, c + d
    c1, c2 = a + c, b + d

    def prob(x):
        # x = top-left cell value
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    p_obs = prob(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12)


def main():
    raw = list(csv.DictReader(open(os.path.join(HERE, "02_raw_responses.csv"),
                                   encoding="utf-8")))
    scores = {(r["task_id"], r["condition"]): r
              for r in csv.DictReader(open(os.path.join(HERE, "03_scoring_sheet.csv"),
                                           encoding="utf-8"))}
    meas = [r for r in raw if r["response"].strip()]
    print(f"records: {len(raw)}, measured: {len(meas)}, "
          f"unmeasured: {len(raw) - len(meas)}")
    for cond in ("benchmark", "real"):
        s = [r for r in meas if r["condition"] == cond]
        ok = sum(1 for r in s if scores[(r["task_id"], cond)]["score"] == "1")
        print(f"{cond}: {ok}/{len(s)} = {ok / len(s) * 100:.1f}%")
    ok = sum(1 for r in meas
             if scores[(r["task_id"], r["condition"])]["score"] == "1")
    print(f"overall: {ok}/{len(meas)} = {ok / len(meas) * 100:.1f}%")
    for cat in ("A", "B", "C", "D"):
        for cond in ("benchmark", "real"):
            s = [r for r in meas
                 if r["category_analysis"] == cat and r["condition"] == cond]
            o = sum(1 for r in s
                    if scores[(r["task_id"], cond)]["score"] == "1")
            print(f"category {cat} {cond}: {o}/{len(s)} = "
                  f"{o / len(s) * 100:.1f}%")
    b = [r for r in meas if r["condition"] == "benchmark"]
    r_ = [r for r in meas if r["condition"] == "real"]
    bp = sum(1 for r in b if scores[(r["task_id"], "benchmark")]["score"] == "1")
    rp = sum(1 for r in r_ if scores[(r["task_id"], "real")]["score"] == "1")
    p = fisher_two_sided(bp, len(b) - bp, rp, len(r_) - rp)
    print(f"Fisher exact p (two-sided): {p:.2f}")
    for cond in ("benchmark", "real"):
        lat = [float(r["latency_s"]) for r in meas
               if r["condition"] == cond and r["latency_s"]]
        print(f"latency {cond}: n={len(lat)} min={min(lat)} "
              f"Q1={q(0.25, lat):.2f} median={statistics.median(lat)} "
              f"Q3={q(0.75, lat):.2f} max={max(lat)}")
    for cond in ("benchmark", "real"):
        tok = sum(int(r["tokens"]) for r in meas
                  if r["condition"] == cond and r["tokens"])
        print(f"tokens {cond}: {tok}")
    print(f"tokens total: "
          f"{sum(int(r['tokens']) for r in meas if r['tokens'])}")
    print(f"runs needing at least one retry: "
          f"{sum(1 for r in raw if r['attempts'] and int(r['attempts']) > 1)}"
          f" of {len(raw)}")
    print(f"responses split across parts: "
          f"{sum(1 for r in meas if r['response_parts'] and int(r['response_parts']) > 1)}"
          f" of {len(meas)}")
    print(f"finish reasons: "
          f"{sorted(set(r['finish_reason'] for r in meas))}")


if __name__ == "__main__":
    main()
