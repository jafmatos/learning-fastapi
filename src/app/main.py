from fastapi import status
from fastapi.responses import JSONResponse
import time
from fastapi import Request
from app.services.ml_service import ml_service
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.routers.predict import router as predict_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_service.load_model()

    yield

    ml_service.unload_model()


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def add_response_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_in_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{duration_in_ms:.2f}"

    return response


@app.exception_handler(RuntimeError)
def handle_runtime_error(request: Request, exception: RuntimeError):
    print(exception.with_traceback(None))

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor"},
    )


@app.exception_handler(Exception)
def handle_exception(request: Request, exception: Exception):
    print(exception.with_traceback(None))
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor"},
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
def handle_not_found_error(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Recurso não encontrado"},
    )

app.include_router(predict_router)
