import typer
import logging
import mlflow
from config.config import ProjectConfig
from databricks.connect import DatabricksSession
from mlflow.tracking import MlflowClient
from .evaluate import evaluate_model

app = typer.Typer()

@app.command()
def main(
    config_path: str = typer.Option("conf/project.yml", "--config", help="Path to YAML project config"),
    env: str = typer.Option(..., help="Target environment (dev, sit, prod)")
):
    config = ProjectConfig.from_yaml(config_path, env)
    
    # Configure root logger dynamically
    logging.basicConfig(level=config.log_level.upper())
    logger = logging.getLogger(__name__)

    spark = DatabricksSession.builder.getOrCreate()
    client = MlflowClient(registry_uri="databricks-uc")
    
    # Validation logic goes here
    logger.info("Initializing MLflow evaluation...")
    
    # 1. Fetch latest model (No aliases like @champion currently - this is a fresh run)
    model_name = config.fully_qualified_model_name
    logger.info(f"Evaluating {model_name}...")
    
    # 2. Run business logic for validation
    is_valid = evaluate_model(model_name)
    
    # 3. Apply Challenger Alias if valid
    if is_valid:
        # Fetch the latest version of the model to apply the alias.
        # Note: In a real pipeline, the newly created version may be passed from the training task via Task Values.
        latest_versions = client.search_model_versions(f"name='{model_name}'")
        if latest_versions:
            latest_version = latest_versions[0].version
            # e.g., client.set_registered_model_alias(model_name, "challenger", latest_version)
            logger.info(f"Would set challenger alias on version {latest_version}")
        else:
            logger.warning(f"No versions found for {model_name} to alias.")
    
    logger.info("Validation completed successfully.")

if __name__ == "__main__":
    app()
