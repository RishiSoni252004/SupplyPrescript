import os
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)
import logging
from app.ml.preprocess import DataPreprocessor

# Configure basic logging for script execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def train_model(data_path="backend/data/shipments.csv", models_dir="backend/models"):
    """
    Trains the XGBoost model for shipment delay prediction.
    Loads data, preprocesses it, trains the model, logs evaluation metrics,
    and saves the artifacts to the specified directory.
    """
    try:
        # 1. Load data
        logger.info(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
        
        # 2. Separate features and target
        # shipment_id is an identifier, actual_delivery_days is an outcome variable that would cause data leakage
        X = df.drop(columns=["shipment_id", "actual_delivery_days", "delayed"])
        y = df["delayed"]
        
        # 3. Train-test split
        logger.info("Splitting dataset into train and test sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # 4. Preprocessing
        logger.info("Initializing and fitting preprocessor...")
        preprocessor = DataPreprocessor()
        X_train_processed = preprocessor.fit_transform(X_train)
        X_test_processed = preprocessor.transform(X_test)
        
        # 5. Model Training & Hyperparameter Tuning
        logger.info("Performing hyperparameter tuning with GridSearchCV to improve accuracy...")
        base_model = XGBClassifier(
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss"
        )
        
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.05, 0.1],
            'max_depth': [5, 7],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }
        
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=3,
            scoring='roc_auc',
            n_jobs=-1
        )
        grid_search.fit(X_train_processed, y_train)
        
        logger.info(f"Best parameters found: {grid_search.best_params_}")
        model = grid_search.best_estimator_
        
        # 6. Evaluation
        logger.info("Evaluating model...")
        y_pred = model.predict(X_test_processed)
        y_pred_proba = model.predict_proba(X_test_processed)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        cm = confusion_matrix(y_test, y_pred)
        
        logger.info(f"--- Model Evaluation Metrics ---")
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        logger.info(f"ROC-AUC:   {roc_auc:.4f}")
        logger.info(f"Confusion Matrix:\n{cm}")
        
        # 7. Save Artifacts
        os.makedirs(models_dir, exist_ok=True)
        preprocessor_path = os.path.join(models_dir, "preprocessor.pkl")
        model_path = os.path.join(models_dir, "xgboost_model.pkl")
        
        logger.info("Saving model artifacts...")
        joblib.dump(preprocessor, preprocessor_path)
        joblib.dump(model, model_path)
        logger.info(f"Artifacts saved to {models_dir}")
        
    except Exception as e:
        logger.error(f"Failed during model training: {e}")
        raise

if __name__ == "__main__":
    # Handle absolute paths for easy running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(script_dir)
    backend_dir = os.path.dirname(app_dir)
    
    data_path = os.path.join(backend_dir, "data", "shipments.csv")
    models_dir = os.path.join(backend_dir, "models")
    
    train_model(data_path=data_path, models_dir=models_dir)
