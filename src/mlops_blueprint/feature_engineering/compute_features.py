import logging
from pyspark.sql import DataFrame

logger = logging.getLogger(__name__)

def compute_features(df: DataFrame) -> DataFrame:
    """
    Template function to apply feature engineering transformations.
    
    USER TODO: Add your custom feature engineering logic here.
    For example:
        from pyspark.sql import functions as F
        result_df = df.withColumn("day_of_week", F.dayofweek("pickup_datetime"))
        return result_df
        
    Args:
        df: Input Spark DataFrame containing raw training data.
        
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
