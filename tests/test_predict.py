from sklearn.metrics import accuracy_score
import numpy as np


def test_predict(sample_input_data, titanic_pipeline):
    # Given
    expected_predictions_number = 131

    # When
    result = titanic_pipeline.predict(data=sample_input_data["X_test"])

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    assert result.get("errors") is None
    assert len(predictions) == expected_predictions_number
    accuracy = accuracy_score(predictions, sample_input_data["y_test"])
    assert accuracy > 0.7
