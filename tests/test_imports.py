import pytest
import importlib

def test_entry_point_imports():
    """
    Test 2: Check if all expected entry points run (import) successfully 
    without SyntaxErrors, ModuleNotFoundErrors, or circular dependencies.
    """
    
    # List of main modules defined in pyproject.toml package scripts
    entry_points = [
        "mlops_blueprint.feature_engineering.main",
        "mlops_blueprint.training.main",
        "mlops_blueprint.validation.main",
        "mlops_blueprint.deployment.main",
        "mlops_blueprint.batch_inference.main"
    ]
    
    for module_name in entry_points:
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            # Note: without a venv, tools like typer, mlflow, databricks.connect might not be installed.
            # In a CI/CD setting where requirements are installed, this will catch true missing imports.
            pytest.fail(f"Failed to import {module_name} due to missing dependencies or syntax: {e}")
        except Exception as e:
            pytest.fail(f"Failed to import {module_name} with unexpected error: {e}")
