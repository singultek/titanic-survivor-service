from sklearn.metrics import accuracy_score
from typing import List
import numpy as np


def test_predict(sample_input_data, titanic_pipeline):
    # Given
    expected_predictions_number = 131

    # When
    result = titanic_pipeline.predict(data=sample_input_data["X_test"])

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, List)
    assert isinstance(predictions[0], int)
    assert result.get("errors") is None
    assert len(predictions) == expected_predictions_number
    accuracy = accuracy_score(predictions, sample_input_data["y_test"])
    assert accuracy > 0.7
