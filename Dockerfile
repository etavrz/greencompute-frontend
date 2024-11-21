#############
# Build (Prepare Environment) image
#############
FROM python:3.11-slim AS builder

# Install curl to install poetry
RUN apt-get update \
    && apt-get install -y \
        curl \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME "/opt/poetry"
ENV PATH "$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory and copy the installation files
WORKDIR /opt/greencompute_frontend
COPY greencompute_frontend ./greencompute_frontend
COPY pyproject.toml poetry.lock README.md ./

# Create the virtual environment and install dependencies
RUN poetry install --only main

#############
# Deployment image
#############
FROM python:3.11-slim AS prod
ENV PATH "/opt/greencompute_frontend/.venv/bin:$PATH"

WORKDIR /opt/greencompute_frontend

# Install curl to run healthcheck
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/greencompute_frontend /opt/greencompute_frontend

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "greencompute_frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
