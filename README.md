# Titanic Survivor Service


## Fork the project or Copy repo on local

## Create the Virtual Environment
- `pip install -r model-package/requirements/requirements.txt`
- `pip install -r titanic-surviver-app/requirements/requirements.txt`
- `pip install -r titanic-surviver-app/requirements/titanic_classification_model-1.0.0-py3-none-any.whl`

## Run PyTests
- Run the tests `pytest model-package/tests`
- Run the tests `pytest titanic-survivor-app/app/tests`
 
## Train Pipeline
- Train the model: `python classification_model/train_pipeline.py`

## Get Predictions
- Predict with new data or test set: `python classification_model/predict.py`
Important to note that, a pipeline should be trained and saved before getting predictions.

## Create a Model Package Wheel 
If one wants to change some parts of the project and use modified model package, 
the steps above can be followed: 
- `cd model-package`
- Change the version on [VERSION](model-package/classification_model/VERSION) file 
- Create new distribution wheel with `python setup.py bdist_wheel`
- Update the version of the wheel in [app requirements](titanic-survivor-app/requirements/requirements.txt)
- Go back to root directory with `cd ..`
- To avoid getting wheel from cache(This step can be skipped if it is certain that there isn't cached wheel for the 
- new version of package), uninstall the package with `pip uninstall titanic-classification-model`
- Install the requirements again with `pip install -r titanic-surviver-app/requirements/requirements.txt`

## Run the App
- `cd titanic-survivor-app`
- `uvicorn app.main:app --host 0.0.0.0 --port 8001`
- Then visit `http://localhost:8001/`

## Containerize with Docker
- `docker build -t titanic-survivor-service:1.0.0 .`
- `docker run -it -p 8001:8001/tcp --name container-titanic-survivor-service titanic-survivor-service:1.0.0`
- Then visit `http://localhost:8001/`



