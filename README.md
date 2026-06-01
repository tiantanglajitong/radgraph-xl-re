# RadGraph-XL Relation Extraction

Local Python project for a dissertation study of transformer-based entity and
relation extraction from radiology reports.

## Data handling

The RadGraph-XL archive is credentialed PhysioNet data. Keep the archive outside
this repository and never commit reports, extracted JSONL files, model outputs,
or notebook cells containing report text.

Copy `.env.example` to `.env` and update `RADGRAPH_XL_ZIP` if the local archive
path changes. `.env`, archives, JSONL files, model weights, and experiment
outputs are ignored by Git.

## VS Code setup

Open `E:\final_project` in VS Code. The workspace settings select:

```text
.venv\Scripts\python.exe
```

Create the environment and install the package:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Run the smoke checks:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m radgraph_re.cli info
```

## Current scope

This first commit contains the local development skeleton only. Dataset audit,
NER training, relation extraction, evaluation, and graph export commands will be
added in the implementation phase.

