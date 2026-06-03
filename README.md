# RadGraph-XL Relation Extraction

Local Python project for a dissertation study of transformer-based entity and
relation extraction from radiology reports.

## Data handling

The RadGraph-XL archive is credentialed PhysioNet data. Keep the archive outside
this repository and never commit reports, extracted JSONL files, model outputs,
or notebook cells containing report text.

Copy `.env.example` to `.env` and update `RADGRAPH_XL_ZIP` if the local archive
path changes. `.env`, archives, JSONL files, model weights, experiment outputs,
and generated figures are ignored by Git.

## VS Code setup

Open `E:\final_project` in VS Code. The workspace settings select:

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

Use these notebooks for the current data-preparation phase:

```text
notebooks\01_data_audit.ipynb
notebooks\02_data_visualization.ipynb
```

`01_data_audit.ipynb` reads the external RadGraph-XL ZIP, checks the JSONL
structure, and writes aggregate outputs:

```text
outputs\audit\data_audit.json
outputs\audit\report_summary.csv
```

`02_data_visualization.ipynb` generates aggregate figures under:

```text
outputs\figures\
```

The notebooks are designed to show only aggregate counts, labels, and
distributions. They must not display or save report text.

## Current scope

The project currently supports local environment verification, notebook-based
RadGraph-XL data audit, and non-sensitive visualization. Dataset splits, NER
training, relation extraction, evaluation, and graph export will be added in
later implementation phases.

