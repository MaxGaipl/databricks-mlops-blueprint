import typer
import logging
from config.config import ProjectConfig
from mlflow.tracking import MlflowClient
from .promote import promote_model

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

    client = MlflowClient(registry_uri="databricks-uc")
    model_name = config.fully_qualified_model_name
    
    logger.info(f"Checking {model_name} aliases for deployment...")
    
    # Execute Deployment Logic via business logic template
    promote_model(client, model_name)

if __name__ == "__main__":
    app()
