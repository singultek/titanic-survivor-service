from classification_model.model.lr_pipeline import LRPipeline
from classification_model.config.core import TRAINED_MODEL_DIR
from typing import Union
import pandas as pd
import os.path


def get_predictions(data: Union[pd.DataFrame, dict], saved_pipeline_name: str):
    response = {}
    try:
        pipeline = LRPipeline().load_pipeline(pipeline_name=saved_pipeline_name)
        response = pipeline.predict(data=data)
        return response
    except FileNotFoundError:
        response["errors"] = (f"Trained pipeline named as {saved_pipeline_name} is not found "
                              f"on {os.path.join(TRAINED_MODEL_DIR, saved_pipeline_name)}. "
                              f"Please be sure that you trained a pipeline before making predictions!")
        return response


if __name__ == "__main__":
    from classification_model.data.data_loader import load_dataset
    from classification_model.config.core import init_config
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    config = init_config()
    titanic_data = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(titanic_data[config.lr_model_config.features],
                                                        titanic_data[config.lr_model_config.label],
                                                        test_size=config.lr_model_config.test_size,
                                                        random_state=config.lr_model_config.random_state)
    titanic_predictions = get_predictions(data=X_test, saved_pipeline_name="trained_classification_model_v0.0.1.pkl")
    accuracy = accuracy_score(titanic_predictions, y_test)
    print(f"Accuracy of Titanic Classification Pipeline: {accuracy}")
