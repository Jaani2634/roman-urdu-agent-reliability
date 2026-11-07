# Benchmark Versus Real Work: How Reliable Is an AI Agent in Roman Urdu?

**Junaid Nazeer**
Independent Researcher, Pakistan

---

## Abstract

Benchmarks have become the default language in which the field talks about AI agents: a benchmark is cheap to run, easy to repeat, and straightforward to compare across systems. Yet a benchmark measures performance under conditions far cleaner than those in which ordinary people use these systems, so a score earned on tidy prompts says surprisingly little about what happens when a real user writes in a hurry, in their own dialect, with missing details. This paper measures that difference directly, in a language the evaluation literature has almost entirely ignored, by taking forty tasks written in Roman Urdu, the everyday written language of tens of millions of Pakistanis, and asking a single commercial model, Gemini 3.5 Flash-Lite, to complete each task twice: once in the clean, complete phrasing a benchmark would use, and once in the informal, abbreviated, sometimes ungrammatical phrasing an ordinary user would actually write. The experiment was run as a single-pass evaluation at the model's default settings, with one attempt per task and a 1,024-token output allowance. Of the eighty planned runs, seventy-five produced usable measurements. First-attempt success reached 94.6 percent (35 of 37) in the benchmark condition and 89.5 percent (34 of 38) in the real-world condition, a gap of 5.1 percentage points that is not statistically significant (Fisher's exact test, p = 0.67). The gap is unevenly distributed: factual questions fell from 83.3 percent (5 of 6) to 66.7 percent (4 of 6), data tasks from 90 percent to 88.9 percent, arithmetic was perfect in both conditions (14 of 14), and multi-step tasks fell from 100 percent (7 of 7 attempted) to 88.9 percent. Beyond the numbers, the experiment surfaced failures no single score can capture: the model answering that Muse, Meta's AI assistant, belongs to no company, giving a stale answer from 2024 to a question about 2026, counting thirteen words and then reporting fifteen, and inventing expenses that were never requested. Benchmark scores slightly overstate real-world reliability for Roman Urdu users, and script fidelity and locale fidelity deserve to be treated as first-class measures of reliability rather than cosmetic details. All tasks, prompts, and raw results are released openly as supplementary material with this paper.

**Keywords:** AI agents, benchmarking, reliability, Roman Urdu, low-resource languages, evaluation gap

---

## 1. Introduction

Anyone who has spent time with an AI agent will recognise the experience: you ask it something in the ordinary way you would ask a colleague, quickly and imperfectly, and the answer that comes back is either impressively capable or quietly wrong in a way that takes a moment to notice. What makes this experience difficult to study is that benchmarks, the instruments the field uses to judge agents, do not resemble it at all. A benchmark prompt is written by a researcher, checked for clarity, stripped of ambiguity, and presented in isolation, whereas a real prompt is written by a person who is busy, who assumes shared context that is not actually shared, and who writes in the language they think in rather than the language a test designer would choose. For speakers of Roman Urdu, this distance between the test and the reality is wider than for almost anyone else, because Roman Urdu is everywhere in daily life, in messages, in comments, in search queries, and almost nowhere in the evaluation literature, which means that the reliability of agents in this language has simply never been measured in any systematic way.

The question this paper asks is therefore a deliberately simple one: when the same task is given to the same agent in the way a benchmark would phrase it and in the way a real user would phrase it, how much of the benchmark performance survives the journey into ordinary language? If the two numbers agree, benchmark scores are a fair guide to real use. If they disagree, the size, shape, and reasons behind the gap become findings in their own right.

The contributions of this paper are threefold. First, I release a forty-task Roman Urdu evaluation set with explicit expected answers and grading rules, to the best of my knowledge the first of its kind for agent reliability in this language. Second, I report measured, not assumed, performance: seventy-five completed runs with success rates, latencies, and token counts, recorded from a real API rather than estimated from a brochure, in a single clean pass at the model's default settings with one attempt per task. Third, I document failure modes that a single score hides: a knowledge gap about which company develops Muse, Meta's AI assistant, stale knowledge, counting errors, invented constraints, and a summary that drops a required element, which matter more to a Roman Urdu user than a few points of accuracy ever will. The remainder of this paper is organized as follows: Section 2 places the work in the context of recent research on agent evaluation, Section 3 describes the task set, the two conditions, and the grading procedure in enough detail for anyone to repeat it, Section 4 presents the results, Section 5 discusses what they mean and what they do not mean, Section 6 states the limitations, and Section 7 concludes. The scope is deliberately narrow: one model, one language, single-turn tasks. Adversarial prompts, multi-turn dialogue, other languages, and reinforcement-learning agents are left for future work.

## 2. Related Work

The idea that benchmark performance and deployed performance are different things is not new, and the recent literature on agent evaluation has made the point with increasing force. Kehkashan et al. (2026), in a comprehensive review of agentic AI evaluation published in *Artificial Intelligence Review*, argue that benchmark results often fail to predict how an agent will behave once it is deployed, and that evaluation itself remains a weak and underdeveloped science, a judgement that carries weight because it comes from a wide survey of the field rather than a single anecdote. Shukla (2025) reaches a similar conclusion from a different angle, reporting Mehta et al.'s finding that leading agents exhibit up to 50x cost variation for similar accuracy, which means that a single accuracy number, however precisely measured, cannot tell a user what an agent will actually cost them or how it will actually feel to use.

Rabanser et al. (2026) attempt to put agent reliability on a genuinely scientific footing, testing across two well-known benchmarks and across conditions. Their central insight, that reliability is not a single number but changes with the conditions under which it is measured, is the starting point for this paper: reliability must be measured conditionally rather than assumed globally, and any study which reports one number and stops there is hiding more than it reveals. Ndzomga (2026) adds a practical observation which matters a great deal for a study like ours, showing that reliable rankings of agents can be obtained without running an entire benchmark, and thereby supporting the use of a small, inexpensive task set such as the one I employ here. Zhu et al. (2025) provide a checklist for building rigorous agent benchmarks, task validity, outcome validity, and benchmark validity, which I follow in Section 3, while surveys by Mohammadi et al. (2025) and Baduwal and Paudel (2026) confirm that the evaluation of agents, including the evaluation of agents interacting with one another, remains an open problem, and Bragg et al. (2026) demonstrate what rigorous benchmarking looks like when it is done properly in a scientific setting.

Two gaps remain, and they are the gaps this paper is designed to fill. The first is a gap of language: the literature evaluates agents almost entirely in English, and the reliability of agents in Roman Urdu, a language spoken and written by tens of millions of people, has not been measured at all. The second is a gap of comparison: the literature compares models against one another far more often than it compares conditions against one another, so the field knows a great deal about which model scores higher and very little about how much any model's score would fall if the prompts were written the way users actually write them. My work fills both gaps at a modest scale: one language that the literature ignores, and one comparison, benchmark phrasing against real phrasing, that the literature rarely makes.

---

## 3. Methodology

### 3.1 Task set

I wrote forty tasks in Roman Urdu, divided into four categories of ten tasks each as designed, and the division itself deserves a brief explanation, because the categories were chosen to span the range from the easiest thing an agent can be asked to the kind of work that most resembles what a real user actually needs. Category A, factual questions, covers general knowledge and simple facts: the population of Pakistan, the full name of Quaid-e-Azam, which company develops the AI assistant Muse, and the date of the first fast of Ramadan in 2026. Category B, data tasks, covers sorting, counting, summarising, tabulating, and drafting, and tests whether the model can manipulate small amounts of structured information without losing track of it. Category C, arithmetic and logic, covers calculations and sequences, and tests whether the model can follow a short chain of reasoning to a single correct answer. Category D, multi-step tasks, covers work with two or more dependent parts, and tests whether the model can complete every part of a job rather than merely starting it well.

On review, four items placed in Category A are single-step arithmetic, not factual recall: A2 (15 percent of 2,500), A6 (minutes in 3 hours 45 minutes), A8 (a 10 percent discount on Rs 800), and A10 (7 x 8 + 12). They are analysed under Category C, so the analysed sizes are A 6, B 10, C 14, D 10. The original assignment is preserved in the supplementary task file, and the headline totals are unaffected by the move, since it is within conditions. Each task has a single expected answer and a binary grading rule, correct (1) or incorrect (0), with no partial credit, and the full task set is listed in the Appendix.

### 3.2 The two conditions

Every task was run in two conditions, and the distinction between them is the heart of the experiment. In the **benchmark condition**, the task was presented exactly as written: a clean, complete, grammatically correct prompt containing all the information needed to answer it, with nothing left implicit and nothing left to guess. In the **real-world condition**, the same task was rewritten the way an ordinary user writes: informally, briefly, sometimes ungrammatically, with filler words and without polite framing, for example, "2500 ka 15 percent nikal do jaldi" instead of "15% of 2,500 kitna hota hai?", and the underlying task and the expected answer were identical in both conditions, so that only the phrasing changed and any difference in outcome can be attributed to the phrasing rather than to the task itself. Figure 1 shows the design of the experiment: forty tasks, each run twice, once in benchmark phrasing and once in real-world phrasing, with the expected answer identical in both conditions, so that only the phrasing changes.

![Figure 1. Experimental design. Each of the forty tasks was run twice, once in benchmark phrasing and once in real-world phrasing, with the expected answer identical in both conditions. The comparison isolates the effect of phrasing alone.](fig4-design.png)

### 3.3 Model and procedure

The agent under test was Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`), accessed through Google's public API, and it was chosen because it is a fast, widely available commercial model of the kind an ordinary user would actually encounter, rather than a research prototype or a frontier system. Each task was presented once per condition, with no system instructions, no examples, and no conversation history, so that the model received only the task prompt itself and nothing else. Three details of the procedure affect how the results should be read. First, all tasks were run in a single pass with Gemini 3.5 Flash-Lite (model ID: gemini-3.5-flash-lite). Although a temperature of 0 was set in the request, this parameter is not supported for custom values on this model and is ignored by the API, which applies its default temperature of 1.0. The runs are therefore not deterministic, and the results should be read as a single sample from the model's default sampling behaviour rather than as a reproducible deterministic measurement. The generation call used a maximum output of 1,024 tokens, and no response in this study was truncated. No thinking level was set in the request, so the model ran at its default minimal thinking level (Google's model documentation states that 3.5 Flash-Lite defaults to minimal thinking). Second, each task was attempted exactly once per condition. Where the API returned an error, most often a "503 Service Unavailable", the call was retried, and the retry was logged: 28 of the 80 runs needed at least one retry, and 5 runs still failed after five attempts each. Those five failures are recorded in the data file as unmeasured, not deleted, and the paper reports the range they imply rather than pretending they never happened. Third, the API sometimes returned a response split across two parts, and the full response was reconstructed by joining all parts before grading, because grading only the first part would have scored several correct answers as failures. I recorded the full response, the response latency, and the token count for every call.

The experiment was run in a single session, each response read in full as it arrived and each failure inspected before it was classified. The observations in Section 4.7 were recorded during the run, not reconstructed afterwards.

### 3.4 Grading

Categories A and C were graded automatically by checking for the expected value in the response, for example, "375" for a fifteen-percent calculation, or "Jinnah" for the Quaid-e-Azam question, with word-boundary matching and manual review of every mismatch (substring matching can miss answers given in words, and can match the wrong thing, as Section 4.4 shows). Categories B and D were graded by hand against the task rubric by a single grader, myself, using the recorded transcripts, and a response counted as correct only if it contained the expected answer or satisfied every part of the task. No partial credit was given anywhere in the study. Every grade, automatic or manual, is recorded in the supplementary scoring sheet with a one-line note explaining it, so that any reader can audit the scoring without taking my word for it.

### 3.5 Analysis

The primary measure is the first-attempt success rate in each condition and the difference between them, where "first-attempt" means exactly one attempt per task at the model's default settings. I also report success rates by category, response latency, and a taxonomy of failures, and differences were tested with Fisher's exact test, which is appropriate for small counts and does not assume large samples. Five tasks could not be measured because the API returned errors even after five attempts each; I report the range those missing tasks imply rather than a single number. No response in this study was truncated, so no sensitivity analysis for truncation was needed.

---

## 4. Results

### 4.1 Headline result

Of the eighty planned runs, seventy-five produced usable measurements, while five runs (B10 in the real-world condition; D2, D3, and D5 in the benchmark condition; D3 in the real-world condition) could not be completed because the API returned repeated "503 Service Unavailable" errors even after five attempts each, and five missing tasks out of eighty is not trivial: both scores below are measured on slightly smaller sets than the full forty tasks. Figure 2 shows the headline result. First-attempt success reached 94.6 percent (35 of 37) in the benchmark condition and 89.5 percent (34 of 38) in the real-world condition, a gap of 5.1 percentage points that is not statistically significant (Fisher's exact test, p = 0.67), and overall success across both conditions was 92.0 percent (69 of 75). If all five unmeasured tasks had passed, the rates would have been 95.0 percent and 90.0 percent; if all five had failed, they would have been 87.5 percent and 85.0 percent. The honest reading of these numbers is therefore a modest one: benchmark phrasing does better, but not by an amount that this sample can certify, and the gap should be treated as an indication to investigate further rather than a conclusion in itself.

![Figure 2. Headline result. First-attempt success was 94.6 percent (35 of 37) in the benchmark condition and 89.5 percent (34 of 38) in the real-world condition, a gap of 5.1 points (p = 0.67). Five tasks could not be measured because of API outages.](fig1-overall.png)

| Category | Benchmark (pass / attempted) | Real-world (pass / attempted) |
|---|---|---|
| A. Factual questions | 5 / 6 (83.3%) | 4 / 6 (66.7%) |
| B. Data tasks | 9 / 10 (90.0%) | 8 / 9 (88.9%) |
| C. Arithmetic and logic | 14 / 14 (100%) | 14 / 14 (100%) |
| D. Multi-step tasks | 7 / 7 (100%) | 8 / 9 (88.9%) |
| **Total** | **35 / 37 (94.6%)** | **34 / 38 (89.5%)** |

Table 1. Success by category and condition. Counts are shown beside every percentage, because the denominators differ: three multi-step tasks and one data task could not be measured. Category A has six tasks and Category C fourteen, after four single-step arithmetic items (A2, A6, A8, A10) were moved from A to C; see Section 3.1.

### 4.2 Results by category

Figure 3 shows where the gap sits, and its location is more informative than its size. Factual questions showed the clearest difference: 83.3 percent against 66.7 percent, a single task between the conditions, driven by two failures in the real-world condition, the knowledge gap in A4 and the stale date in A5, both discussed in Section 4.4. Data tasks ran at 90 percent benchmark against 88.9 percent real-world, a difference of one task in each direction: the benchmark condition lost B2, where the summary dropped the village, while the real-world condition lost B4, where the model counted thirteen words and reported fifteen. Arithmetic was perfect in both conditions (14 of 14), which is consistent with the idea that short, mechanical reasoning survives informal phrasing almost untouched. Multi-step tasks ran at 100 percent in the benchmark condition (7 of 7 attempted) against 88.9 percent in the real-world condition, a difference of a single task, D5, which is not statistically significant (p = 1.0) and should not be over-read. The pattern across categories is therefore a narrow one: messy phrasing costs a little almost everywhere, and nowhere does it cost a lot.

![Figure 3. Success by category. Factual questions fell from 83.3 percent (5 of 6) to 66.7 percent (4 of 6), data tasks from 90 percent to 88.9 percent, arithmetic was perfect in both conditions (14 of 14), and multi-step tasks fell from 100 percent (7 of 7 attempted) to 88.9 percent.](fig2-categories.png)

### 4.3 Latency and cost

Response latency was close in the two conditions in absolute terms, though not identical. The median was 2.67 seconds in the benchmark condition (minimum 0.9, first quartile 1.21, third quartile 6.25, maximum 62.89) and 2.21 seconds in the real-world condition (minimum 0.98, first quartile 1.33, third quartile 3.47, maximum 12.23). The benchmark maximum of 62.89 seconds is a single slow call (D10); the medians are the fair comparison, and on that measure the real-world condition was, if anything, slightly faster. Total recorded token usage was 13,397 tokens across seventy-five calls: 6,245 in the benchmark condition and 7,152 in the real-world condition. Real-world phrasing did not make the model meaningfully slower or more expensive; whatever it costs the user, it costs in accuracy rather than in time.

### 4.4 What went wrong

Six of the seventy-five measured runs failed, and understanding those six failures is, in my judgement, more valuable than the headline percentages, because a percentage tells you how often something goes wrong while a taxonomy tells you why. No response in this study was truncated, so all six failures are genuine model errors, and they fall into five types:

- **Knowledge gap (2 failures).** Asked which company develops Muse, Meta's AI assistant, the model answered in both conditions that it is not any one company's product, wrong in exactly the same way twice, which suggests a genuine gap in the model's knowledge rather than a slip of phrasing.
- **Stale knowledge (1 failure).** Asked for the first fast of Ramadan in 2026, the model answered with the 2024 date (12 March 2024), confidently and with a precise day. The grading rule was fixed so that the substring "20" inside "2024" could no longer score it as correct, and the error survived the cleaner design.
- **Counting error (1 failure).** Asked to count the words in a thirteen-word paragraph, the model listed thirteen words and then reported a total of fifteen in the real-world condition, contradicting its own list in the very next line. In the benchmark condition the same task was answered correctly after the model first said twelve and then corrected itself to thirteen.
- **Over-elaboration (1 failure).** Asked for a monthly budget with only rent (Rs 12,000), food (Rs 10,000), and the remaining savings from Rs 40,000, the model invented extra categories (bills, transport, medical) and reported savings of Rs 10,000 instead of Rs 18,000, in the real-world condition, and wrote the amounts with the Indian rupee symbol rather than Rs.
- **Summary omission (1 failure).** Asked to summarise a paragraph about a village, an old man, a field, and stories, the model produced a good summary in the benchmark condition that left out the village entirely, which fails the rubric even though the sentence reads well. The same task in real-world phrasing kept all four elements.

Figure 4 shows the six failures at a glance.

![Figure 4. Six failures in seventy-five runs. All six were genuine model errors in five types, led by knowledge gaps (two). No response was truncated.](fig3-failures.png)

### 4.5 The unmeasured five

Five tasks could not be measured, and the honest way to handle them is to state the range they imply rather than to hide them. If all five had passed, the benchmark rate would be 95.0 percent and the real-world rate 90.0 percent; if all five had failed, the rates would be 87.5 percent and 85.0 percent. The gap between the conditions would therefore lie between 2.5 and 5.0 points under the most extreme assumptions, and the headline figures of 94.6 percent and 89.5 percent sit inside those ranges. The missing tasks do not change the conclusion, but they bound how precisely it can be stated; the most cautious reading uses the lower ends of the ranges.

### 4.6 Qualitative observations

Three observations do not appear in the success rates, yet they matter to Roman Urdu users as much as the numbers do. First, **script mixing**: in response to Roman Urdu prompts, the model sometimes slipped a word in another script into an otherwise Roman Urdu answer, a Devanagari fragment in a product description (D7, real-world condition) and a Urdu-script word in a sentence correction (B9, benchmark condition), and while the content was correct, the script was not the one the user had written in. Second, **currency confusion**: the budget answer in D5 used the Indian rupee symbol throughout a Pakistani budget, a small error that reveals how easily a model can drift across a border it was never told about. Third, **stale knowledge**: the Ramadan answer described above was not merely wrong about the year but confidently wrong, offering a precise date from the wrong year with no sign of uncertainty. None of these is captured by a benchmark score, and all of them are exactly the kind of failure a real user notices first.

### 4.7 Observations from running the experiment

Some of what happened during the run changed how I think about the results. First, the API itself behaved unevenly: long stretches of instant answers interrupted without warning by bursts of "503 Service Unavailable" errors, sometimes four failures in a row on the very same prompt that had worked a minute earlier. Five runs never did work, even after five attempts each. Second, twenty-three of the seventy-five responses arrived split across two parts, and the first part alone often looked like a failure, a capital-cities answer that stopped after "In te", a story that stopped mid-sentence, a shopping list that stopped after the first item; joining the parts before grading changed two scores. Third, the script mixing: every prompt was written in Roman Urdu, yet a Devanagari fragment appeared in a product description and a Urdu-script word in a sentence correction, correct in content and wrong in form. The model also counted thirteen words and then announced fifteen, and answered a question about 2026 with a precise date from 2024. None of these moments appears in the tables, but all of them shaped the conclusions: reliability, as a user experiences it, is not a score but a sequence of small moments, most of them fine, a few of them quietly wrong.

---

## 5. Discussion

### 5.1 What the numbers mean

The headline finding is modest, and I would rather state it modestly than overstate it: a 5.1-point gap that could easily be noise, on a sample too small to certify it, in a pilot study that was designed to explore rather than to prove. I do not claim that benchmarks are useless, nor that real-world phrasing destroys performance, and any reader who takes that message from this paper has misunderstood it. What I do claim is narrower, and I think more useful, because it survives the limitations I have been careful to state. First, simple tasks survive messy phrasing almost untouched: arithmetic was perfect in both conditions, and data tasks lost a single task in each direction. Second, the damage is narrow: no category lost more than two tasks in either condition. Third, the failures in this study were genuine model errors rather than infrastructure failures, six of them, none of them a truncated response, which means the gap that remains is a property of the model and not of the serving layer.

### 5.2 What the clean run did not find

An earlier, messier run of this same experiment had suggested that multi-step tasks were the fragile category, with success falling from 75 percent to 60 percent. The clean run does not support that finding. Multi-step tasks ran at 100 percent in the benchmark condition (7 of 7 attempted) and 88.9 percent in the real-world condition, a difference of a single task, D5, and the lost-parts pattern from the earlier run, a missing table, a missing agenda point, a schedule that stopped mid-afternoon, did not appear at all. The only multi-step failure in the clean run was over-elaboration, the model inventing expenses rather than losing parts of the job. The earlier multi-step gap looks like an artifact of a messy first run, with retries, a small token cap, and truncated responses, rather than a stable property of the model. Multi-step work is still where real user work lives, and it still deserves the closest testing, but this study does not show it to be uniquely fragile.

### 5.3 What the clean run changed

This paper reports a clean replication of an earlier, messier run of the same experiment, and the comparison between the two is itself a finding. The headline gap shrank from 8.6 points to 5.1 points. The pilot's own summary reported a 6.1-point gap, because its grader counted the stale 2024 Ramadan date as correct; re-grading that one answer with the fixed word-boundary rule gives 80.0 percent in the real-world condition and a gap of 8.6 points, and the pilot data file records both the original and the corrected score. The multi-step gap shrank from fifteen points to eleven, on a much smaller number of measured tasks, and lost its statistical meaning entirely (p = 1.0). Four truncated responses became zero, because the output allowance was raised from 400 tokens to 1,024. Two things did not change: the model still answered A4 wrong in both conditions, and it still gave the 2024 date for Ramadan 2026 in the real-world condition, even after the grading rule that had once scored that answer as correct was fixed. The lesson I take from the comparison is that a first, messy run overstates the gap and misattributes its causes, and that the discipline of a clean run, one attempt, default settings, logged retries, and auditable grades, is what turns an anecdote into a measurement.

### 5.4 Implications for Roman Urdu users

For a Roman Urdu speaker, the headline accuracy number is not the whole story, and it may not even be the most important part of the story. A model that answers correctly but in the wrong script, or with the wrong currency symbol, has still failed the user in a practical sense, because the user must now do the extra work the model was supposed to save them. Evaluation in Roman Urdu therefore needs to score script fidelity and locale fidelity alongside correctness, which are two measures that do not exist in English benchmarks and which I recommend future work adopt, not as optional extras but as part of what reliability means for this language.

## 6. Limitations

This is a pilot study, and its limits are plain enough that I would rather state them myself than have them pointed out. I acknowledge four limitations:

- **One model, one sampling setting.** Only Gemini 3.5 Flash-Lite was tested, in a single pass at the model's default sampling settings, so the results describe that model under one setting and not agents in general. Because custom sampling parameters are ignored on this model, we could not enforce deterministic decoding. Each task was run once, so sampling variation is not measured in this study. A repeated-runs design would be needed to separate genuine task difficulty from run-to-run variation. The remedy is replication across models and repeated runs, which the released task set makes straightforward.
- **Small sample.** The sample is 75 measured runs, and the headline difference is not statistically significant (p = 0.67). The study was designed to explore, not to prove, and the failure taxonomy is the finding that survives the sample size, not the headline percentage.
- **Five unmeasured tasks.** Five tasks (B10 real-world; D2, D3, and D5 benchmark; D3 real-world) could not be measured at all because of API outages. The direction of the resulting bias is unknown: the benchmark rate would be 95.0 percent if all five had passed and 87.5 percent if all five had failed, and the real-world rate would be 90.0 percent or 85.0 percent, so the honest statement is a range rather than a single number.
- **One grader, artificial tasks.** Grading of categories B and D was done by a single human grader, though every grade is now recorded in the supplementary scoring sheet with a one-line note, so the scoring is auditable. The tasks are artificial rather than drawn from real user logs.

This study is a starting point. It should complement, not replace, larger evaluations with more models, real user logs, and repeated runs; its main value is the task set, the failure taxonomy, and the questions it raises for the next study.

## 7. Conclusion

Benchmark scores slightly overstate how well an AI agent does real Roman Urdu work, by about five points in this single-pass evaluation at the model's default settings, and the gap, while not statistically significant, is spread thinly across categories rather than concentrated where it matters most. The more durable findings, however, are qualitative rather than numerical: the model does not know which company develops Muse, it gives a stale answer from 2024 with confidence, it invents expenses that were never requested, and it mixes scripts and currencies in ways a benchmark score never captures. A first, messier run of this same experiment had suggested a larger gap and a fragile multi-step category; the clean run corrects both claims, and that correction is itself the most useful result of the replication.

The question this paper leaves is therefore not "How often does the agent succeed?" but "How often does it finish the whole job, in the right script, with the right currency, on the first try?" For builders of Roman Urdu agents, the practical lesson is to test with messy, real phrasing, to score the completion of every part rather than merely the final answer, and to treat script and locale fidelity as reliability rather than cosmetics. For evaluators, the lesson is that a benchmark score is a ceiling rather than a promise, and that the distance between the ceiling and the floor is itself worth measuring, carefully, honestly, and more than once.

---

## References

1. Kehkashan, T., Abdullah, M., Al-Shamayleh, A. S., et al. (2026). From benchmarks to deployment: a comprehensive review of agentic AI evaluation. *Artificial Intelligence Review*, 59(8), Article 167. https://doi.org/10.1007/s10462-026-11571-0
2. Rabanser, S., Kapoor, S., Kirgis, P., Liu, K., Utpala, S., et al. (2026). Towards a science of AI agent reliability. arXiv:2602.16666. Accepted at ICML 2026.
3. Ndzomga, F. (2026). Efficient benchmarking of AI agents. arXiv:2603.23749.
4. Shukla, M. (2025). Evaluation and benchmarking of generative and agentic AI systems: A comprehensive survey. Preprints.org. https://doi.org/10.20944/preprints202512.1421.v1. Also SSRN 5927324.
5. Baduwal, M., & Paudel, P. (2026). Evaluating agentic artificial intelligence: A comprehensive survey of metrics, benchmarks, and methodologies. TechRxiv.
6. Bragg, J., D'Arcy, M., Balepur, N., Bareket, D., et al. (2026). AstaBench: Rigorous benchmarking of AI agents with a scientific research suite. ICLR.
7. Mohammadi, M., Li, Y., Lo, J., Yip, W., et al. (2025). Evaluation and benchmarking of LLM agents: A survey. Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining.
8. Zhu, Y., Jin, T., Pruksachatkun, Y., et al. (2025). Establishing best practices for building rigorous agentic benchmarks. NeurIPS 2025, Datasets and Benchmarks track. arXiv:2507.02825. https://doi.org/10.52202/085713-5547
9. Khan, T., Motie, S., Kocak, S. A., & Raza, S. (2025). Optimizing large language models: Metrics, energy efficiency, and case study insights. Proceedings of the IEEE Conference on Artificial Intelligence (CAI 2025), 370-375. arXiv:2504.06307. https://doi.org/10.48550/arXiv.2504.06307
10. Yadav, P. (2026). Energy-efficient lightweight models for Green Artificial Intelligence in language technologies. *Procedia Computer Science*, 275, 175-182.
11. Mehta, S., et al. (2025). CLEAR: A holistic evaluation framework for enterprise agentic AI. arXiv:2511.14136.

---

## Data Availability

The full task set, both prompt versions, raw responses, token counts, latencies, scoring sheet, experiment code, analysis code, missing-task list, and the pilot-run data are supplied as supplementary material with this paper (files 01-07 and README.md in the supplementary folder) and in the public repository https://github.com/Jaani2634/roman-urdu-agent-reliability.

## Author Contributions

Junaid Nazeer is the sole author. He designed the study, wrote the forty tasks, ran the experiment, graded the open-ended tasks, analysed the results, and wrote the paper.

## Acknowledgements

The author thanks the anonymous reviewers for their comments on an earlier draft.

## Funding

This research received no external funding.

## Competing Interests

The author declares no competing interests.

## Ethics

No human participants were involved and no personal data were collected. The study used only the author's own prompts and a commercial API.

---

## Appendix A: Task list (summary)

Four items (A2, A6, A8, A10) were designed under Category A and are analysed under Category C; see Section 3.1. Original categories are preserved in the supplementary task file.

**A. Factual questions (6 analysed):** A1 Pakistan's population; A3 Lahore-Islamabad distance; A4 which company develops the AI assistant Muse (expected: Meta); A5 first fast of Ramadan 2026; A7 Quaid-e-Azam's full name; A9 "research" in Urdu.

**B. Data tasks (10):** B1 sort five names alphabetically; B2 summarise a paragraph in one sentence; B3 sort five numbers ascending; B4 count words in a paragraph; B5 build a three-row table of cities and specialities; B6 reply to an email stating the meeting is at 11 o'clock; B7 capitals of Pakistan, India, Bangladesh; B8 five-item shopping list under Rs 1,000; B9 correct a sentence; B10 a three-part story about a lost child.

**C. Arithmetic and logic (14 analysed):** C1 unit price of sugar; C2 distance at 60 km/h for 3 hours; C3 remainder after 37% of 1,000; C4 area of a 12 x 10 ft room; C5 next number after 2, 4, 8, 16; C6 savings from Rs 50,000 after 30% spending; C7 bus departure after a 45-minute delay from 9:30; C8 splitting Rs 900 among three friends; C9 perimeter of an 8 x 5 rectangle; C10 the day ten days after Friday; A2 15% of 2,500; A6 minutes in 3 h 45 min; A8 price after 10% discount on Rs 800; A10 7 x 8 + 12.

**D. Multi-step tasks (10):** D1 five cities, a famous dish each, then a table; D2 three video titles, pick the best, give a reason; D3 a shop schedule from 9 a.m. to 6 p.m., hour by hour; D4 summarise a story, ask a question about it, answer it; D5 a monthly budget from Rs 40,000; D6 a three-point meeting agenda with detail, time, and venue; D7 a ~50-word product description, three benefits, price Rs 500; D8 who first stepped on the Moon, two more sentences, a source; D9 a seven-day meal plan plus a shopping list; D10 code printing 1-10, an explanation, and a change to print in reverse.

---

## Appendix B: Anticipated objections

Two objections to this study are obvious enough that they deserve answers here rather than from a reviewer.

**"Forty tasks is too small."** A small task set can still rank reliably: Ndzomga (2026) shows that reliable rankings can be obtained without running an entire benchmark. The contribution is the failure taxonomy and the task set, not the headline percentage, and both survive the sample size.

**"One model only."** Testing one model under two conditions isolates the variable that matters here, which is phrasing; a second model would add a second variable, not a second answer. The released task set exists so that others can run the same comparison on other models.

## Appendix C: Reproducibility details

Model: Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`), accessed through Google's public API. Generation: maximum output 1,024 tokens, at the model's default settings (a temperature of 0 was set in the request but is ignored by this model, which applies its default temperature of 1.0); no thinking level was set, so the model ran at its default minimal thinking level; no system instructions, no examples, no conversation history. Each task was attempted exactly once per condition. Where the API returned an error, most often "503 Service Unavailable", the call was retried, and every retry was logged: 28 of the 80 runs needed at least one retry, and 5 runs still failed after five attempts each and are recorded as unmeasured. The API sometimes returned a response split across two parts; the full response was reconstructed by joining all parts before grading. Grading: categories A and C were graded automatically by word-boundary matching for the expected value, with manual review of every mismatch; categories B and D were graded by hand against the task rubric by a single grader, and a response counted as correct only if it contained the expected answer or satisfied every part of the task. No partial credit was given. Every grade is recorded in the supplementary scoring sheet with a one-line note. Differences were tested with Fisher's exact test. The full response, latency, and token count for every call are recorded in the supplementary raw-responses file. The analysis code in the supplementary folder recomputes every headline number from those files.
