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
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH

# Set the working directory and copy the installation files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Create the virtual environment and install dependencies
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install --only main --no-root

#############
# Deployment image
#############
FROM python:3.11-slim AS prod

# Install curl to run healthcheck
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

# Set the working directory and copy the source code
WORKDIR /app
COPY . /app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "greencompute_frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
