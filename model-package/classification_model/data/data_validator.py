from typing import List, Optional, Tuple
from classification_model.data.data_loader import load_dataset
from pydantic import BaseModel, ValidationError
import numpy as np
import pandas as pd


def validate_data(input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:

    loaded_preprocessed_dataframe = load_dataset(dataframe=input_data)
    errors = None

    try:
        MultipleTitanicDataInputs(inputs=loaded_preprocessed_dataframe.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.json()

    return loaded_preprocessed_dataframe, errors


class TitanicDataInputSchema(BaseModel):
    sex: Optional[object]
    age: Optional[float]
    fare: Optional[float]
    cabin: Optional[object]
    embarked: Optional[object]
    title: Optional[object]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
