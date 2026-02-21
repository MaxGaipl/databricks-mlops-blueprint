import logging
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

def compute_features(df: DataFrame, spark: SparkSession = None) -> DataFrame:
    """
    Template function to apply feature engineering transformations.
    
    BEST PRACTICE: Make your business logic completely independent of the
    Databricks environment. Avoid using the global `spark` or `dbutils` objects 
    (the `__builtins__`). Instead, pass the DataFrames directly or pass the 
    SparkSession as an argument. This ensures your code is testable locally 
    via pytest without needing to mock runtime globals.

    USER TODO: Add your custom feature engineering logic here.
    For example:
        from pyspark.sql import functions as F
        result_df = df.withColumn("day_of_week", F.dayofweek("pickup_datetime"))
        return result_df
        
    Args:
        df: Input Spark DataFrame containing raw training data.
        spark: (Optional) The SparkSession, explicitly passed if needed to create new DataFrames.
        
    Returns:
        Spark DataFrame containing the engineered features.
    """
    logger.info("Computing features (business logic)...")
    
    # -------------------------------------------------------------
    # USER CODE GOES HERE: Implement your feature transformations
    # -------------------------------------------------------------
    # Example placeholder:
    # df = df.withColumn("computed_feature", ...)
    
    result_df = df 
    # -------------------------------------------------------------
    
    return result_df
