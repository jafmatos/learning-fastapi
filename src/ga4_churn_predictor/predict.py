import pandas
import joblib
from pathlib import Path
from functools import lru_cache
from sklearn.pipeline import Pipeline
from ga4_churn_predictor.config import RAW_NUMERICAL_FEATURES
from ga4_churn_predictor.config import CATEGORICAL_FEATURES
from ga4_churn_predictor.config import MODEL_PATH


REQUIRED_COLUMNS = RAW_NUMERICAL_FEATURES + CATEGORICAL_FEATURES


@lru_cache(maxsize=1)
def load_model(model_path: Path | str | None = None) -> Pipeline:
    path = Path(model_path) if model_path else Path(MODEL_PATH)

    if not path.exists():
        raise FileNotFoundError(f"Modelo não encontrado em '{path}'")

    return joblib.load(path)


def predict_single(
    model: Pipeline,
    total_pedidos: int,
    receita_total_em_usd: float,
    ticket_medio_em_usd: float,
    recencia_dias: int,
    dias_desde_primeiro_pedido: int,
    tempo_relacionamento_dias: int,
    total_itens_comprados: int,
    total_interacoes_quinzena_1: int,
    total_interacoes_quinzena_2: int,
    total_interacoes_quinzena_3: int,
    total_interacoes_quinzena_4: int,
) -> dict:
    input_dataframe = pandas.DataFrame(
        {
            "total_pedidos": [total_pedidos],
            "receita_total_em_usd": [receita_total_em_usd],
            "ticket_medio_em_usd": [ticket_medio_em_usd],
            "recencia_dias": [recencia_dias],
            "dias_desde_primeiro_pedido": [dias_desde_primeiro_pedido],
            "tempo_relacionamento_dias": [tempo_relacionamento_dias],
            "total_itens_comprados": [total_itens_comprados],
            "total_interacoes_quinzena_1": [total_interacoes_quinzena_1],
            "total_interacoes_quinzena_2": [total_interacoes_quinzena_2],
            "total_interacoes_quinzena_3": [total_interacoes_quinzena_3],
            "total_interacoes_quinzena_4": [total_interacoes_quinzena_4],
        }
    )

    prediction = model.predict(input_dataframe)
    prediction_probability = model.predict_proba(input_dataframe)
    prediction_class = int(prediction[0])

    return {
        "predicao_classe": prediction_class,
        "predicao_probabilidade": round(float(prediction_probability[0, 1]), 2),
        "predicao_status": "Churn" if prediction_class == 1 else "Ativo",
    }


def predict_batch(model: Pipeline, data: list[dict]):
    input_dataframe = pandas.DataFrame(data)

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in input_dataframe.columns
    ]

    if missing_columns:
        raise ValueError(f"Colunas faltando: {missing_columns}")

    predictions = model.predict(input_dataframe)
    probabilities = model.predict_proba(input_dataframe)

    output_dataframe = input_dataframe.copy()
    output_dataframe["predicao_classe"] = predictions.astype(int)
    output_dataframe["predicao_probabilidade"] = probabilities[:, 1].round(2)
    output_dataframe["predicao_status"] = output_dataframe["predicao_classe"].map(lambda x: "Churn" if x == 1 else "Ativo")

    return output_dataframe.to_dict("records")
