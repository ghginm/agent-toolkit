# Audit #2 — ML/DS Methodology

Critically evaluate the ML/DS *reasoning* and experimental methodology: not only what was implemented but why it may or may not be appropriate for this problem, data, and deployment context.

Contents:
1. What qualifies a finding
2. Inspection areas and code probes
3. The reasoning chain (required per finding)
4. Confirmed vs inferred rationale
5. Research gaps — flag, don't research
6. Scope discipline with the other audits
7. Handoff shape

## 1. What qualifies a finding

A methodology finding connects a specific implementation choice to a specific risk to validity, generalization, or decision quality, and points at code. "No baseline model" is only a finding when results are being reported as decision-relevant; "no calibration" is only a finding when a threshold decision exists somewhere (cite where the threshold is applied). Findings without a mechanism ("might be overfit, who knows") go into the `unknown` section, not the findings list.

## 2. Inspection areas and code probes

Locate the code that *implements* each area — methodology audits are done in the code, not in the notebook prose. Useful probes: grep `split`, `shuffle`, `RandomState|random_state|seed`, `fit_transform|\.fit(`, `merge|join|concat`, metric names, `test`, `holdout`, `calibrat`, `dropna|fillna|encode`.

**a. Problem framing and target.** What is the label, and does the optimization target match the stated objective? Read where the target column is constructed (`shift`, thresholding, label joins) — target bugs hide there. Check the metric actually computed in eval code vs the metric README claims.

**b. Split integrity — the leakage battery.** For each transform/scaler/encoder/imputer/feature-selection step, check where it is fit: fitting on the full dataset before splitting is the classic leak — cite the line. Also check:
- Temporal leakage: shuffled CV on time-dependent data; features containing information from after the label's cutoff (`grep shift|lead`, compare merge keys' dates); train/test split before time-window features are built.
- Group leakage: same entity (user, device, product) in train and test — look at what keys the split uses vs what the model memorizes.
- Target leakage: features derived from the label, including through merges on label-rich tables.
- Preprocessing defined outside the CV folds (a single fit outside folds re-used per fold).
- Hyperparameter selection on the test set (trace what data `GridSearch|Optuna|param_trials` consumes and what data the reported score uses).

**c. Data assumptions and sampling.** What population does the data represent; is the sampling biased (only surviving users, only completed transactions, missing-not-at-random NaN patterns); is `dropna` silently shrinking the population (cite line + report the drop if cheap to compute from code reading — do not fabricate numbers). Label quality: proxy labels, noisy feedback loops, construction cutoffs.

**d. Feature engineering.** Do transforms match the serving-time availability of the same columns (batch vs online skew)? Are categories/encodings handled for unseen values? Time features leak via future aggregates? Each concern needs the code path cited.

**e. Model and baseline choices.** Is there a trivial baseline (majority/mean/per-item mean/last-value for time series) reported alongside the fancy model? Missing baseline with reported "improvement" claims → finding. Model family choice is rarely a finding by itself — it becomes one when data properties (size, structure, latency, interpretability requirement) contradict it; state the contradiction and cite the property.

**f. Evaluation and metrics.** Metric alignment with cost structure (accuracy on 1% positives; AUC when the decision is a threshold on precision); CV scheme validity (single split reported as the number, k folds without variance, early-stop on the eval set); uncertainty (any CI or seed-variation on headline results?); aggregation (macro vs micro vs weighted — silent choice changes conclusions).

**g. Calibration and thresholds.** If the system thresholds probabilities, is the calibration step present and fit on data disjoint from training? Where is the threshold value set (cite config/constant) and is it tied to a documented operating point?

**h. Error analysis and robustness.** Does anything examine *which* errors happen (slices, confusion by segment, residual plots)? Absence is a finding only for tiers/uses where error asymmetry matters (cite the use context). Distribution shift handling: retraining trigger, drift monitoring — expected at tier 4; at tier 2 note as gap-to-deployment if production intent exists.

**i. Reproducibility of results.** Seed handling, data version pinning (hash, snapshot name, or none), the path from raw data → reported number. A result nobody can regenerate is a finding: cite what's missing concretely.

**j. Interpretability / consequential domains.** Only when stakes or regulation demand it (loan, medical, hiring, or user-facing automated action — cite the evidence of the domain from code/docs, don't infer from vibes). Fairness slices, explanation hooks.

## 3. The reasoning chain (required per finding)

Every `ml` finding writes these eight steps compactly — they are what makes this an analysis instead of a checklist:

1. **What the implementation does** (cited: `path::symbol`).
2. **Why the original choice may have been reasonable** — the honest steelman.
3. **Assumptions it relies on** (independence, stationarity, availability, no feedback loops...).
4. **What could go wrong** — the concrete failure mechanism and direction of harm.
5. **Meaningful alternative**, and why it might help *or hurt* (no free "just use XGBoost").
6. **How to validate the concern experimentally** — the smallest decisive experiment with its protocol.
7. **Confidence** with reason; where relevant, severity by the tier of decision the result feeds.
8. **Category** — `justified-now` | `experiment-first` | `research-gap`; this classification is what the handoff (§7) and downstream planning agents sort on.

## 4. Confirmed vs inferred rationale

If README/comment/commit documents the author's reasoning → quote and cite it (`confirmed rationale`). Otherwise write `inferred rationale (not documented): <best guess>` — never present a guess as the author's reason. Do not invent historical design decisions; there is no way to know, and an audit that guesses loses its authority.

## 5. Research gaps — flag, don't research

This audit is not a literature workflow. When a concern depends on external theoretical knowledge or evidence you cannot get from this repo:

- Record it in the report's **Research gaps** section: the targeted question, why the answer changes the implementation/experiments, what evidence would resolve it, and its uncertainty status (`unknown`).
- Do not launch broad literature searches. A separate research skill can take the flag later; a sharp question is the deliverable here.

## 6. Scope discipline with the other audits

Methodology problems go here even when they live in code structure: leakage *is* audit #2; "leakage happens because preprocessing can only run before the split given the current module layout" is *also* an audit #1 boundary finding — cross-reference by ID instead of restating the analysis. Anything about open-ended risk outside these areas → audit #3 territory; when running `all`, hand candidates over rather than double-filing.

## 7. Handoff shape

Separate two tiers of proposals explicitly:
- **Justified now** — fixes whose superiority doesn't depend on new evidence (e.g., fitting the scaler inside the CV loop): touch points, expected metric movement direction, and which tests/evals to run.
- **Experiment first** — changes needing validation: the experiment protocol (split to use, metric, baseline, guardrails such as latency or slice performance), and the decision rule for adopting the result.

Include: model/feature/data/eval/config files touched; invariants ("training and serving must consume the same feature builder"); leakage and regression risks if the change is done partially; and approval-needed flags (anything changing the dataset, the metric, or retraining cost).
