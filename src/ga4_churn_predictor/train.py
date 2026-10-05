from ga4_churn_predictor.data import y_train
from ga4_churn_predictor.data import X_train
from ga4_churn_predictor.pipeline import pipeline
from ga4_churn_predictor.config import MODEL_PATH
import joblib

def train_and_save_model():
    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, MODEL_PATH)

if __name__ == "__main__":
    train_and_save_model()