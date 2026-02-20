import typer
import logging
from config.config import ProjectConfig
from databricks.connect import DatabricksSession
from mlflow.tracking import MlflowClient
from .score import score_batch

# Optional feature engineering client dependencies
# from databricks.feature_engineering import FeatureEngineeringClient

app = typer.Typer()

@app.command()
def main(
    config_path: str = typer.Option("conf/project.yml", "--config", help="Path to YAML project config"),
    env: str = typer.Option(..., help="Target environment (dev, sit, prod)"),
    input_table: str = typer.Option(None, help="Inference data table")
):
    config = ProjectConfig.from_yaml(config_path, env)
    
    # Configure root logger dynamically
    logging.basicConfig(level=config.log_level.upper())
    logger = logging.getLogger(__name__)

    spark = DatabricksSession.builder.getOrCreate()
    client = MlflowClient(registry_uri="databricks-uc")
    
    model_name = config.fully_qualified_model_name
    
    try:
        champion_model = client.get_model_version_by_alias(model_name, "champion")
        model_uri = f"models:/{model_name}@champion"
        logger.info(f"Loaded Champion model version {champion_model.version} for batch inference")
        
        # Execute Batch Inference Logic
        input_table = input_table or config.training_data_path
        input_df = spark.table(input_table)
        
        result_df = score_batch(model_uri, input_df)
        
        logger.info("Batch inference completed and written to destination.")
        
    except Exception as e:
        logger.error(f"Cannot run inference: {e}")
        raise e

if __name__ == "__main__":
    app()
