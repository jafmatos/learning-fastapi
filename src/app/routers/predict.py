from fastapi.responses import StreamingResponse
import io
from pandas import DataFrame
from app.dependencies.get_upload_csv_dataframe import get_upload_csv_dataframe
from fastapi import UploadFile
from fastapi import Security
from app.security import validate_api_key
from fastapi import APIRouter
from app.schemas.prediction import ChurnOutput
from fastapi import Depends
from app.schemas.prediction import ChurnInput
from app.services.ml_service import get_ml_service
from app.services.ml_service import MLService

router = APIRouter(
    prefix="/predict", dependencies=[Security(validate_api_key)], tags=["Predições"]
)


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


@router.post("/csv")
def predict_csv(
    upload_file: UploadFile,
    ml_service: MLService = Depends(get_ml_service),
    input_dataframe: DataFrame = Depends(get_upload_csv_dataframe),
):
    output_dataframe = ml_service.predict_dataframe(input_dataframe)

    buffer = io.BytesIO()
    output_dataframe.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)

    output_filename = f"predicoes_{upload_file.filename}"

    return StreamingResponse(
        content=buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={output_filename}"},
    )
