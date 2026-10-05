from pydantic import Field
from pydantic import BaseModel


class ChurnInput(BaseModel):
    total_pedidos: int = Field(..., gt=0, description="Total de pedidos")
    receita_total_em_usd: float = Field(
        ..., gt=0, description="Receita total em dólares"
    )
    ticket_medio_em_usd: float = Field(..., gt=0, description="Ticket médio em dólares")
    recencia_dias: int = Field(..., ge=0, description="Dias desde o último pedido")
    dias_desde_primeiro_pedido: int = Field(
        ..., ge=0, description="Dias desde o primeiro pedido"
    )
    tempo_relacionamento_dias: int = Field(
        ..., ge=0, description="Tempo total de relacionamento em dias"
    )
    total_itens_comprados: int = Field(
        ..., ge=0, description="Total de itens comprados"
    )
    total_interacoes_quinzena_1: int = Field(
        ..., ge=0, description="Total de interações na primeira quinzena"
    )
    total_interacoes_quinzena_2: int = Field(
        ..., ge=0, description="Total de interações na segunda quinzena"
    )
    total_interacoes_quinzena_3: int = Field(
        ..., ge=0, description="Total de interações na terceira quinzena"
    )
    total_interacoes_quinzena_4: int = Field(
        ..., ge=0, description="Total de interações na quarta quinzena"
    )


class ChurnOutput(BaseModel):
    predicao_classe: int = Field(..., ge=0, le=1, description="Predição de churn")
    predicao_probabilidade: float = Field(
        ..., ge=0, le=1, description="Probabilidade de churn"
    )
    predicao_status: str = Field(..., description="Status da predição")