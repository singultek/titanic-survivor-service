# Titanic Survivor Service

### The Goal of the Project

The Titanic Survivor Service is a Python-based 
application designed to provide information about 
passengers who survived the Titanic disaster. The 
project aims to offer a simple API for predicting the 
survivors with the help of provided input data based on 
various information about the passenger such as age, sex, 
title, cabin, fare, and embankment status.

### Which Technologies I Used

**Python**: De facto standard programming language of the machine learning applications.

**FastAPI**: Utilized for building the API due to its high performance, easy-to-use 
interface, and automatic interactive documentation generation.

**pytest**: Employed for testing purposes to ensure the reliability and correctness of 
the codebase.

**Docker**: Utilized for containerization, facilitating easy deployment and reproducibility 
across different environments.

**Table of Contents**
* [How to Setup the Environment](#how-to-setup-the-environment)
* [How to Run Tests](#how-to-run-tests)
* [How to Use the Service](#how-to-use-the-service)
* [About Author](#about-author)

## How to Setup the Environment

### Fork the project or Copy repo on local
- Forking the project: If you intend to contribute to the project or modify it for 
your own purposes, it's recommended to fork the repository first. This creates a 
copy of the repository under your GitHub account, allowing you to freely make changes
without affecting the original project. You can fork the repository by clicking the 
"Fork" button on the GitHub repository page.
- Copy the repository locally: If you just want to use the project without contributing 
or modifying it, you can simply clone the repository to your local machine using the 
following command:
  - `git clone https://github.com/singultek/titanic-survivor-service.git`

### Set Up the Environment with uv
This project uses [uv](https://docs.astral.sh/uv/) to manage the Python version and
dependencies for both `model-package` and `titanic-survivor-app` together, as a single
workspace.

1. Install uv (see the [official install guide](https://docs.astral.sh/uv/getting-started/installation/)):

`curl -LsSf https://astral.sh/uv/install.sh | sh`

2. From the repository root, sync the workspace. This reads `.python-version`,
installs Python 3.11.1 automatically if it isn't already available, creates a `.venv`,
and installs both packages plus their exact locked dependency versions from `uv.lock`:

`uv sync`

3. (Optional) Activate the environment directly if you want plain `python`/`pytest`
commands to work without prefixing them with `uv run`:
   * On Windows: `.venv\Scripts\activate`
   * On macOS and Linux: `source .venv/bin/activate`

Once `uv sync` has completed, the environment setup is complete, and you can proceed
to run tests, use the service, or make modifications to the project as needed.

### Updating the Model Package
Because `model-package` and `titanic-survivor-app` are members of the same uv
workspace, `titanic-survivor-app` always depends on the local, in-repo version of
`model-package` — there's no wheel to manually build or copy for local development.

If one wants to change the model package and use the modified version:
- Make your changes under `model-package/`
- Bump the version in [VERSION](model-package/classification_model/VERSION)
- From the repo root, run `uv sync` again to pick up the change

If you need to produce a standalone wheel for distribution outside this workspace
(e.g. publishing to an internal package index), run:
`uv build --package model-package`

The wheel will be written to `model-package/dist/`.


## How to Run Tests

Running tests ensures that the code behaves as expected and helps maintain its 
reliability and correctness. In this project, tests are organized into different 
directories corresponding to different components of the application.

1. Model Package Tests
- `uv run pytest model-package/tests`
2. Titanic Survivor App Tests
- `uv run pytest titanic-survivor-app/app/tests`

Running these tests will execute the test cases defined in the respective directories,
ensuring that the model package and the application components work as expected. 
If any test fails, pytest will provide detailed information about the failure, helping
identify and fix any issues in the codebase.

It's good practice to run tests regularly, especially after making changes to the code,
to catch and address any regressions or bugs early in the development process.

## How to Use the Service

The Titanic Survivor Service provides a simple API to access information about 
passengers who survived the Titanic disaster. You can interact with the service by
sending HTTP requests to its endpoints using tools like cURL, Postman, or by making 
HTTP requests from your application.

### Train Pipeline
Before using the service, you may need to train the machine learning model pipeline to 
ensure accurate predictions. Follow the below code snippet to train the pipeline:
- Train the model: `python model-package/classification_model/train_pipeline.py`

### Get Predictions
Once the model pipeline is trained, you can use the service to make predictions on new 
data or test sets. Follow these steps to get predictions:

- Predict with new data or test set: `python model-package/classification_model/predict.py`

**Important to note that**, a pipeline should be trained and saved before getting predictions. 
Inside the model package, there are some implementations to throw an error, or automatically
train a baseline pipeline when the user tries to make predictions without having 
a trained pipeline. Nonetheless, it is advised to manually train a pipeline before 
making predictions.


### Run the App
To interact with the service via its API endpoints, follow these steps to run the application:
1. Navigate to the Titanic Survivor App Directory: 
- `cd titanic-survivor-app`
2. Run the  FastAPI application using the uvicorn command:
- `uv run uvicorn app.main:app --host 0.0.0.0 --port 8001`  OR
3. Directly run the app with prepared script:
- `uv run bash ./run.sh`
- Then visit `http://localhost:8001/`

(If you activated the `.venv` per the setup step above, the plain `uvicorn ...` /
`sh ./run.sh` commands work too, without the `uv run` prefix.)

### Containerize with Docker
If you prefer to containerize the service for easy deployment, you can follow 
these steps:

1. Build the Docker Image: 
- `docker build --no-cache -t titanic-survivor-service:1.1.0 -f Dockerfile .`
    - --no-cache flag is used to have clean build, otherwise some minor changes may 
  not be executed in order to fasten the build process.
    - -t flag is useful to tag the image. In this example, out tag is same as the 
  release. If you want to create an image instance directly on your Docker Hub, you
  can modify the command as `docker build --no-cache -t ${YOUR_DOCKER_HUB_USERNAME}/
  titanic-survivor-service:1.1.0 -f Dockerfile .`. 
    - -f flag will help you to point out the docker file name you want to build from. 
  "Dockerfile" is the default value. Docker file name is followed by "." path indicator.
2. Run the Docker Container:
- `docker run -it -p 8001:8001/tcp --name container-titanic-survivor-service titanic-survivor-service:1.1.0`
  - -it flag uses the interactive terminal. 
  - -p flag is used for linking the containers port to our local machines port.
  - --name flag instantiate the container with the given name, otherwise it would be 
  assigned randomly.
  - If we build the image directly on Docker Hub, we need to give image from there. In
  this case, image name would be `${YOUR_DOCKER_HUB_USERNAME}/titanic-survivor-service:1.1.0`
3. The service will be accessible at`http://localhost:8001/`


## About Author

I'm Sinan Gültekin, a Machine Learning Engineer based in Italy.

For any suggestions or questions, you can contact me via <singultek@gmail.com>

Distributed under the MIT License. _See ``LICENSE`` for more information._
