from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SQL_DIR = ROOT_DIR / "sql"
SQL_QUERY_PATH = SQL_DIR / "ga4_event_query.sql"
PROCESSED_DATASET_DIR = ROOT_DIR / "dataset" / "processed"
RAW_DATASET_DIR = ROOT_DIR / "dataset" / "raw"
DATA_PATH = RAW_DATASET_DIR / "users.parquet"
MODEL_PATH = ROOT_DIR / "models" / "churn_model.joblib"
GOOGLE_APPLICATION_CREDENTIALS = ROOT_DIR / "key" / "sandbox-508815-5323cef31685.json"
BIGQUERY_PROJECT_ID = "sandbox-508815"

TEST_SIZE = 0.2
RANDOM_STATE = 42

RAW_NUMERICAL_FEATURES = [
    "total_pedidos",
    "receita_total_em_usd",
    "ticket_medio_em_usd",
    "recencia_dias",
    "dias_desde_primeiro_pedido",
    "tempo_relacionamento_dias",
    "total_itens_comprados",
    "total_interacoes_quinzena_1",
    "total_interacoes_quinzena_2",
    "total_interacoes_quinzena_3",
    "total_interacoes_quinzena_4",
]

MODEL_NUMERICAL_FEATURES = [
    "ticket_medio_em_usd",
    "recencia_dias",
    "dias_desde_primeiro_pedido",
    "tempo_relacionamento_dias",
    "total_itens_comprados",
    "tendencia_interacoes",
    "media_dias_entre_pedidos"
]

CATEGORICAL_FEATURES = []

TARGET_FEATURE = "churn"
