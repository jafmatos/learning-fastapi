from pandas import DataFrame
import pandas
from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile


async def get_upload_csv_dataframe(upload_file: UploadFile) -> DataFrame:
    if not upload_file.content_type == "text/csv":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo deve ser do tipo CSV",
        )

    try:
        dataframe = pandas.read_csv(upload_file.file)

        if dataframe.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo CSV está vazio",
            )

        yield dataframe
    except (pandas.errors.ParserError, pandas.errors.EmptyDataError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo CSV está vazio, corrompido ou mal formatado",
        )

    finally:
        await upload_file.close()
