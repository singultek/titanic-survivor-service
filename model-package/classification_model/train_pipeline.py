from classification_model.model.lr_pipeline import LRPipeline
from typing import Union


def training_pipeline(saved_pipeline_name: Union[str, None]):
    pipeline = LRPipeline()
    print(f"Initialised pipeline: \n {pipeline.pipeline}")
    pipeline.train(is_saved=True, saved_pipeline_name=saved_pipeline_name)


if __name__ == "__main__":
    training_pipeline(saved_pipeline_name="trained_pipeline.pkl")
