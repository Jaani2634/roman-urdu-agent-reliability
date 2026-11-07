# Benchmark vs Real Work: How Reliable Is an AI Agent in Roman Urdu?

English paper (v8) + supplementary data for a single-pass evaluation of Gemini 3.5 Flash-Lite on 40 Roman Urdu tasks, each run twice: once in clean benchmark phrasing, once in informal real-world phrasing.

## Headline results

- Benchmark: **94.6% (35/37)**; real-world: **89.5% (34/38)**; overall **92.0% (69/75)**
- Gap: **5.1 percentage points**, not statistically significant (Fisher's exact test, p = 0.67)
- 75 of 80 planned runs measured; 5 API-error failures recorded as unmeasured
- Total recorded tokens: **13,397** (benchmark 6,245; real-world 7,152)

## Contents

- `paper-draft-v8.md` — the paper (English, v8)
- `supplementary/01_tasks_full.csv` — all 40 tasks with exact prompts (both conditions) and expected answers
- `supplementary/02_raw_responses.csv` — all 80 runs with full raw responses
- `supplementary/03_scoring_sheet.csv` — pass/fail for every run with scorer notes
- `supplementary/04_run_code.py` — the experiment code
- `supplementary/05_analysis.py` — recomputes every headline number from the data
- `supplementary/06_missing_tasks.md` — the 5 unmeasured runs and why
- `supplementary/07_pilot_run.csv` — the first (messier) pilot run, original + corrected scores
- `supplementary/README.md` — reproduction steps and notes

## Reproduce the numbers

```bash
python3 supplementary/05_analysis.py
```

## Notes

- The runs used the model's default sampling settings. A temperature of 0 was set in the request but is ignored by this model (Google's documentation: custom temperature/top-K/top-P values are not supported and are ignored; default temperature 1.0 applies), so the results are a single sample from default sampling behaviour, not a deterministic measurement. No thinking level was set; the model ran at its default minimal thinking level.
- Figure images (Fig 1–4) are described in the paper; the source PNGs will be added under `figures/` in a follow-up commit.
- The Roman Urdu version of the paper is not included in this repository (English only, by the author's choice).
