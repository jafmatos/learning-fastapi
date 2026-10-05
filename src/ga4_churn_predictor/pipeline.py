from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from ga4_churn_predictor.config import CATEGORICAL_FEATURES
from ga4_churn_predictor.config import MODEL_NUMERICAL_FEATURES
from pandas import DataFrame
from ga4_churn_predictor.config import RANDOM_STATE
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def feature_engineering(dataframe: DataFrame):
    dataframe = dataframe.copy()

    dataframe["tendencia_interacoes"] = (
        -3 * dataframe["total_interacoes_quinzena_1"]
        - 1 * dataframe["total_interacoes_quinzena_2"]
        + 1 * dataframe["total_interacoes_quinzena_3"]
        + 3 * dataframe["total_interacoes_quinzena_4"]
    ) / 10
    dataframe["media_dias_entre_pedidos"] = dataframe["tempo_relacionamento_dias"] / dataframe["total_pedidos"]
    dataframe["fator_recencia"] = dataframe["recencia_dias"] / dataframe["media_dias_entre_pedidos"]

    dataframe.replace([-numpy.inf, numpy.inf], numpy.nan, inplace=True)

    return dataframe


FeatureTransformer = FunctionTransformer(feature_engineering)

column_transformer = ColumnTransformer(
    transformers=[
        ("imputer", SimpleImputer(strategy="median"), MODEL_NUMERICAL_FEATURES),
    ],
    remainder="drop",
)

pipeline = Pipeline(
    steps=[
        ("feature_engineering", FeatureTransformer),
        ("column_transformer", column_transformer),
        (
            "model",
            HistGradientBoostingClassifier(random_state=RANDOM_STATE, class_weight="balanced"),
        ),
    ]
)
