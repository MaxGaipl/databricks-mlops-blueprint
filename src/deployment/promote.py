import logging
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)

def promote_model(client: MlflowClient, model_name: str):
    """
    Template function to manage model deployment and registry aliases.
    
    BEST PRACTICE: Make your business logic completely independent of the
    Databricks environment. Pass required clients (like MlflowClient) as arguments 
    rather than initializing them globally or relying on Databricks notebook context.

    USER TODO: Add your custom promotion logic here.
    For example:
        # Fetch the model version with "challenger" alias and promote to "champion"
        challenger_version = client.get_model_version_by_alias(model_name, "challenger")
        client.set_registered_model_alias(model_name, "champion", challenger_version.version)
        
    Args:
        client: The MlflowClient instance to interact with the model registry.
        model_name: The fully qualified name of the model in Unity Catalog.
    """
    logger.info(f"Promoting model {model_name} in registry (business logic)...")
    
    # -------------------------------------------------------------
    # USER CODE GOES HERE: Implement your deployment and promotion logic
    # -------------------------------------------------------------
    try:
        challenger_version = client.get_model_version_by_alias(model_name, "challenger")
        logger.info(f"Promoting version {challenger_version.version} to champion")
        
        client.set_registered_model_alias(model_name, "champion", challenger_version.version)
        logger.info("Successfully deployed model to champion alias.")
    except Exception as e:
        logger.error(f"Failed to find or assign challenger model. Error: {e}")
        raise
    # -------------------------------------------------------------
