from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from ga4_churn_predictor.data import y_test
from sklearn.metrics import classification_report
from ga4_churn_predictor.data import X_test
from ga4_churn_predictor.config import MODEL_PATH
import joblib

model = joblib.load(MODEL_PATH)

y_pred = model.predict(X_test)

print(f"""
Classification Report:

{classification_report(y_test, y_pred)}
""")

print(f"""
ROC AUC Score:

{roc_auc_score(y_test, y_pred):.2f}
""")

print(f"""
Confusion Matrix:

{confusion_matrix(y_test, y_pred)}
""")
