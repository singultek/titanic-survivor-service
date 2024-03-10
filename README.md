# Deploy a Package: Titanic Survivor App


## Fork the project or Copy repo on local

## Create the Virtual Environment
- `pip install -r model-package/requirements/requirements.txt`
- `pip install -r titanic-surviver-app/requirements/requirements.txt`

## Run Pytest
- Run the tests `pytest model-package/tests`
- Run the tests `pytest titanic-survivor-app/app/tests`
 
## Train Pipeline
- Train the model: `python classification_model/train_pipeline.py`

## Get Predictions
- Predict with new data or test set: `python classification_model/predict.py`
Important to note that, a pipeline should be trained and saved before getting predictions.

## Create a Package Wheel 
- `python setup.py bdist_wheel`

## Run the App
- `cd titanic-survivor-app`
- `uvicorn app.main:app --host 0.0.0.0 --port 8001`
- Then visit `http://localhost:8001/`