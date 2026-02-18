# Evaluation

The evaluation chapter measures how well the system performs. The reader arrives here believing the system works. This chapter tells them how it performed by showing evidence.

The focus is analytical, not demonstrative. Present hypotheses, describe how you tested them, report what you measured, and interpret the results.

Evaluation should be anchored in the main claims of what the paper has made so far.

## Required Elements

Missing any element is a fail.

- [ ] What specific claims are you testing? State each as a falsifiable prediction or a concrete question with a measurable answer.
- [ ] How did you test each hypothesis? Describe the experimental setup, what you measured, what you controlled, and what you varied.
- [ ] What did the measurements show? Tables and figures must carry the weight here.
- [ ] What do the results mean? Connect each finding back to its hypothesis. State whether the hypothesis held, partially held, or failed.

## Rules

Each is pass/fail.

1. State hypotheses before describing experiments. The reader must know what question an experiment answers before learning how it was run.

2. Every experiment must map to a hypothesis. If an experiment does not test a stated hypothesis, it has no purpose in this chapter. If a hypothesis has no experiment, the evaluation is incomplete.

3. Describe the methodology with enough precision to reproduce. Name the hardware, dataset sizes, trial counts, duration, and any randomization or sampling strategy. "We ran several tests" fails. "We ran 500 trials on a four-node cluster over 48 hours" passes.

4. Report results with numbers. "Performance improved" fails. "Discovery latency dropped from 320 ms to 180 ms" passes. Every claim must attach to a measurement.

5. Separate results from interpretation. Present what the data shows before explaining what it means. Mixing the two makes it impossible for the reader to evaluate your reasoning independently.

6. Every figure and table must be referenced in the prose and explained. State what the reader should observe — do not leave them to draw their own conclusions from a chart.

7. Acknowledge threats to validity. State what could undermine your results — sample size, environment constraints, confounding variables. A missing threats section signals that the author has not critically examined their own work.

8. Do not introduce the system or explain how it works. The reader already knows. If you find yourself describing architecture or walking through features, that belongs earlier in the paper.

9. When results contradict a hypothesis, report them with the same rigor and prominence as confirmations. Do not bury or minimize disconfirming evidence.

10. Compare against a meaningful baseline. Results in isolation have no scale. The baseline can be an existing tool, a naive approach, or a theoretical bound — but the reader needs a reference point to judge the numbers.