import pandas as pd
import numpy as np

from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from classification_model.predict import get_predictions

from app import schemas, model_version, api_version
from app.config import Settings
from app.log_config import app_config


logger = app_config.get_logger()
settings = Settings()
api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Health Check of the API
    """
    logger.info("Health Check.")
    health_check = schemas.Health(
        name=settings.PROJECT_NAME, api_version=api_version, model=model_version
    )

    return health_check.dict()


@api_router.post("/predict", response_model=schemas.PredictionResponse, status_code=200)
async def predict(input_data: schemas.MultipleTitanicDataInputs) -> Any:
    """
    Make survivor predictions from titanic crash with the titanic-classification-model
    """
    logger.info(f"Getting the input data...")
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = get_predictions(data=input_df.replace({np.nan: None}), saved_pipeline_name=settings.TRAINED_MODEL_NAME)

    # TODO: Investigate ValidationError handling more
    if results["errors"] is not None:
        logger.warning(f"Prediction error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=results["errors"])

    logger.info(f"Prediction is finished: {results.get('predictions')}")

    return results
