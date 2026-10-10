# 📘 Guia Definitivo de FastAPI: Arquitetura Modular de Produção

Este guia é uma referência completa e prática sobre **FastAPI**, construído desde a primeira linha em torno da **arquitetura de pastas modular e profissional** recomendada para ambientes corporativos e projetos de Machine Learning / MLOps.

---

## 📑 Índice

1. [A Estrutura de Pastas Ideal e Inicialização do Projeto](#1-a-estrutura-de-pastas-ideal-e-inicialização-do-projeto)
2. [Configurações e Variáveis de Ambiente com `.env` (`src/app/config.py`)](#2-configurações-e-variáveis-de-ambiente-com-env-srcappconfigpy)
3. [Contratos de Dados e Validação com Pydantic v2 (`src/app/schemas/`)](#3-contratos-de-dados-e-validação-com-pydantic-v2-srcappschemas)
   - [3.1 Schema de Inferência (Entrada e Saída)](#31-schema-de-inferência-srcappschemaspredictionpy)
   - [3.2 Evoluindo o `config.py`: Validando o `.env` com Pydantic Settings](#32-evoluindo-o-configpy-validando-o-env-com-pydantic-settings)
4. [Injeção de Dependências e Banco de Dados (`src/app/database.py`)](#4-injeção-de-dependências-e-banco-de-dados-srcappdatabasepy)
5. [Camada de Serviço e Inferência de IA (`src/app/services/`)](#5-camada-de-serviço-e-inferência-de-ia-srcappservices)
6. [Roteamento Modular e Parâmetros HTTP (`src/app/routers/`)](#6-roteamento-modular-e-parâmetros-http-srcapprouters)
   - [6.1 Rota de Monitoramento (`health.py`)](#61-rota-de-monitoramento-srcapproutershealthpy)
   - [6.2 Rotas de Inferência (`predict.py`)](#62-rotas-de-inferência-srcapprouterspredictpy)
   - [6.3 Tipos de Parâmetros HTTP (Body, Path, Query, Header)](#63-tipos-de-parâmetros-http-body-path-query-header)
7. [Segurança e Autenticação por API Key (`src/app/security.py`)](#7-segurança-e-autenticação-por-api-key-srcappsecuritypy)
8. [Orquestração Principal, Ciclo de Vida e Middlewares (`src/app/main.py`)](#8-orquestração-principal-ciclo-de-vida-e-middlewares-srcappmainpy)
   - [8.1 Registrando os Routers](#81-registrando-os-routers)
   - [8.2 Ciclo de Vida com `lifespan` (Carregamento da IA na RAM)](#82-ciclo-de-vida-com-lifespan-carregamento-da-ia-na-ram)
   - [8.3 Middlewares de Produção (CORS e Medição de Latência)](#83-middlewares-de-produção-cors-e-medição-de-latência)
9. [Tratamento Robusto de Exceções e Respostas de Erro](#9-tratamento-robusto-de-exceções-e-respostas-de-erro)
10. [Tarefas em Segundo Plano para MLOps (`BackgroundTasks`)](#10-tarefas-em-segundo-plano-para-mlops-backgroundtasks)
11. [Containerização com Docker para Produção](#11-containerização-com-docker-para-produção)
12. [Upload e Processamento de Arquivos em Data Science (`UploadFile` e `File`)](#12-upload-e-processamento-de-arquivos-em-data-science-uploadfile-e-file)
13. [Comandos de Terminal Essenciais (Cheat Sheet)](#13-comandos-de-terminal-essenciais-cheat-sheet)

---

## 1. A Estrutura de Pastas Ideal e Inicialização do Projeto

Em projetos profissionais (especialmente em Ciência de Dados e IA), **nunca** colocamos todo o código em um único arquivo `main.py` na raiz. Separamos o projeto em módulos coesos onde cada camada tem uma única responsabilidade.

### 1.1 A Árvore de Diretórios Padrão da Indústria

```text
meu_projeto/
│
├── models/                           # 🧠 Artefatos gerados pelo treino (.joblib, .onnx)
│   └── churn_model.joblib
│
├── notebooks/                        # 📓 Experimentação, análises e EDA
│   └── analise.ipynb
│
├── src/
│   ├── app/                          # 🚀 PACOTE PRINCIPAL DA API FASTAPI
│   │   ├── __init__.py
│   │   ├── config.py                 # Variáveis de ambiente (.env) e constantes
│   │   ├── database.py               # Sessão SQLAlchemy (Depends com yield)
│   │   ├── security.py               # Autenticação por API Key (M2M) e dependências de segurança
│   │   │
│   │   ├── schemas/                  # Contratos de dados (Pydantic Models)
│   │   │   ├── __init__.py
│   │   │   └── prediction.py         # Schemas de Entrada e Saída
│   │   │
│   │   ├── services/                 # Lógica de negócio pura (sem código HTTP)
│   │   │   ├── __init__.py
│   │   │   └── ml_service.py         # Carregamento e inferência do modelo
│   │   │
│   │   ├── routers/                  # Endpoints separados por domínio
│   │   │   ├── __init__.py
│   │   │   ├── health.py             # GET /health
│   │   │   └── predict.py            # POST /predict e POST /predict/batch
│   │   │
│   │   └── main.py                   # Ponto de entrada (FastAPI, Lifespan, Middlewares)
│   │
│   └── ga4_churn_predictor/          # 🔬 PACOTE DE MACHINE LEARNING (Treinamento isolado)
│       ├── data.py
│       ├── pipeline.py
│       ├── train.py
│       └── predict.py
│
├── .env                              # Segredos e variáveis de ambiente (fora do Git)
├── Dockerfile                        # Conteinerização para nuvem/Kubernetes
├── pyproject.toml / requirements.txt # Gerenciador de dependências
└── README.md
```

### 1.2 Como Inicializar essa Estrutura no Terminal

```bash
# 1. Cria a raiz do projeto e acessa
mkdir meu_projeto && cd meu_projeto

# 2. Cria e ativa o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 3. Instala o FastAPI com as ferramentas padrão e o python-dotenv
pip install --upgrade pip
pip install "fastapi[standard]" python-dotenv

# 4. Cria a árvore de pastas profissional de uma só vez
mkdir -p models notebooks src/app/schemas src/app/services src/app/routers

# 5. Cria os arquivos iniciais com __init__.py
touch src/app/__init__.py
touch src/app/schemas/__init__.py
touch src/app/services/__init__.py
touch src/app/routers/__init__.py
touch src/app/config.py src/app/database.py src/app/security.py src/app/main.py
```

### 1.3 Como Executar a API a partir da Raiz

Como a aplicação reside em `src/app/main.py`, você deve executá-la da raiz do projeto usando a **notação de módulo em pontos (`.`)**:

```bash
# Opção A: Pelo utilitário oficial FastAPI CLI
fastapi dev src/app/main.py

# Opção B: Pelo Uvicorn clássico (Padrão de Produção)
uvicorn src.app.main:app --reload --port 8000
```

> **Por que `src.app.main:app`?**
>
> - `src.app.main`: Caminho do módulo Python a partir da raiz (`src/app/main.py`).
> - `:app`: Nome da variável instanciada (`app = FastAPI()`) dentro de `main.py`.
> - `--reload`: Reinicia o servidor instantaneamente ao detectar qualquer salvamento em qualquer arquivo.

Acesse no navegador:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 2. Configurações e Variáveis de Ambiente com `.env` (`src/app/config.py`)

Centralize todas as configurações e segredos usando variáveis de ambiente e o arquivo `.env`:

### 2.1 Arquivo `.env` (na raiz do projeto, fora do Git)

```env
API_TITLE="GA4 Churn Predictor API"
API_VERSION="1.0.0"
API_DESCRIPTION="API de Predição de Churn com Machine Learning"
API_SECRET_KEY="chave-super-secreta-producao-1234"
```

### 2.2 Arquivo `src/app/config.py`

```python
# src/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Raiz do projeto (sobe de 'app' -> 'src' -> raiz)
ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"

# Carrega as variáveis do .env se o arquivo existir
load_dotenv(ENV_PATH)

# Caminhos de arquivos essenciais
MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "churn_model.joblib"

# Configurações lidas do ambiente com valores padrão (fallbacks)
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = os.getenv("API_TITLE", "GA4 Churn Predictor API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API de Predição de Churn com Machine Learning")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "chave-padrao-dev")
```

---

## 3. Contratos de Dados e Validação com Pydantic v2 (`src/app/schemas/`)

Os schemas definem a garantia e integridade de entrada, além do contrato estrito de resposta (`response_model`).

### 3.1 Schema de Inferência (`src/app/schemas/prediction.py`)

```python
# src/app/schemas/prediction.py
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class ChurnInput(BaseModel):
    """
    Contrato estrito de entrada para predição.
    Todas as features necessárias para o modelo de Churn.
    """
    total_pedidos: int = Field(..., gt=0, description="Total de pedidos")
    receita_total_em_usd: float = Field(..., gt=0, description="Receita total em dólares")
    ticket_medio_em_usd: float = Field(..., gt=0, description="Ticket médio em dólares")
    recencia_dias: int = Field(..., ge=0, description="Dias desde o último pedido")
    dias_desde_primeiro_pedido: int = Field(..., ge=0, description="Dias desde o primeiro pedido")
    tempo_relacionamento_dias: int = Field(..., ge=0, description="Tempo total de relacionamento em dias")
    total_itens_comprados: int = Field(..., ge=0, description="Total de itens comprados")
    total_interacoes_quinzena_1: int = Field(..., ge=0, description="Total de interações na quinzena 1")
    total_interacoes_quinzena_2: int = Field(..., ge=0, description="Total de interações na quinzena 2")
    total_interacoes_quinzena_3: int = Field(..., ge=0, description="Total de interações na quinzena 3")
    total_interacoes_quinzena_4: int = Field(..., ge=0, description="Total de interações na quinzena 4")
    email_contato: Optional[str] = Field(None, description="E-mail opcional do cliente")

    @field_validator("email_contato")
    @classmethod
    def validar_email(cls, valor: Optional[str]):
        if valor is not None and "@" not in valor:
            raise ValueError("O e-mail informado é inválido: deve conter '@'.")
        return valor


class ChurnOutput(BaseModel):
    """
    Contrato de saída garantido ao cliente.
    """
    prediction_class: int = Field(..., ge=0, le=1, description="Predição de churn (0 ou 1)")
    prediction_probability: float = Field(..., ge=0.0, le=1.0, description="Probabilidade de churn")
    prediction_status: str = Field(..., description="Status da predição: 'Churn' ou 'Ativo'")
    versao_modelo: str = "1.0.0"
```

### 3.2 Evoluindo o `config.py`: Validando o `.env` com Pydantic Settings

Agora que você aprendeu como o Pydantic valida tipos (`float`, `int`, `str`) e campos obrigatórios com `BaseModel`, você pode aplicar exatamente **esse mesmo superpoder para validar o seu arquivo `.env`**!

No Tópico 2, usamos o `os.getenv()`, que lê tudo como texto puro (`str`) e não acusa erros imediatos se uma variável obrigatória for esquecida.
Com a biblioteca oficial **`pydantic-settings`**, transformamos as configurações em uma classe validada no momento da inicialização:

```bash
pip install pydantic-settings
```

Refatorando o `src/app/config.py` para usar validação estrita com Pydantic:

```python
# src/app/config.py
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """
    Configurações da aplicação validadas estritamente via Pydantic.
    Se faltar uma variável obrigatória ou o tipo for incompatível, a API nem inicializa!
    """
    API_TITLE: str = Field("GA4 Churn Predictor API", description="Título da API")
    API_VERSION: str = Field("1.0.0", description="Versão semântica")
    API_DESCRIPTION: str = Field("API de Predição de Churn com Machine Learning", description="Descrição do serviço")
    API_SECRET_KEY: str = Field(..., description="Chave de API obrigatória (deve estar definida no .env)")
    PORT: int = Field(8000, description="Porta HTTP da aplicação (convertida automaticamente para inteiro)")

    # Carrega automaticamente do arquivo .env na raiz do projeto
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instância única das configurações (Singleton)
settings = Settings()

# Atalhos para manter compatibilidade com imports existentes
API_TITLE = settings.API_TITLE
API_VERSION = settings.API_VERSION
API_DESCRIPTION = settings.API_DESCRIPTION
API_SECRET_KEY = settings.API_SECRET_KEY
```

> **Por que essa abordagem é superior em produção?**
>
> 1. **Falha Rápida (*Fail Fast*):** Se você esquecer de definir `API_SECRET_KEY` no `.env`, a API se recusa a iniciar e mostra uma mensagem de erro clara no terminal antes de atender requisições, evitando subir para a nuvem sem proteção.
> 2. **Conversão de Tipos Automática:** Variáveis como `PORT=8000` ou `DEBUG=True` no `.env` são convertidas e validadas automaticamente para `int` e `bool`.
> 3. **Autocomplete e Segurança na IDE:** Você ganha autocompletar ao digitar `settings.API_SECRET_KEY`, eliminando bugs por erro de digitação de strings (ex: `os.getenv("API_SECERT_KEY")`).

---

## 4. Injeção de Dependências e Banco de Dados (`src/app/database.py`)

A injeção de dependências (`Depends`) é um dos pilares mais poderosos do FastAPI. Usando **geradores (`yield`)**, garantimos que recursos pesados (como sessões de banco de dados SQLite, PostgreSQL ou conexões com serviços externos) sejam abertos antes da rota e **fechados garantidamente no `finally`**, mesmo se a rota disparar um erro:

```python
# src/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./banco.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependência canônica do FastAPI: abre uma sessão do banco e garante o fechamento no finally.
    Pode ser injetada em qualquer rota via: db_session: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 5. Camada de Serviço e Inferência de IA (`src/app/services/`)

A camada de serviço contém a **lógica pura de negócio**. Ela conecta os schemas do FastAPI com o pacote de Machine Learning (`ga4_churn_predictor`), permitindo que a API permaneça desacoplada:

```python
# src/app/services/ml_service.py
from ga4_churn_predictor.predict import load_model, predict_single, predict_batch
from app.schemas.prediction import ChurnInput, ChurnOutput

class MLService:
    def __init__(self):
        self.model = None

    def load_model(self):
        """Carrega o modelo compilado do disco para a memória RAM."""
        self.model = load_model()
        print("✅ [MLService] Modelo carregado na RAM com sucesso!")

    def unload_model(self):
        self.model = None

    def predict_single(self, data: ChurnInput) -> ChurnOutput:
        if self.model is None:
            raise RuntimeError("O modelo de Machine Learning não está carregado.")

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
            prediction_class=output["predicao_classe"],
            prediction_probability=output["predicao_probabilidade"],
            prediction_status=output["predicao_status"],
        )

    def predict_batch(self, data: list[ChurnInput]) -> list[ChurnOutput]:
        if self.model is None:
            raise RuntimeError("O modelo de Machine Learning não está carregado.")

        lista_dicionarios = [item.model_dump() for item in data]
        resultados = predict_batch(self.model, lista_dicionarios)

        return [
            ChurnOutput(
                prediction_class=res["predicao_classe"],
                prediction_probability=res["predicao_probabilidade"],
                prediction_status=res["predicao_status"],
            )
            for res in resultados
        ]

# Instância única compartilhada (Singleton)
ml_service = MLService()
```

---

## 6. Roteamento Modular e Parâmetros HTTP (`src/app/routers/`)

Agora que temos **Schemas (Tópico 3)**, **Dependências (Tópico 4)** e o **Serviço de IA (Tópico 5)**, o próximo passo natural é **expor as rotas HTTP**.

Dividimos as rotas em arquivos separados utilizando o `APIRouter`.

### 6.1 Rota de Monitoramento (`src/app/routers/health.py`)

```python
# src/app/routers/health.py
from fastapi import APIRouter
from app.services.ml_service import ml_service

router = APIRouter(prefix="/health", tags=["Monitoramento"])

@router.get("")
def checar_saude():
    """Endpoint público para Docker, Kubernetes e Cloud Liveness/Readiness probes."""
    modelo_pronto = ml_service.model is not None
    return {
        "status": "healthy" if modelo_pronto else "degraded",
        "modelo_carregado": modelo_pronto
    }
```

### 6.2 Rotas de Inferência (`src/app/routers/predict.py`)

A rota recebe o schema `ChurnInput`, chama o `ml_service` e garante a resposta através de `response_model=ChurnOutput`:

```python
# src/app/routers/predict.py
from fastapi import APIRouter
from app.schemas.prediction import ChurnInput, ChurnOutput
from app.services.ml_service import ml_service

router = APIRouter(prefix="/predict", tags=["Predição de IA"])

@router.post("", response_model=ChurnOutput)
def prever_unitario(cliente: ChurnInput):
    """Executa a inferência para um único cliente."""
    return ml_service.predict_single(cliente)


@router.post("/batch", response_model=list[ChurnOutput])
def prever_lote(clientes: list[ChurnInput]):
    """Executa a inferência em lote para uma lista de clientes."""
    return ml_service.predict_batch(clientes)
```

### 6.3 Tipos de Parâmetros HTTP (Body, Path, Query, Header)

O FastAPI descobre automaticamente como extrair cada dado analisando a assinatura da função:

```python
from fastapi import APIRouter, Path, Query, Header, Cookie
from typing import Optional, List

router = APIRouter()

@router.get("/clientes/{cliente_id}")
def buscar_cliente(
    # 1. Path Parameter: obrigatório na URL (/clientes/42)
    cliente_id: int = Path(..., ge=1, le=999999, description="ID único do cliente"),
  
    # 2. Query Parameters: filtros opcionais (?ordenar=data&limite=50)
    ordenar: str = Query("data", enum=["data", "score", "valor"]),
    limite: int = Query(20, ge=1, le=100),
    tags: Optional[List[str]] = Query(None),
  
    # 3. Header Parameter: lido do cabeçalho da requisição
    user_agent: Optional[str] = Header(None),
  
    # 4. Cookie Parameter: lido de cookies do navegador
    session_token: Optional[str] = Cookie(None)
):
    return {
        "cliente_id": cliente_id,
        "ordenar": ordenar,
        "limite": limite,
        "tags": tags,
        "user_agent": user_agent
    }
```

---

## 7. Segurança e Autenticação por API Key (`src/app/security.py`)

Agora que as rotas estão no ar e funcionando, qualquer pessoa na internet pode chamar seu endpoint e gastar a sua CPU. **É o momento exato de blindar a API.**

Para comunicação Machine-to-Machine (M2M) — como dashboards do Streamlit, pipelines ou microsserviços —, o padrão de **API Key** via cabeçalho HTTP é o mais indicado.

Entender como isso funciona fica muito mais intuitivo quando dividimos em **duas formas**: uma simples e direta (com `Header` e `Depends`) e uma robusta (padrão de produção com `APIKeyHeader` e `Security`).

---

### 7.1 O que é uma API Key por baixo dos panos?

Uma API Key nada mais é do que um **cabeçalho HTTP customizado** (por convenção, chamado de `X-API-KEY`) que o cliente envia na requisição. O servidor simplesmente lê esse cabeçalho e verifica: *"Essa chave é igual à chave secreta configurada no sistema?"* Se for igual, permite a execução; se não for, devolve **HTTP 403 Forbidden**.

---

### 7.2 Forma 1: A Abordagem Simples (Com `Header` e `Depends`)

Como você já aprendeu a usar `Header(...)` no Tópico 6, você pode criar uma validação simples e direta:

```python
# Exemplo didático com Header e Depends
from fastapi import Header, HTTPException, status, Depends
from app.config import API_SECRET_KEY

def validar_api_key_simples(x_api_key: str = Header(..., description="Chave de acesso da API")) -> str:
    """Lê o cabeçalho X-API-KEY e compara diretamente."""
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Chave de API inválida ou ausente."
        )
    return x_api_key
```

E para usar na rota:

```python
@router.post("/single")
def prever_unitario(
    data: ChurnInput, 
    chave: str = Depends(validar_api_key_simples)
):
    ...
```

> **Por que essa forma é excelente para o aprendizado?**
> Ela desmistifica completamente a segurança: você percebe que autenticação em APIs web começa com uma simples leitura de cabeçalho HTTP e um `if`.
>
> **Quais são as limitações para produção?**
>
> 1. **Não integra com o Swagger UI:** No `/docs`, não aparece o botão visual de autorização; o usuário teria que preencher o header manualmente em cada teste.
> 2. **Vulnerabilidade a *Timing Attacks*:** Comparações diretas de strings com `!=` em Python retornam `False` assim que encontram o primeiro caractere diferente. Um atacante medindo nanosegundos de resposta pode deduzir a chave secreta caractere por caractere.

---

### 7.3 Forma 2: A Abordagem Robusta de Produção (Com `APIKeyHeader` e `Security`)

Para resolver essas limitações em aplicações de produção, o FastAPI fornece o módulo `fastapi.security`, combinando três pilares: **`APIKeyHeader`**, **`Security`** e a biblioteca criptográfica nativa **`secrets`**.

#### 1. Em que formato a chave deve ser salva no `.env`? (Raw, Hash ou Encriptada?)

No arquivo `.env`, a chave é salva em **texto puro (raw string)**, gerada com alta entropia criptográfica:

```dotenv
# .env
API_SECRET_KEY="minha-chave-secreta-de-producao-xyz123"
```

> **Dica Pro:** Para gerar uma chave forte e segura no terminal, execute:
>
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

* **Por que salvar em texto puro (raw) no `.env`?**O arquivo `.env` reside exclusivamente no servidor local ou na infraestrutura de nuvem protegida (Kubernetes Secrets, AWS Secrets Manager, etc.). Ele **nunca** vai para o GitHub. Por ser o próprio cofre da aplicação, o FastAPI precisa do valor original em memória para poder validar as requisições que chegam.
* **Quando usar Hash (como SHA-256 ou Bcrypt)?**
  Apenas quando você cria um sistema SaaS onde **milhares de clientes externos** geram suas próprias chaves e essas chaves ficam salvas em uma tabela de **banco de dados compartilhado** (ex: PostgreSQL). Nesses casos, salva-se o hash no banco para que DBAs ou vazamentos de dumps não revelem as chaves dos clientes. Para APIs internas, microsserviços e Machine Learning onde a chave protege o serviço no `.env`, o padrão de mercado é a **chave raw no .env**.

---

#### 2. Onde é definido o nome do Header? (`APIKeyHeader`)

O nome do cabeçalho HTTP é definido explicitamente no argumento **`name`** da classe `APIKeyHeader`:

```python
from fastapi.security import APIKeyHeader

# O argumento 'name' define exatamente qual cabeçalho HTTP o cliente deve enviar
api_key_scheme = APIKeyHeader(name="X-API-KEY", auto_error=False)
```

* **`name="X-API-KEY"`**: É aqui que você batiza o cabeçalho. O cliente terá que enviar `X-API-KEY: sua-chave`. Poderia ser qualquer outro nome (como `X-Model-Token` ou `Authorization`).
* **`auto_error=False`**:
  * Se for `True` (padrão): o FastAPI interrompe a requisição com uma mensagem genérica em inglês (`403 Not authenticated`) antes de seu código rodar se o header faltar.
  * Se for `False`: o FastAPI apenas tenta extrair o header. Se o cliente esquecer de mandar, a sua função recebe `None`. Isso permite que **você personalize a mensagem de erro** em português e o status code correto (401 ou 403).

---

#### 3. O que diabos é a classe `Security` e como ela funciona?

A classe `Security` do FastAPI é, por baixo dos panos, uma **subclasse direta de `Depends`**:

```python
# Na arquitetura interna do FastAPI:
class Security(Depends):
    ...
```

Ela executa exatamente a mesma injeção de dependência que o `Depends`, **mas com superpoderes adicionais para o Swagger UI e OpenAPI**:

1. **Ativa o Botão Authorize 🔓 no Swagger:** Ao usar `Security(api_key_scheme)`, o FastAPI adiciona os metadados de segurança no `openapi.json`. Isso faz o Swagger UI desenhar o **botão verde Authorize** no topo da página e os **cadeadinhos trancados** ao lado de cada rota protegida.
2. **Suporte a Escopos (`scopes`):** Permite restringir permissões granulares por rota (ex: `Security(validar, scopes=["admin"])`).

> **O que aconteceria se você trocasse `Security` por `Depends`?**
> A verificação da chave ainda funcionaria no terminal com `curl`, **mas o Swagger `/docs` ficaria cego**: não saberia que a rota exige chave, não desenharia o cadeado e não exibiria o botão Authorize.

---

#### 4. Código Completo de `src/app/security.py`

```python
# src/app/security.py
import secrets
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.config import API_SECRET_KEY

# 1. Configura o esquema de segurança e o nome do Header esperado
CABECALHO_API = "X-API-KEY"
api_key_scheme = APIKeyHeader(name=CABECALHO_API, auto_error=False)

# Conjunto de chaves autorizadas (pode vir do .env ou de uma lista)
CHAVES_AUTORIZADAS = {
    API_SECRET_KEY,
    "chave-dashboard-analise-9988",
}

def validar_api_key(chave_recebida: str = Security(api_key_scheme)) -> str:
    """
    Injeção de dependência com proteção contra Timing Attacks e integração com Swagger UI.
    """
    # 1. Verifica se o cliente enviou o header
    if not chave_recebida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: Cabeçalho 'X-API-KEY' ausente."
        )

    # 2. Validação imune a Timing Attack com secrets.compare_digest
    chave_valida = any(
        secrets.compare_digest(chave_recebida, autorizada)
        for autorizada in CHAVES_AUTORIZADAS
    )

    if not chave_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: Chave de API ('X-API-KEY') inválida."
        )

    return chave_recebida
```

> **Por que usar `secrets.compare_digest` em vez de `==`?**
> A comparação comum do Python `chave_recebida == autorizada` é interrompida no **primeiro caractere diferente**. Isso significa que se os primeiros 5 caracteres estiverem certos, ela demora alguns microssegundos a mais para responder do que se o primeiro caractere já estivesse errado. Hackers usam essa diferença de tempo (*Timing Attack*) para adivinhar chaves secretas caractere por caractere.
> A função `secrets.compare_digest` gasta **rigorosamente o mesmo tempo** comparando todas as letras, eliminando essa vulnerabilidade.

---

### 7.4 Como Proteger o Roteador Inteiro

Em vez de adicionar a validação função por função, você pode blindar todas as rotas de predição de uma vez só passando a dependência na criação do `APIRouter`:

```python
# src/app/routers/predict.py
from fastapi import APIRouter, Security
from app.security import validar_api_key

# Todas as rotas deste router passarão a exigir a chave X-API-KEY automaticamente!
router = APIRouter(
    prefix="/predict",
    tags=["Predições"],
    dependencies=[Security(validar_api_key)]
)
```

---

## 8. Orquestração Principal, Ciclo de Vida e Middlewares (`src/app/main.py`)

Com schemas, banco, serviços, routers e segurança prontos, o arquivo `src/app/main.py` atua como o **orquestrador geral**: reúne os routers, configura o ciclo de vida (`lifespan`) e aplica os middlewares:

```python
# src/app/main.py
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.services.ml_service import ml_service
from app.routers import health, predict

# 1. Ciclo de Vida: Carrega o modelo na RAM antes de receber conexões
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 [LIFESPAN] Iniciando servidor e carregando modelo de IA...")
    ml_service.load_model()
    yield
    print("🛑 [LIFESPAN] Finalizando servidor e liberando recursos...")
    ml_service.unload_model()

# 2. Instância do FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan
)

# 3. Middlewares
# CORS: Permite conexão com dashboards (React, Vue, Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Latência: cronometra cada requisição e anexa no cabeçalho de resposta
@app.middleware("http")
async def monitorar_tempo_de_resposta(request: Request, call_next):
    inicio = time.perf_counter()
    resposta = await call_next(request)
    duracao_ms = (time.perf_counter() - inicio) * 1000
    resposta.headers["X-Process-Time-Ms"] = f"{duracao_ms:.2f}"
    return resposta

# 4. Inclusão dos Routers Modularizados
app.include_router(health.router)
app.include_router(predict.router)

# Rota raiz informativa
@app.get("/", tags=["Geral"])
def raiz():
    return {
        "sistema": API_TITLE,
        "docs": "/docs",
        "health": "/health",
        "autenticacao": "Header 'X-API-KEY'"
    }
```

---

## 9. Tratamento Robusto de Exceções e Respostas de Erro

Ao construir APIs, especialmente para servir modelos de Machine Learning, erros vão acontecer: payloads vazios, modelo não carregado ou falhas inesperadas de cálculo. A regra de ouro é **nunca deixar o cliente no escuro com um erro genérico ou stack trace vazando**.

### 9.1 Códigos de Status HTTP Mais Utilizados (`fastapi.status`)

Para responder corretamente ao cliente, utilizamos os status codes semânticos do protocolo HTTP disponíveis no módulo `fastapi.status`:

| Código       | Constante FastAPI                  | Aplicação Prática em APIs de ML                                |
| :------------ | :--------------------------------- | :---------------------------------------------------------------- |
| **200** | `HTTP_200_OK`                    | Predição ou consulta executada com sucesso (`GET`, `POST`). |
| **201** | `HTTP_201_CREATED`               | Recurso criado com sucesso (ex: novo registro no banco).          |
| **400** | `HTTP_400_BAD_REQUEST`           | Payload vazio ou dados inconsistentes enviados pelo cliente.      |
| **401** | `HTTP_401_UNAUTHORIZED`          | Chave de API ausente ou inválida.                                |
| **403** | `HTTP_403_FORBIDDEN`             | Autenticado, mas sem permissão para acessar o recurso.           |
| **404** | `HTTP_404_NOT_FOUND`             | Rota, cliente ou modelo inexistente.                              |
| **422** | `HTTP_422_UNPROCESSABLE_ENTITY`  | Falha automática de validação dos tipos no Pydantic.           |
| **500** | `HTTP_500_INTERNAL_SERVER_ERROR` | Erro inesperado não tratado no código Python (bug).             |
| **503** | `HTTP_503_SERVICE_UNAVAILABLE`   | Modelo de Machine Learning não carregado na memória RAM.        |

---

### 9.2 `HTTPException` Nativa

Para interromper uma requisição imediatamente e retornar um status code com mensagem explicativa:

```python
from fastapi import HTTPException, status

if not dados:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="A lista de clientes não pode estar vazia."
    )
```

---

### 9.3 Handler Global de Exceções (`@app.exception_handler`)

Captura exceções inesperadas disparadas pelo Scikit-Learn ou serviço de IA, devolvendo um JSON limpo sem vazar stack trace no console do cliente:

```python
# Em src/app/main.py
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(RuntimeError)
def tratar_erro_runtime(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=503,
        content={"erro": "Serviço Temporariamente Indisponível", "detalhe": str(exc)}
    )
```

---

## 10. Tarefas em Segundo Plano para MLOps (`BackgroundTasks`)

O `BackgroundTasks` permite disparar ações assíncronas **após** o cliente ter recebido a resposta HTTP da predição. Isso é essencial em Data Science para registrar logs de auditoria e monitorar **Data Drift** sem aumentar o tempo de resposta do endpoint:

```python
from fastapi import APIRouter, BackgroundTasks, Security
from app.schemas.prediction import ChurnInput, ChurnOutput
from app.services.ml_service import ml_service
from app.security import validar_api_key

router = APIRouter(prefix="/predict", tags=["Predições"])

def registrar_auditoria_mlops(dados_cliente: dict, predicao: dict):
    """Grava em disco ou banco para monitorar Drift sem atrasar o cliente."""
    with open("auditoria_mlops.log", "a") as f:
        f.write(f"Cliente: {dados_cliente} -> Saida: {predicao}\n")

@router.post("", response_model=ChurnOutput)
def predizer_com_auditoria(
    cliente: ChurnInput,
    background_tasks: BackgroundTasks,
    chave: str = Security(validar_api_key)
):
    resultado = ml_service.predict_single(cliente)
  
    # O cliente recebe a resposta imediatamente; a gravação roda em background!
    background_tasks.add_task(
        registrar_auditoria_mlops,
        dados_cliente=cliente.model_dump(),
        predicao=resultado.model_dump()
    )
  
    return resultado
```

---

## 11. Containerização com Docker para Produção

Com a estrutura modular em `src/app/`, seu `Dockerfile` fica limpo, leve e direto:

```dockerfile
FROM python:3.11-slim

# Evita criação de arquivos .pyc e buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os artefatos de IA e o código da aplicação
COPY models/ ./models/
COPY src/ ./src/

# Expõe a porta padrão
EXPOSE 8000

# Executa o servidor apontando para o módulo src.app.main:app
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 12. Upload e Processamento de Arquivos em Data Science (`UploadFile` e `File`)

Em aplicações reais de Machine Learning e Ciência de Dados, muitas vezes as requisições não chegam como pequenos payloads JSON. É extremamente comum precisar receber **arquivos brutos**:

* Planilhas **CSV ou Excel** contendo milhares de linhas para inferência em lote (*Batch Inference*);
* Imagens (**PNG, JPEG**) para modelos de Visão Computacional;
* Documentos (**PDF, TXT**) para pipelines de NLP ou RAG;
* Áudios (**WAV, MP3**) para modelos de transcrição (Whisper).

Para receber arquivos, o protocolo HTTP utiliza o formato **`multipart/form-data`** (em vez do tradicional `application/json`).

---

### 12.1 Pré-requisito Obrigatório: `python-multipart`

Para que o FastAPI consiga processar requisições com formulários e uploads de arquivos (`multipart/form-data`), é obrigatório instalar a biblioteca **`python-multipart`**:

```bash
uv add python-multipart
```

> **Se você esquecer de instalar:** Ao chamar um endpoint com upload de arquivos, a aplicação retornará erro `500 Internal Server Error` avisando que a biblioteca `python-multipart` não foi encontrada.

---

### 12.2 `bytes = File(...)` vs `UploadFile` (A Escolha Certa)

O FastAPI oferece duas maneiras de declarar o recebimento de arquivos:

| Abordagem                               | Como declarar                       | O que faz por baixo dos panos                                                                                                            | Quando usar                                                                                                                                                                                         |
| :-------------------------------------- | :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`bytes` bruto**               | `arquivo: bytes = File(...)`      | Carrega o arquivo**100% na memória RAM** como uma sequência de bytes puros.                                                      | **Apenas para arquivos minúsculos** (ícones, pequenos textos < 1MB). **Perigo:** se o usuário enviar um CSV de 2GB, sua API vai estourar a RAM e cair (*Crash por Out of Memory*). |
| **`UploadFile` (Padrão Ouro)** | `arquivo: UploadFile = File(...)` | Utiliza um arquivo em*spool*: grava na memória até ~1MB e, se passar disso, armazena temporariamente em disco de forma transparente. | **Sempre em produção e Data Science**. Suporta streaming assíncrono, não estoura a RAM e fornece metadados do arquivo.                                                                    |

#### Vantagens do `UploadFile`:

* **`arquivo.filename`**: Nome original do arquivo enviado pelo cliente (ex: `clientes_outubro.csv`);
* **`arquivo.content_type`**: Tipo MIME do arquivo (ex: `text/csv`, `application/pdf`, `image/png`);
* **`arquivo.file`**: Um objeto de arquivo Python padrão (*file-like object*), que pode ser passado diretamente para funções como `pandas.read_csv(arquivo.file)` sem precisar gravar no disco antes!
* **Métodos assíncronos úteis**:
  * `conteudo = await arquivo.read()`: Lê os bytes do arquivo;
  * `await arquivo.seek(0)`: Volta o ponteiro de leitura para o início;
  * `await arquivo.close()`: Fecha e libera o arquivo temporário da memória/disco.

---

### 12.3 Caso Real de Data Science: Inferência em Lote via Upload de CSV

Veja como criar um endpoint profissional em `src/app/routers/predict.py` que recebe uma planilha CSV de clientes, valida as colunas e executa a predição com o `pandas` e o `ml_service`:

```python
import io
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Security
from app.services.ml_service import ml_service
from app.security import validar_api_key

router = APIRouter(prefix="/predict", tags=["Predições"])

@router.post("/upload-csv")
async def predizer_por_arquivo_csv(
    arquivo: UploadFile = File(..., description="Planilha CSV contendo as features de clientes"),
    chave: str = Security(validar_api_key)
):
    """
    Recebe um arquivo CSV via multipart/form-data,
    processa diretamente no Pandas e retorna as predições.
    """
    # 1. Validação da extensão do arquivo
    if not arquivo.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo inválido: apenas arquivos com extensão '.csv' são aceitos."
        )

    try:
        # 2. Lê diretamente no Pandas a partir do stream em memória (sem salvar no disco!)
        df = pd.read_csv(arquivo.file)
    
        # 3. Verifica se o DataFrame não está vazio
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo CSV enviado está vazio."
            )
    
        # 4. Converte para lista de dicionários e executa a inferência em lote
        dados_lista = df.to_dict(orient="records")
        predicoes = ml_service.predict_batch(dados_lista)
    
        return {
            "arquivo_processado": arquivo.filename,
            "total_linhas": len(df),
            "predicoes": predicoes
        }
    
    except pd.errors.ParserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falha ao processar o CSV: o arquivo está corrompido ou mal formatado."
        )
    finally:
        # 5. Boa prática obrigatória: sempre fechar o arquivo temporário
        await arquivo.close()
```

---

### 12.4 Upload de Múltiplos Arquivos (`list[UploadFile]`)

Se você precisar que o cliente envie vários arquivos de uma só vez (ex: vários CSVs de filiais diferentes ou um lote de imagens para classificação):

```python
from typing import List
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/upload-multiplos")
async def upload_multiplos_arquivos(
    arquivos: List[UploadFile] = File(..., description="Lista de arquivos para processamento")
):
    resultados = []
  
    for arq in arquivos:
        resultados.append({
            "nome": arq.filename,
            "tipo": arq.content_type
        })
        await arq.close()
    
    return {"total_arquivos": len(arquivos), "detalhes": resultados}
```

No Swagger UI (`/docs`), o campo de upload de múltiplos arquivos permite selecionar vários arquivos simultaneamente usando a tecla `Ctrl` ou `Shift`.

---

### 12.5 Devolvendo um CSV Processado para Download (`StreamingResponse`)

Em fluxos de negócio, é comum o analista subir um CSV com 5.000 clientes e esperar **baixar de volta o mesmo CSV com as colunas de predição adicionadas** (`predicao_classe`, `predicao_probabilidade`, `predicao_status`).

O FastAPI suporta isso perfeitamente com `StreamingResponse`:

```python
import io
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/processar-e-baixar-csv")
async def processar_e_baixar_csv(arquivo: UploadFile = File(...)):
    # 1. Lê o CSV enviado
    df = pd.read_csv(arquivo.file)
  
    # 2. Executa a predição e anexa as colunas no próprio DataFrame
    predicoes = ml_service.predict_batch(df.to_dict(orient="records"))
    df["predicao_classe"] = [p.predicao_classe for p in predicoes]
    df["predicao_probabilidade"] = [p.predicao_probabilidade for p in predicoes]
    df["predicao_status"] = [p.predicao_status for p in predicoes]
  
    # 3. Escreve o DataFrame enriquecido diretamente em um buffer de bytes
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)  # Rebobina o cursor para o StreamingResponse ler desde o início
  
    await arquivo.close()
  
    # 4. Devolve como download direto para o navegador/cliente
    nome_saida = f"predicoes_{arquivo.filename}"
    return StreamingResponse(
        content=buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={nome_saida}"}
    )
```

---

### 12.6 Boas Práticas Essenciais ao Lidar com Arquivos

1. **Sempre use `await arquivo.close()`**: Garante que os arquivos temporários em disco criados pelo Starlette sejam liberados, evitando encher o armazenamento do servidor.
2. **Valide a extensão e o `content_type`**: Nunca confie cegamente no arquivo enviado pelo cliente. Valide tanto o nome (`.csv`, `.xlsx`, `.png`) quanto o MIME type (`arquivo.content_type == "text/csv"`).
3. **Limite o tamanho máximo**: Em produção, configure o proxy reverso (Nginx, Traefik, AWS API Gateway) para limitar uploads gigantes (ex: máximo de 50MB ou 100MB) para evitar ataques de negação de serviço (DoS).

---

## 13. Comandos de Terminal Essenciais (Cheat Sheet)

```bash
# Rodar a API localmente a partir da raiz com hot reload
uv run uvicorn src.app.main:app --reload --port 8000

# Rodar pelo CLI oficial do FastAPI
fastapi dev src/app/main.py

# Construir imagem Docker
docker build -t minha-api-ml:1.0.0 .

# Rodar container expondo a porta 8000
docker run -p 8000:8000 minha-api-ml:1.0.0
```
