FROM python:3.11

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-titanic-user

WORKDIR /opt/titanic-survivor-app

ARG PIP_EXTRA_INDEX_URL

# Install requirements, including from Gemfury
ADD ./titanic-survivor-app /opt/titanic-survivor-app/
RUN pip install --upgrade pip
RUN pip install -r /opt/titanic-survivor-app/requirements.txt

RUN chmod +x /opt/titanic-survivor-app/run.sh
RUN chown -R ml-titanic-user:ml-titanic-user ./

USER ml-titanic-user

EXPOSE 8001

CMD ["bash", "./run.sh"]
