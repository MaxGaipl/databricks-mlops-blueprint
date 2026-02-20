import pytest
from mlops_blueprint.config.config import load_config
from pydantic import ValidationError

def test_config_environments():
    """
    Test 1: Check if the configuration files can be converted without errors 
    into the pydantic model for each environment.
    """
    config_path = "conf/project.yml"
    
    environments = ["dev", "sit", "prod"]
    
    for env in environments:
        try:
            config = load_config(config_path, env)
            
            # Assert that the basic global and environment-specific fields are parsed
            assert config.environment == env
            assert hasattr(config, "catalog")
            assert hasattr(config, "schema")
            assert hasattr(config, "experiment_name")
            assert hasattr(config, "model_name")
            assert hasattr(config, "training_data_path")
            assert hasattr(config, "log_level")
            
        except ValidationError as e:
            pytest.fail(f"Pydantic ValidationError occurred while parsing config for environment '{env}': {e}")
        except FileNotFoundError:
            pytest.skip(f"Could not find {config_path} to test. Ensure you run pytest from the project root.")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred parsing '{env}' config: {e}")

def test_missing_environment():
    """Test loading an environment that doesn't exist raises an error."""
    with pytest.raises(ValueError, match="not found in"):
        load_config("conf/project.yml", "nonexistent_env")
