from ga4_churn_predictor.config import TEST_SIZE
from ga4_churn_predictor.config import RANDOM_STATE
from ga4_churn_predictor.config import TARGET_FEATURE
from ga4_churn_predictor.config import CATEGORICAL_FEATURES
from ga4_churn_predictor.config import RAW_NUMERICAL_FEATURES
from ga4_churn_predictor.config import DATA_PATH
from ga4_churn_predictor.config import BIGQUERY_PROJECT_ID
from ga4_churn_predictor.config import GOOGLE_APPLICATION_CREDENTIALS
from ga4_churn_predictor.config import SQL_QUERY_PATH
from sklearn.model_selection import train_test_split
from google.cloud import bigquery
import pandas
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(GOOGLE_APPLICATION_CREDENTIALS)


def fetch_and_save_data():
    gbq_client = bigquery.Client(project=BIGQUERY_PROJECT_ID)

    query = SQL_QUERY_PATH.read_text(encoding="utf-8")

    dataframe = gbq_client.query(query).to_dataframe()
    dataframe.to_parquet(DATA_PATH, index=False)

    print(f"Data fetched and saved to {DATA_PATH}")


if __name__ == "__main__":
    fetch_and_save_data()


dataframe = pandas.read_parquet(DATA_PATH)

X = dataframe[RAW_NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
y = dataframe[TARGET_FEATURE]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=RANDOM_STATE, test_size=TEST_SIZE
)
