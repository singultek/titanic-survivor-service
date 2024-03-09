import pytest
import os

from typing import Generator
from classification_model.data.data_loader import load_dataset
from classification_model.config.core import init_config
from classification_model import __version__ as _version
from classification_model.model.lr_pipeline import LRPipeline
from sklearn.model_selection import train_test_split

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture()
def config():
    return init_config()


@pytest.fixture()
def sample_input_data(config) -> dict:
    data = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(data[config.lr_model_config.features],
                                                        data[config.lr_model_config.label],
                                                        test_size=config.lr_model_config.test_size,
                                                        random_state=config.lr_model_config.random_state)
    return {"X_test": X_test, "y_test": y_test}


@pytest.fixture()
def titanic_pipeline(config):
    pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    if os.path.isfile(pipeline_file_name):
        titanic_pipeline = LRPipeline().load_pipeline(pipeline_name=pipeline_file_name)
    else:
        titanic_pipeline = LRPipeline().train(is_saved=True)
        titanic_pipeline = titanic_pipeline.load_pipeline(pipeline_name=pipeline_file_name)
    return titanic_pipeline


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
