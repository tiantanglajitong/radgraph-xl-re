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

The same checks are available in VS Code through `Terminal > Run Task`.

## Current scope

This commit configures the local development and ML environment. Dataset audit,
NER training, relation extraction, evaluation, and graph export commands will be
added in the implementation phase.
