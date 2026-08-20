# Controlled Optimisation Guide

## Fixed Experimental Conditions

Keep the following unchanged in every experiment:

- report-level train/validation/test split;
- `RANDOM_SEED = 42`;
- BIO label construction and strict span evaluation;
- validation-only model and threshold selection;
- test evaluation after selecting a configuration.

Do not change the seed during the experiments in this guide. A run is comparable only
when the dataset split, seed, evaluation code, and all non-target factors are fixed.

## Output Naming

The notebooks preserve the original baseline outputs.

- Sliding-window NER: `ner_<backbone>_sliding_window_*`
- Named RE experiment: `re_<RE_EXPERIMENT_NAME>_*`
- End-to-end run: `end_to_end_<NER_EXPERIMENT>_<RE_EXPERIMENT>_*`

Notebook 08 discovers these files automatically and writes consolidated comparison
tables.

## Recommended Run Order

### 1. PubMedBERT NER in the Existing Pipeline

Notebook 07 is currently configured as:

```python
NER_EXPERIMENT = "pubmedbert_sliding_window"
RE_EXPERIMENT = "bert_generic_neg5_unweighted"
```

This uses the selected complete-report NER and RE configurations. To isolate the
NER change against the original relation baseline, set only `RE_EXPERIMENT` to
`"bert_base_uncased"`, run Notebook 07, and then run Notebook 08.

### 2. RE Precision Experiment

Notebook `05_train_re_transformer_v2.ipynb` initially selects:

```python
RE_EXPERIMENT_NAME = "bert_generic_neg5_unweighted"
```

This changes the training negative ratio from `3:1` to `5:1` and disables inverse
frequency class weighting. It directly tests the current high-recall, low-precision
error pattern.

Notebook 05 v2:

- exports every relation-class probability;
- tunes a positive threshold on validation predictions only;
- applies the frozen threshold to the test set;
- reports positive micro and macro precision, recall, and F1.

After training, set Notebook 07 to:

```python
NER_EXPERIMENT = "pubmedbert_sliding_window"
RE_EXPERIMENT = "bert_generic_neg5_unweighted"
```

### 3. RE Backbone Comparison

Run these Notebook 05 v2 profiles separately:

```python
RE_EXPERIMENT_NAME = "bert_generic_neg5_unweighted"
```

```python
RE_EXPERIMENT_NAME = "pubmedbert_generic_neg5_unweighted"
```

Only the transformer checkpoint changes. Negative sampling, marker design, loss,
context, sequence length, training settings, split, and seed remain fixed.

### 4. Marker Comparison

Run:

```python
RE_EXPERIMENT_NAME = "pubmedbert_generic_neg5_unweighted"
```

and:

```python
RE_EXPERIMENT_NAME = "pubmedbert_typed_neg5_unweighted"
```

The second profile uses entity-type markers such as:

```text
[HEAD_OBS] ... [/HEAD_OBS]
[TAIL_ANAT] ... [/TAIL_ANAT]
```

This isolates whether explicit Anatomy/Observation information improves relation
classification.

### 5. Capped Class-Weight Experiment

Run:

```python
RE_EXPERIMENT_NAME = "pubmedbert_typed_neg5_capped"
```

The maximum normalised class weight is capped at `5.0`. Compare it with the unweighted
typed-marker profile to determine whether moderate weighting helps `suggestive_of`
without recreating excessive false positives.

### 6. Sliding-Window NER

Notebook 06 is initially configured as:

```python
EXPERIMENT_NAMES = ["pubmedbert"]
LONG_REPORT_METHOD = "sliding_window"
MAX_LENGTH = 512
WINDOW_OVERLAP = 128
RANDOM_SEED = 42
```

Overlapping predictions are averaged at the original-word level and then merged into
one complete report-level BIO sequence. The primary metric is strict full-report entity
F1 against all gold entities.

For a controlled backbone comparison, change only:

```python
EXPERIMENT_NAMES = ["bert_base_uncased", "pubmedbert"]
```

After training, Notebook 07 can use:

```python
NER_EXPERIMENT = "pubmedbert_sliding_window"
```

## Selection Metrics

### NER

Primary:

- strict full-report entity micro F1.

Secondary:

- full-report recall;
- macro F1;
- per-label F1;
- number of predicted and gold entities.

Do not compare tokenizer-specific truncated classification-report support.

### RE

Primary:

- positive-relation macro F1.

Secondary:

- positive-relation micro F1;
- positive precision and recall;
- `located_at`, `modify`, and `suggestive_of` F1;
- predicted positive relation count.

Do not select a relation model using overall candidate accuracy because
`no_relation` dominates the candidate set.

### End to End

Report:

- span-and-relation micro F1;
- strict graph F1;
- per-relation F1;
- gold-entity to end-to-end F1 decrease.

## Hardware Guidance

The RTX 5070 Ti Laptop GPU and 64 GB RAM are sufficient. Use the existing batch sizes
first:

```text
NER train/eval batch: 4 / 8
RE train/eval batch: 8 / 16
End-to-end inference batch: 32
```

Sliding-window NER creates more training samples than report truncation, so it will
take longer. Batch size mainly affects speed and memory; it is not the first quality
parameter to increase.

## Result Logging

For each run record:

- experiment name;
- model checkpoint;
- marker design;
- negative ratio and loss weighting;
- context and maximum length;
- validation-selected threshold;
- validation and test positive micro/macro F1;
- runtime and peak GPU memory;
- interpretation and any failure.

Notebook 08 writes:

- `ner_full_report_backbone_comparison.csv`;
- `re_experiment_comparison.csv`;
- `dissertation_primary_results.csv`;
- `dissertation_relation_results.csv`;
- `dissertation_results_and_error_analysis.md`.
