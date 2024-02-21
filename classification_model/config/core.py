from pydantic import BaseModel, ValidationError
from typing import List, Union
import os
import yaml


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(PACKAGE_ROOT, "config.yml")
TRAINED_MODEL_DIR = os.path.join(PACKAGE_ROOT, "output", "model")
RESULTS_DIR = os.path.join(PACKAGE_ROOT, "output", "results")


class AppConfig(BaseModel):
    """
    Application configuration
    """
    package_name: str
    pipeline_save_file: str


class LRModelConfig(BaseModel):
    """
    Model configuration
    """
    label: str
    features: List[str]
    numerical_variables: List[str]
    categorical_variables: List[str]
    cabin: List[str]
    test_size: float
    C: float
    random_state: int


class Config(BaseModel):
    """
    Main config for package
    """
    app_config: AppConfig
    lr_model_config: LRModelConfig


def _create_and_validate_config(parsed_config):
    try:
        return Config(app_config=AppConfig(**parsed_config),
                      lr_model_config=LRModelConfig(**parsed_config))
    except ValidationError as e:
        print(e)


def _read_config_from_path(path):
    with open(path, "r") as config_file:
        try:
            parsed_config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)
        _config = _create_and_validate_config(parsed_config=parsed_config)
        return _config


def get_config_from_yaml(parsed_config: Union[dict, str] = None) -> Config:
    if parsed_config is None:
        if os.path.isfile(CONFIG_FILE_PATH):
            return _read_config_from_path(path=CONFIG_FILE_PATH)
        else:
            raise OSError(f"Config file is not found at {CONFIG_FILE_PATH}")
    if isinstance(parsed_config, str):
        if os.path.isfile(parsed_config):
            return _read_config_from_path(path=parsed_config)
        else:
            raise OSError(f"Config file is not found at {parsed_config}")
    if isinstance(parsed_config, dict):
        return _create_and_validate_config(parsed_config=parsed_config)


if __name__ == "__main__":
    config_from_yaml = get_config_from_yaml()
    config_from_path = get_config_from_yaml(parsed_config='/Users/sinan/Projects/deploy_ml_titanic/classification_model/config.yml')
    parsed_config = {'package_name': 'classification_model', 'pipeline_name': 'classification_model',
                     'pipeline_save_file': 'trained_classification_model_v', 'label': 'survived',
                     'features': ['age', 'fare', 'sex', 'cabin', 'embarked', 'title'], 'numerical_variables': ['age', 'fare'],
                     'categorical_variables': ['sex', 'cabin', 'embarked', 'title'], 'cabin': ['cabin'], 'test_size': 0.1,
                     'C': 0.0005, 'random_state': 0}
    config_from_dict = get_config_from_yaml(parsed_config=parsed_config)
