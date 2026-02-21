import yaml
from pydantic import BaseModel, Field

class ProjectConfig(BaseModel):
    environment: str = Field(description="The deployment environment (dev, sit, prod)")
    catalog: str = Field(description="The Unity Catalog name")
    schema_name: str = Field(description="The Schema name")
    experiment_name: str = Field(description="MLflow experiment path")
    model_name: str = Field(description="Name of the model in UC")
    training_data_path: str = Field(description="Path to the bronze/raw data")
    log_level: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")

    @property
    def fully_qualified_model_name(self) -> str:
        return f"{self.catalog}.{self.schema_name}.{self.model_name}"

    @classmethod
    def from_yaml(cls, config_path: str, environment: str) -> "ProjectConfig":
        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)

        # 1. Get the shared/global attributes
        base_config = {
            k: v for k, v in raw_config.items() if k != "environments"
        }

        # 2. Get the environment-specific attributes
        environments_block = raw_config.get("environments", {})
        if environment not in environments_block:
            raise ValueError(f"Environment '{environment}' not found in {config_path}")
        
        env_config = environments_block[environment]

        # 3. Merge them together (env_config overwrites base_config if they overlap)
        merged_config = {**base_config, **env_config, "environment": environment}

        # 4. Pass the flat, merged dictionary to Pydantic
        return cls(**merged_config)
