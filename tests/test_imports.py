import pytest
import importlib

@pytest.mark.parametrize("module_name", [
    "feature_engineering.main",
    "training.main",
    "validation.main",
    "deployment.main",
    "batch_inference.main"
])
def test_entry_point_imports(module_name):
    """
    Test 2: Check if all expected entry points run (import) successfully 
    without SyntaxErrors, ModuleNotFoundErrors, or circular dependencies.
    """
    try:
        importlib.import_module(module_name)
    except ImportError as e:
        # Note: without a venv, tools like typer, mlflow, databricks.connect might not be installed.
        # In a CI/CD setting where requirements are installed, this will catch true missing imports.
        pytest.fail(f"Failed to import {module_name} due to missing dependencies or syntax: {e}")
    except Exception as e:
        pytest.fail(f"Failed to import {module_name} with unexpected error: {e}")
