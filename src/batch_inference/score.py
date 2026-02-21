import logging
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

def score_batch(model_uri: str, input_df: DataFrame, spark: SparkSession = None) -> DataFrame:
    """
    Template function to perform batch inference using a trained model.
    
    BEST PRACTICE: Make your business logic completely independent of the
    Databricks environment. Avoid using the global `spark` or `dbutils` objects 
    (the `__builtins__`). Instead, pass DataFrames directly or pass the 
    SparkSession as an argument. This ensures local testability.

    USER TODO: Add your custom scoring logic here.
    For example:
        # from databricks.feature_engineering import FeatureEngineeringClient
        # fe_client = FeatureEngineeringClient()
        # result_df = fe_client.score_batch(model_uri=model_uri, df=input_df)
        # return result_df
        
    Args:
        model_uri: The URI of the model to use for inference (e.g. models:/<name>@champion).
        input_df: The input Spark DataFrame to score.
        spark: (Optional) The SparkSession.
        
    Returns:
        Spark DataFrame containing the predictions.
    """
    logger.info(f"Scoring batch data using model {model_uri} (business logic)...")
    
    # -------------------------------------------------------------
    # USER CODE GOES HERE: Implement your batch scoring logic
    # -------------------------------------------------------------
    # result_df = fe_client.score_batch(...)
    
    result_df = input_df
    # -------------------------------------------------------------
    
    return result_df
