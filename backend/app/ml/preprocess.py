import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.numerical_features = [
            "distance_km",
            "shipping_cost",
            "expected_delivery_days"
        ]
        
        self.categorical_features = [
            "supplier",
            "origin",
            "destination",
            "transport_mode",
            "weather_condition",
            "traffic_level",
            "order_priority"
        ]
        
        # Define preprocessing for numerical columns (impute missing -> scale)
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        # Define preprocessing for categorical columns (impute missing -> onehot)
        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])

        # Combine preprocessing steps
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numerical_features),
                ("cat", categorical_transformer, self.categorical_features)
            ]
        )
        
        self.is_fitted = False

    def fit_transform(self, df: pd.DataFrame):
        """Fit the preprocessor to the data and transform it."""
        try:
            logger.info("Fitting and transforming data...")
            transformed_data = self.preprocessor.fit_transform(df)
            self.is_fitted = True
            return transformed_data
        except Exception as e:
            logger.error(f"Error during fit_transform: {e}")
            raise

    def transform(self, df: pd.DataFrame):
        """Transform new data using the fitted preprocessor."""
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        try:
            return self.preprocessor.transform(df)
        except Exception as e:
            logger.error(f"Error during transform: {e}")
            raise

    def get_feature_names_out(self):
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        return self.preprocessor.get_feature_names_out()
