from typing import List, Optional, Tuple
from classification_model.data.data_loader import load_dataset
from pydantic import BaseModel, ValidationError, field_validator, model_validator
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

    @field_validator("age")
    @classmethod
    def age_must_be_logical(cls, v):
        if v is not None and (v < 0.0 or 130.0 < v):
            raise ValueError("Given value is not a possible human age!")
        return v

    @field_validator("sex")
    @classmethod
    def sex_must_be_valid(cls, v):
        if v is not None and v not in ["male", "female"]:
            raise ValueError("Please give a valid sex input from ['male', 'female']!")
        return v

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v):
        if v not in ["Mrs", "Mr", "Miss", "Master"] and v != "Other":
            raise ValueError("Please give a valid title input from ['Mrs', 'Mr', 'Miss', 'Master']!")
        return v

    @model_validator(mode="after")
    def check_sex_title_match(self):
        if self.sex == "male" and self.title != "Other":
            if self.title not in ["Mr", "Master"]:
                raise ValueError("Given sex and title input do not match!")
            return self
        if self.sex == "female" and self.title != "Other":
            if self.title not in ["Mrs", "Miss"]:
                raise ValueError("Given sex and title input do not match!")
            return self


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
