import typer
import logging
import mlflow
from mlops_blueprint.config.config import load_config
from databricks.connect import DatabricksSession
from mlops_blueprint.training.train import build_model

# Optional: FeatureEngineeringClient
# from databricks.feature_engineering import FeatureEngineeringClient
from mlflow.tracking import MlflowClient

app = typer.Typer()

@app.command()
def main(
    config_path: str = typer.Option("conf/project.yml", "--config", help="Path to YAML project config"),
    env: str = typer.Option(..., help="Target environment (dev, sit, prod)")
):
    config = load_config(config_path, env)
    
    # Configure root logger dynamically
    logging.basicConfig(level=config.log_level.upper())
    logger = logging.getLogger(__name__)

    # Connect
    spark = DatabricksSession.builder.getOrCreate()
    mlflow.set_registry_uri("databricks-uc")
    mlflow.set_experiment(config.experiment_name)
    
    logger.info("Initializing MLflow for training run...")
    
    with mlflow.start_run() as run:
        # Example: Log parameters
        mlflow.log_param("env", config.environment)
        mlflow.log_param("training_data", config.training_data_path)
        
        # --------------------------
        # Execute Training Logic
        # --------------------------
        # 1. Look up features via featurestore
        # fe_client = FeatureEngineeringClient()
        # training_set = fe_client.create_training_set(...)
        training_set = None # Placeholder if not using feature store
        
        # 2. Train Model using business logic defined in model_building/train.py
        model = build_model(training_set)
        
        # 3. Log the Model 
        # fe_client.log_model(
        #     model=model,
        #     artifact_path="model",
        #     registered_model_name=config.fully_qualified_model_name,
        #     training_set=training_set
        # )
        
        logger.info(f"Model trained and registered to {config.fully_qualified_model_name}")
        
if __name__ == "__main__":
    app()
