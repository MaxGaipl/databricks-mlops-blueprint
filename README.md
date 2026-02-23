# Databricks MLOps Blueprint Template

A standard, production-ready blueprint for MLOps on Databricks. This template emphasizes **configuration-driven development**, **local-first engineering**, and **automated deployments** using Databricks Asset Bundles (DABs).

## 🚀 Quickstart

Follow these steps to initialize your new project from this template:

### 1. Prerequisites
- [uv](https://docs.astral.sh/uv/) (Modern Python package manager)
- [Databricks CLI](https://docs.databricks.com/en/dev-tools/cli/index.html)
- Python 3.12

### 2. Initialize Project
Clone the repository and run the initialization script:

```bash
python init_project.py
```
This script will:
- Prompt for your project name and Databricks workspace URLs.
- Perform a global find-and-replace to rename all template placeholders.
- Initialize a git repository and commit the changes.
- Self-destruct after completion.

### 3. Setup Environment
```bash
uv sync --extra local-dev
```

### 4. Deploy to Sandbox
```bash
databricks bundle deploy -t sandbox
```

## 🛠 Way of Working

- **Local Development**: Write and test code locally using `databricks-connect`. No more copy-pasting code into web notebooks!
- **Pure Python**: Business logic resides in `src/` as standard Python modules.
- **Wheels first**: All code is packaged as a Python Wheel before being deployed to Databricks clusters.
- **Config-driven**: Use Pydantic models and YAML files to manage experiment parameters and environment-specific settings.

## 📖 Documentation

For a deep dive into the architecture, configuration system, and deployment workflows, see the **[Full Project Documentation](DOCUMENTATION.md)**.
