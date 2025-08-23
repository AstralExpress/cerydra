FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.1.4
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/code"

# Set working directory
WORKDIR /code

# Copy dependency files first
COPY pyproject.toml poetry.lock* /code/

# Install dependencies (system-wide, no virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy source code
COPY app /code/app
COPY core /code/core

# Default command
CMD ["poetry", "run", "python", "-m", "app"]
