from pandas import DataFrame
import gc as garbage_colector
from pydantic import TypeAdapter
from app.schemas.prediction import ChurnInput
from app.schemas.prediction import ChurnOutput
from ga4_churn_predictor.predict import load_model
from ga4_churn_predictor.predict import predict_single, predict_batch, predict_dataframe

churn_output_list_adapter = TypeAdapter(list[ChurnOutput])


class MLService:
    def __init__(self):
        self.model = None

    def load_model(self):
        self.model = load_model()

    def unload_model(self):
        self.model = None

        load_model.cache_clear()

        garbage_colector.collect()

    def predict_single(self, data: ChurnInput) -> ChurnOutput:
        if self.model is None:
            raise RuntimeError("O modelo não foi carregado")

        output = predict_single(
            self.model,
            total_pedidos=data.total_pedidos,
            receita_total_em_usd=data.receita_total_em_usd,
            ticket_medio_em_usd=data.ticket_medio_em_usd,
            recencia_dias=data.recencia_dias,
            dias_desde_primeiro_pedido=data.dias_desde_primeiro_pedido,
            tempo_relacionamento_dias=data.tempo_relacionamento_dias,
            total_itens_comprados=data.total_itens_comprados,
            total_interacoes_quinzena_1=data.total_interacoes_quinzena_1,
            total_interacoes_quinzena_2=data.total_interacoes_quinzena_2,
            total_interacoes_quinzena_3=data.total_interacoes_quinzena_3,
            total_interacoes_quinzena_4=data.total_interacoes_quinzena_4,
        )

        return ChurnOutput(
            predicao_classe=output["predicao_classe"],
            predicao_probabilidade=output["predicao_probabilidade"],
            predicao_status=output["predicao_status"],
        )

    def predict_batch(self, data: list[ChurnInput]) -> list[ChurnOutput]:
        if self.model is None:
            raise RuntimeError("O modelo não foi carregado")

        data_as_dict_list = [item.model_dump() for item in data]

        output = predict_batch(self.model, data=data_as_dict_list)

        return churn_output_list_adapter.validate_python(output)

    def predict_dataframe(self, data: DataFrame) -> DataFrame:
        if self.model is None:
            raise RuntimeError("O modelo não foi carregado")

        output_dataframe = predict_dataframe(self.model, data)

        return output_dataframe


ml_service = MLService()


def get_ml_service() -> MLService:
    return ml_service
