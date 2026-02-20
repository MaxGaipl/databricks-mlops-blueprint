import logging
import mlflow

logger = logging.getLogger(__name__)

def build_model(training_set):
    """
    Template function to train your machine learning model.
    
    USER TODO: Add your custom model training logic here.
    For example:
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor()
        model.fit(X, y)
        return model
        
    Args:
        training_set: The training dataset retrieved from the Feature Store.
        
    Returns:
        The trained machine learning model.
    """
    logger.info("Building machine learning model (business logic)...")
    
    # -------------------------------------------------------------
    # USER CODE GOES HERE: Implement your model training
    # -------------------------------------------------------------
    # model = ...
    
    model = None
    # -------------------------------------------------------------
    
    return model
