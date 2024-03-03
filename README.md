# Deploy a Package: Titanic Classification Model


## Fork the project or Copy repo on local

## Create the Virtual Environment
- `pip install -r model-package/requirements/requirements.txt`
- `pip install -r titanic-surviver-app/requirements/requirements.txt`

## Run Pytest
- Run the tests `pytest tests`
 
## Train Pipeline
- Train the model: `python classification_model/train_pipeline.py`

## Get Predictions
- Predict with new data or test set: `python classification_model/predict.py`
Important to note that, a pipeline should be trained and saved before getting predictions.

## Create a Package Wheel 
- `python setup.py bdist_wheel`