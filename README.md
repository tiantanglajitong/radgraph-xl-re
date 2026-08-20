# RadGraph-XL Relation Extraction

Local Python project for a dissertation study of transformer-based entity and
relation extraction from radiology reports.

## Data handling

The project uses the complete 2,300-report RadGraph-XL collection:

```text
RadGraphXL\
  radgraph-xl-...-1.0.0.zip          # 300 credentialed MIMIC reports
  stanford\
    stanford-radgraph-XL.jsonl       # 2,000 Stanford reports
```

Both sources are restricted data. Never commit reports, extracted JSONL files,
model outputs, or notebook cells containing report text. `RadGraphXL/`, `.env`,
archives, JSONL files, model weights, experiment outputs, and generated figures
are ignored by Git.

Copy `.env.example` to `.env` and configure:

```text
RADGRAPH_XL_MIMIC_ZIP
RADGRAPH_XL_STANFORD_JSONL
RADGRAPH_XL_RUN_NAME
```

`RADGRAPH_XL_RUN_NAME=full_2300` writes new artifacts below
`outputs\full_2300\` so the completed 300-report outputs are not overwritten.

### Dataset acknowledgement and citation

RadGraph-XL was created by Delbrouck et al. and released by
[@Stanford-AIMI](https://github.com/Stanford-AIMI) for research on clinical
entity and relation extraction. This repository contains an independent
experimental pipeline and does not redistribute any RadGraph-XL records.

Researchers should obtain the data through the authorised release channels,
accept the applicable data-use terms, and cite both the dataset paper and the
versioned dataset release:

- [RadGraph-XL paper, Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.765/)
- [RadGraph-XL v1.0.0 on PhysioNet](https://physionet.org/content/radgraph-xl/1.0.0/), DOI: `10.13026/j8e7-pr22`
- [Official Stanford AIMI RadGraph-XL repository](https://github.com/Stanford-AIMI/radgraph-XL)

```bibtex
@inproceedings{delbrouck-etal-2024-radgraph,
  title     = {RadGraph-XL: A Large-Scale Expert-Annotated Dataset for
               Entity and Relation Extraction from Radiology Reports},
  author    = {Delbrouck, Jean-Benoit and Chambon, Pierre and Chen, Zhihong
               and Varma, Maya and Johnston, Andrew and Blankemeier, Louis
               and Van Veen, Dave and Bui, Tan and Truong, Steven
               and Langlotz, Curtis},
  booktitle = {Findings of the Association for Computational Linguistics:
               ACL 2024},
  year      = {2024},
  pages     = {12902--12915},
  url       = {https://aclanthology.org/2024.findings-acl.765}
}
```

## VS Code setup

Open the cloned repository folder in VS Code. The workspace settings select:

```text
.venv\Scripts\python.exe
```

Create the environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

Install the CUDA-enabled PyTorch wheel and project dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements\torch-cu128.txt
.\.venv\Scripts\python.exe -m pip install -e ".[dev,ml,notebook]"
```

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Run the checks:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\check_environment.py
.\.venv\Scripts\python.exe -m radgraph_re.cli info
```

Open `test.ipynb` in VS Code to rerun the package import, GPU detection, and
CUDA matrix multiplication checks interactively.

## Notebook workflow

Run the notebooks in numerical order:

```text
notebooks\01_data_audit.ipynb
notebooks\02_data_visualization.ipynb
notebooks\03_prepare_radgraph_ner_re_dataset.ipynb
notebooks\04_train_ner_transformer.ipynb
notebooks\05_train_re_transformer_v2.ipynb
notebooks\06_compare_ner_backbones.ipynb
notebooks\07_evaluate_end_to_end_pipeline.ipynb
notebooks\08_error_analysis_and_results.ipynb
notebooks\09_threshold_sensitivity_analysis.ipynb
notebooks\10_report_language_and_similarity_analysis.ipynb
```

`01_data_audit.ipynb` reads both restricted sources, checks their compatible
JSONL structure, and writes source-level and combined aggregate outputs:

```text
outputs\full_2300\audit\data_audit.json
outputs\full_2300\audit\report_summary.csv
```

`02_data_visualization.ipynb` generates aggregate figures under:

```text
outputs\full_2300\figures\
```

It also writes `dataset_figure_manifest.json`, which records the dataset scope,
suggested dissertation placement, and caption for every formal dataset figure.

`03_prepare_radgraph_ner_re_dataset.ipynb` creates a stratified 70/15/15
report split and model-ready files under `outputs\full_2300\interim\`. Relation
candidates are written to CSV in bounded chunks so the full 5+ million-row
candidate pool is not retained in memory.

Notebooks 04-08 resolve every intermediate, model, prediction, result, analysis,
and figure path below `outputs\<RADGRAPH_XL_RUN_NAME>\`. Notebook 05 v2 scans the
large relation-candidate CSV in two bounded-memory passes: the first counts each
split and label, and the second retains all positive relations while selecting
the configured number of training negatives. Validation and test candidates are
unsampled by default.

`09_threshold_sensitivity_analysis.ipynb` evaluates the relation confidence
threshold on validation predictions only and applies the selected threshold to
the frozen test predictions.

`10_report_language_and_similarity_analysis.ipynb` performs the final lexical
and split-leakage audit. It requires the fixed split generated by Notebook 03
but does not require model training. It writes aggregate language metrics,
normalised-text hashes, TF-IDF cosine-similarity scores and figure metadata to:

```text
outputs\full_2300\linguistic_audit\
outputs\full_2300\figures\
```

Notebook 10 does not export report text or token sequences. Aggregate top terms
may include de-identification or reporting-template language; these terms must
be interpreted as properties of the model input, not solely as clinical
vocabulary.

The notebooks are designed to show only aggregate counts, labels, and
distributions. They must not display or save report text. Repository notebooks
are committed without execution outputs; rerun them only in an authorised local
environment.

## Current scope

The project supports local environment verification, protected-data audit,
model-ready dataset preparation, BERT NER and RE baselines, error analysis,
domain-specific NER backbone comparison, end-to-end pipeline evaluation, and a
report-language and cross-split similarity audit.
The complete-data preprocessing stage has been executed. Full model training is
started manually from notebooks 04-06 because it is GPU-intensive; notebooks
07-08 are run after the required full-dataset checkpoints and predictions exist.

