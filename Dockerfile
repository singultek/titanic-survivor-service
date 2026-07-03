FROM python:3.11.1 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

WORKDIR /code

# Copy workspace manifests and lockfile first for better layer caching
COPY pyproject.toml uv.lock .python-version ./
COPY model-package/ model-package/
COPY titanic-survivor-app/ titanic-survivor-app/

# --frozen fails the build if uv.lock is out of sync with pyproject.toml
# --no-dev excludes pytest and other dev-only tools from the runtime image
# --no-editable installs the workspace-local model package as a self-contained
# package rather than a path reference, since only titanic-survivor-app/ (not
# model-package/) is copied into the final stage below
RUN uv sync --frozen --no-dev --no-editable --package titanic-survivor-app

# Train the pipeline and save it into the installed classification_model package
# (under .venv/.../classification_model/output/model/), since the trained .pkl is
# gitignored/dockerignored as a build artifact and is never copied in from the host.
ENV PATH="/code/.venv/bin:$PATH"
RUN python -m classification_model.train_pipeline

FROM python:3.11.1

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-titanic-user

WORKDIR /code

COPY --from=builder /code/.venv /code/.venv
COPY --from=builder /code/titanic-survivor-app /code/titanic-survivor-app

ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code/titanic-survivor-app

RUN chmod +x run.sh
RUN chown -R ml-titanic-user:ml-titanic-user /code

USER ml-titanic-user

# Make port 8001 available for links and/or publish
EXPOSE 8001

CMD ["bash", "./run.sh"]
