import os
import joblib
import logging
from typing import Tuple, Any, Optional

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.preprocessor = None
            cls._instance.is_loaded = False
        return cls._instance

    def load_models(self, models_dir: str = "models") -> None:
        """Load the ML model and preprocessor into memory."""
        if self.is_loaded:
            logger.info("Models already loaded.")
            return

        try:
            # We want to use absolute paths based on project root if possible, or relative to this file
            if not os.path.isabs(models_dir):
                # assume models_dir is relative to backend root
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                models_dir = os.path.join(base_dir, models_dir)

            preprocessor_path = os.path.join(models_dir, "preprocessor.pkl")
            model_path = os.path.join(models_dir, "xgboost_model.pkl")

            if not os.path.exists(preprocessor_path) or not os.path.exists(model_path):
                logger.error("Model or preprocessor files not found. Please train the model first.")
                return

            logger.info("Loading preprocessor and model...")
            self.preprocessor = joblib.load(preprocessor_path)
            self.model = joblib.load(model_path)
            self.is_loaded = True
            logger.info("Successfully loaded ML models.")
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise

    def get_models(self) -> Tuple[Optional[Any], Optional[Any]]:
        """Return the loaded model and preprocessor."""
        return self.model, self.preprocessor

    def get_model_info(self) -> dict:
        """Return metadata about the trained model."""
        if not self.is_loaded or self.model is None or self.preprocessor is None:
            return {"status": "Model not loaded"}

        # Basic metadata
        try:
            features = self.preprocessor.get_feature_names_out().tolist()
        except:
            features = []

        return {
            "model_name": "Shipment Delay Predictor",
            "algorithm": type(self.model).__name__,
            "features_used": features,
            "status": "Loaded and Ready"
        }

# Global instance
ml_models = ModelLoader()
