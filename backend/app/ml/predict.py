import pandas as pd
import logging
from typing import Dict, Any

from app.ml.model_loader import ml_models

logger = logging.getLogger(__name__)

class PredictionService:
    @staticmethod
    def predict_delay(features: Dict[str, Any]) -> dict:
        """
        Takes raw features, applies preprocessing, and returns the prediction.
        """
        model, preprocessor = ml_models.get_models()
        
        if model is None or preprocessor is None:
            raise RuntimeError("ML model or preprocessor is not loaded. Cannot make predictions.")
            
        try:
            # Convert single dictionary to DataFrame
            df = pd.DataFrame([features])
            
            # Preprocess
            X_processed = preprocessor.transform(df)
            
            # Predict
            prediction = model.predict(X_processed)[0]
            probability = model.predict_proba(X_processed)[0][1]
            
            result = "Delayed" if prediction == 1 else "Not Delayed"
            confidence = f"{probability * 100:.1f}%" if prediction == 1 else f"{(1 - probability) * 100:.1f}%"
            
            return {
                "prediction": result,
                "delay_probability": round(float(probability), 4),
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
