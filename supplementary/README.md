# Supplementary material

Paper: "Benchmark Versus Real Work: How Reliable Is an AI Agent in Roman Urdu?"
(Junaid Nazeer, independent researcher, Pakistan.) This folder holds every file
needed to check the paper's numbers from the raw data. No repository link
exists yet; the files will be deposited in a public repository (OSF, Zenodo,
or GitHub) on upload, and the link will be added to the paper's Data
Availability section.

## Files

| File | Contents |
|---|---|
| 01_tasks_full.csv | All 40 tasks: task ID, original category (as designed in Stage 1), analysis category (as analysed in the paper, v8), the exact benchmark and real-world prompts, and the expected answer. 40 records. |
| 02_raw_responses.csv | All 80 runs: task, condition, exact prompt, expected answer, the model's full response, finish reason, latency, token count, number of response parts, attempts, API errors, model and settings. 80 records. |
| 03_scoring_sheet.csv | All 80 runs: score (1/0, blank where unmeasured), scoring method, and a one-line grading note for every run. 80 records. |
| 04_run_code.py | The exact code that ran the clean experiment (`run_clean.py`, copied verbatim). It set `temperature = 0` and `max_output_tokens = 1024` in the request. |
| 05_analysis.py | Recomputes every headline number in the paper from 02 and 03 (rates, category rates, Fisher's exact test, latency distribution, token totals, retries, split responses). Pure standard library; run `python3 05_analysis.py`. |
| 06_missing_tasks.md | The 5 unmeasured runs and why each failed. |
| 07_pilot_run.csv | The earlier, messier pilot run (75 records) with the original auto-score and a corrected score. See below. |
| README.md | This file. |

## Facts a re-user needs

**Sampling settings.** The request set a temperature of 0, but Google's
official model documentation for Gemini 3.5 Flash-Lite states that custom
values for temperature, top-K, and top-P are not supported and are ignored by
the API, which applies its default temperature of 1.0. The runs are therefore
a single sample from the model's default sampling behaviour, not a
deterministic measurement. No thinking level was set in the request, so the
model ran at its default minimal thinking level (Google's model documentation
states that 3.5 Flash-Lite defaults to minimal thinking).

**Category reclassification (v8).** Four items designed under Category A are
single-step arithmetic, not factual recall: A2 (15% of 2,500), A6 (minutes in
3 h 45 min), A8 (10% discount on Rs 800), A10 (7 x 8 + 12). They are analysed
under Category C. Analysed sizes are therefore A 6, B 10, C 14, D 10. The
original assignment is preserved in the `original_category` column of 01 and
02. The headline totals (35/37, 34/38, 69/75) are unaffected, because the move
is within conditions.

**Pilot re-grading (07).** The pilot's own summary reported a 6.1-point gap
(88.6% vs 82.5%) because its grader counted the stale 2024 Ramadan date as
correct (the substring "20" inside "2024" matched). Re-grading that one
answer with the fixed word-boundary rule gives 80.0% in the real-world
condition and a gap of 8.6 points, which is the figure the paper reports.
The `corrected_score` column records the re-grading; `auto_score` is the
pilot's original score. Category B and D pilot grades were manual and are
taken from the pilot summary (stage2-results.md, sections 2 and 4); the
correction notes name the reason for each failing grade.

**Figures.** The paper numbers figures in order of first mention. The image
files keep their original names: Figure 1 (experimental design) is
`fig4-design.png`, Figure 2 (headline result) is `fig1-overall.png`,
Figure 3 (results by category) is `fig2-categories.png`, Figure 4 (failures)
is `fig3-failures.png`. The figure files sit beside the paper draft, not in
this folder.

**Task IDs.** A1-A10 factual questions, B1-B10 data tasks, C1-C10 arithmetic
and logic, D1-D10 multi-step tasks. Each task was run twice: `benchmark`
(clean, complete phrasing) and `real` (informal, real-world phrasing).
Expected answers are in 01; grading rules are in the paper, Section 3.4.

## How to reproduce the headline numbers

```
python3 05_analysis.py
```

Expected: benchmark 35/37 = 94.6%, real 34/38 = 89.5%, overall 69/75 =
92.0%, Fisher's exact p = 0.67; tokens benchmark 6245, real 7152, total
13397; 28 of 80 runs needed at least one retry; 23 of 75 responses arrived
split across parts; all 75 finish reasons STOP (no truncations).
