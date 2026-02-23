# Comprehensive Project Documentation

This document provides a detailed overview of the Databricks MLOps Blueprint architecture, development workflows, and deployment strategies.

## 📁 Project Structure

```text
├── conf/                  # YAML configuration files (env-specific & global)
├── notebooks/             # Interactive notebooks & local scratchpads
├── resources/             # Databricks Asset Bundle (DAB) job definitions
├── src/                   # Main source code (Pure Python)
│   ├── config/            # Pydantic configuration models
│   ├── feature_engineering/ # Logic for feature preparation
│   ├── training/          # Model training and MLflow tracking
│   ├── validation/        # Model evaluation and signature validation
│   └── deployment/        # Deployment scripts (UC registration, etc.)
├── tests/                 # Unit and integration tests
├── databricks.yml         # Main DAB entry point
└── pyproject.toml         # Python project metadata and dependencies
```

---

## ⚙️ Configuration Management

We use a **two-layered** configuration system:
1. **YAML Files (`conf/`)**: Store human-readable parameters.
2. **Pydantic Models (`src/config/`)**: Provide runtime validation and type safety.

### Environment Support
The `ProjectConfig` class (in `src/config/config.py`) implements a merging logic:
- Global parameters are defined at the top level of `conf/project.yml`.
- Environment-specific overrides (e.g., `dev`, `sit`, `prod`) are defined under the `environments` key.

To load a config for a specific environment:
```python
from config.config import ProjectConfig
config = ProjectConfig.from_yaml("conf/project.yml", "dev")
```

---

## 💻 Local Development Workflow

This template is designed for **local-first** development.

### 1. Environment Setup
We use `uv` for lightning-fast dependency management.
```bash
uv sync --extra local-dev
```

### 2. Interactive Development
Use `notebooks/scratchpad.py` for interactive coding. With the [Databricks Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=databricks.databricks), you can run code directly on a Databricks cluster using **Databricks Connect**.

### 3. CLI Entry Points
Each ML stage (Feature Engineering, Training, etc.) is defined as a CLI command in `pyproject.toml`. This allows you to run them locally for debugging:
```bash
# Example: Run feature engineering locally
python -m feature_engineering.main --env dev
```

---

## 🚀 Deployment (Databricks Asset Bundles)

All infrastructure and jobs are managed as **Databricks Asset Bundles (DABs)**.

### Commands
- **Deploy to Sandbox**: `databricks bundle deploy -t sandbox`
- **Run a Job**: `databricks bundle run feature_engineering_job -t sandbox`
- **Destroy Stack**: `databricks bundle destroy -t sandbox`

### Resource Definitions
Job definitions are located in `resources/`. These YAML files reference the CLI entry points defined in `pyproject.toml`. When you deploy, the DAB build process:
1. Builds a **Python Wheel** from your `src/` directory.
2. Uploads the Wheel to Databricks.
3. Configures the Job to install that Wheel on the cluster.

---

## ✅ Best Practices

- **Avoid Notebook logic**: Keep business logic in `src/` modules. Notebooks should only be used for exploration or as thin wrappers.
- **Unit Testing**: Write tests in `tests/` and run them with `pytest`. Mock Spark or use `databricks-connect` for integration tests.
- **MLflow Tracking**: Every training run should be tracked in MLflow using the `experiment_name` from the config.
- **Unity Catalog**: Always use Unity Catalog for data governance (Catalog -> Schema -> Table).
