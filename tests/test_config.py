import pytest
from pathlib import Path
from mlops_blueprint.config.config import ProjectConfig
from pydantic import ValidationError

def get_config_files():
    """Helper to find all yaml files in conf/ directory"""
    conf_dir = Path("conf")
    if not conf_dir.exists():
        return []
    return list(conf_dir.glob("*.yml")) + list(conf_dir.glob("*.yaml"))

@pytest.mark.parametrize("config_path", get_config_files())
def test_config_environments(config_path):
    """
    Test 1: Check if all configuration files can be loaded correctly
    for each environment into the ProjectConfig model.
    """
    environments = ["dev", "sit", "prod"]
    
    for env in environments:
        try:
            ProjectConfig.from_yaml(str(config_path), env)
        except ValidationError as e:
            pytest.fail(f"Pydantic ValidationError occurred while parsing config '{config_path}' for environment '{env}': {e}")
        except FileNotFoundError:
            pytest.skip(f"Could not find {config_path} to test. Ensure you run pytest from the project root.")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred parsing '{env}' config '{config_path}': {e}")

@pytest.mark.parametrize("config_path", get_config_files())
def test_missing_environment(config_path):
    """Test loading an environment that doesn't exist raises an error."""
    with pytest.raises(ValueError, match="not found in"):
        ProjectConfig.from_yaml(str(config_path), "nonexistent_env")
