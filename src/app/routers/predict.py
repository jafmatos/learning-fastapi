from fastapi import Security
from app.security import validate_api_key
from fastapi import APIRouter
from app.schemas.prediction import ChurnOutput
from fastapi import Depends
from app.schemas.prediction import ChurnInput
from app.services.ml_service import get_ml_service
from app.services.ml_service import MLService

router = APIRouter(prefix="/predict", dependencies=[Security(validate_api_key)], tags=["Predições"])


@router.post("/single", response_model=ChurnOutput)
def predict_single(
    data: ChurnInput,
    ml_service: MLService = Depends(get_ml_service),
):
    return ml_service.predict_single(data)


@router.post("/batch", response_model=list[ChurnOutput])
def predict_batch(
    data: list[ChurnInput],
    ml_service: MLService = Depends(get_ml_service),
):
    return ml_service.predict_batch(data)
