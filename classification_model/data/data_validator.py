from typing import List, Optional, Tuple, Union
from classification_model.config.core import init_config
from classification_model.data.data_loader import load_dataset
from pydantic import BaseModel, ValidationError
import numpy as np
import pandas as pd


def validate_data(input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:

    loaded_preprocessed_dataframe = load_dataset(dataframe=input_data)
    validated_data = loaded_preprocessed_dataframe[init_config().lr_model_config.features].copy()
    errors = None

    try:
        MultipleTitanicDataInputs(inputs=validated_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class TitanicDataInputSchema(BaseModel):
    pclass: Optional[int]
    name: Optional[str]
    sex: Optional[str]
    age: Optional[int]
    sibsp: Optional[int]
    parch: Optional[int]
    ticket: Optional[int]
    fare: Optional[float]
    cabin: Optional[str]
    embarked: Optional[str]
    boat: Optional[Union[str, int]]
    body: Optional[int]
    homedest: Optional[str]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
