FROM python:3.11.1

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-titanic-user

WORKDIR /code/titanic-survivor-app

# Copy our titanic survivor app from the current folder to /code inside the container
ADD ./titanic-survivor-app /code/titanic-survivor-app/

# Install our requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/titanic-survivor-app/requirements/requirements.txt
RUN pip install /code/titanic-survivor-app/requirements/titanic_classification_model-1.1.0-py3-none-any.whl


RUN chmod +x /code/titanic-survivor-app/run.sh
RUN chown -R ml-titanic-user:ml-titanic-user ./

USER ml-titanic-user

# Make port 8001 available for links and/or publish
EXPOSE 8001

CMD ["bash", "./run.sh"]
#CMD ["uvicorn", "app.main:app", "--host=0.0.0.0" , "--reload" , "--port", "8001"]