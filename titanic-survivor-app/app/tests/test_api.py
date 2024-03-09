import numpy as np

from typing import List
from fastapi.testclient import TestClient
from classification_model.model.lr_pipeline import LRPipeline
from sklearn.metrics import accuracy_score


def test_predict(client: TestClient, sample_input_data: dict, titanic_pipeline: LRPipeline):
    # Given
    expected_predictions_number = 131

    payload = {
        # ensure pydantic plays well with np.nan
        "inputs": sample_input_data["X_test"].replace({np.nan: None}).to_dict(orient="records")
    }

    # When
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_response = response.json()
    assert prediction_response["predictions"]
    assert prediction_response["errors"] is None
    assert isinstance(prediction_response["predictions"], List)
    assert isinstance(prediction_response["predictions"][0], int)
    assert len(prediction_response["predictions"]) == expected_predictions_number
    accuracy = accuracy_score(prediction_response["predictions"], sample_input_data["y_test"])
    assert accuracy > 0.7
