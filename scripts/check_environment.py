"""Verify the local ML environment without loading restricted data."""

from __future__ import annotations

import importlib
import importlib.metadata
import json
import platform
import sys
from typing import Any

import torch

REQUIRED_PACKAGES = (
    "accelerate",
    "datasets",
    "matplotlib",
    "networkx",
    "numpy",
    "pandas",
    "python-dotenv",
    "PyYAML",
    "safetensors",
    "scikit-learn",
    "seaborn",
    "seqeval",
    "transformers",
)

IMPORT_NAMES = {
    "python-dotenv": "dotenv",
    "PyYAML": "yaml",
    "scikit-learn": "sklearn",
}


def package_versions() -> dict[str, str]:
    """Return installed versions after confirming imports work."""
    versions: dict[str, str] = {}
    for package_name in REQUIRED_PACKAGES:
        importlib.import_module(IMPORT_NAMES.get(package_name, package_name))
        versions[package_name] = importlib.metadata.version(package_name)
    return versions


def environment_report() -> dict[str, Any]:
    """Build a JSON-serializable local environment report."""
    cuda_available = torch.cuda.is_available()
    return {
        "python": platform.python_version(),
        "executable": sys.executable,
        "torch": torch.__version__,
        "torch_cuda_build": torch.version.cuda,
        "cuda_available": cuda_available,
        "gpu": torch.cuda.get_device_name(0) if cuda_available else None,
        "packages": package_versions(),
    }


def main() -> None:
    """Print the report and fail if CUDA is unavailable."""
    report = environment_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["cuda_available"]:
        raise SystemExit("CUDA is unavailable in the configured PyTorch environment.")


if __name__ == "__main__":
    main()

