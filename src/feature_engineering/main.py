import typer
import logging
from mlops_blueprint.config.config import ProjectConfig
from databricks.connect import DatabricksSession
from mlops_blueprint.feature_engineering.compute_features import compute_features

# Optional: Add databricks feature store import
# from databricks.feature_engineering import FeatureEngineeringClient

# from databricks.feature_engineering import FeatureEngineeringClient

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

    logger.info(f"Loaded config for env: {config.environment}")

    # Establish spark connection via connect or native runner
    # Because DatabricksSession is smart, it seamlessly connects locally or acts natively inside the cluster
    spark = DatabricksSession.builder.getOrCreate()
    
    logger.info(f"Reading from {config.training_data_path}...")
    df = spark.table(config.training_data_path)
    
    # --------------------------
    # Execute Feature Logic
    # --------------------------
    # Calls the business logic defined in transformations/compute_features.py
    transformed_df = compute_features(df)
    
    # Write to feature store / unity catalog
    feature_table = f"{config.catalog}.{config.schema}.features_table"
    logger.info(f"Feature engineering complete. Prepared to write to {feature_table}")
    
    # fe = FeatureEngineeringClient()
    # fe.create_table(name=feature_table, df=transformed_df, ...) 

if __name__ == "__main__":
    app()
