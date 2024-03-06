from pydantic import BaseModel
from typing import Optional, Any, List
from classification_model.data.data_validator import TitanicDataInputSchema


class PredictionResponse(BaseModel):
    predictions: Optional[List]
    version: str
    errors: Optional[Any]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]

    model_config = {
        "json_schema_extra": {
            "example": {
                "inputs": [
                    {
                        "sex": "male",
                        "age": 25.0,
                        "fare": 170.0,
                        "cabin": "B5",
                        "embarked": "S",
                        "title": "Mr"
                    }
                ]
            }
        }
    }
