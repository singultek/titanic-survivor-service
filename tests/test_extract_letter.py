from classification_model.config.core import init_config
from classification_model.features.extract_letter import ExtractLetterTransformer


def test_extract_letter_transformer(sample_input_data, config):
    # Given
    transformer = ExtractLetterTransformer(features=config.lr_model_config.cabin)
    assert sample_input_data["X_test"]["cabin"].iat[6] == "E12"

    # When
    subject = transformer.fit_transform(sample_input_data["X_test"])

    # Then
    assert subject["cabin"].iat[6] == "E"
