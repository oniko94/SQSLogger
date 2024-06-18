FROM python:3.12-alpine AS server_base
WORKDIR /api
# Install the system dependencies
RUN pip3 install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
# Install the project dependencies in a separate cached layer
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-root --no-interaction --no-cache --only=main
# The most frequently changed layer (source code/migrations)
#COPY __init__.py __init__.py
COPY alembic.ini alembic.ini
COPY core core

# Isolated api endpoints image
FROM server_base AS server_api
COPY .bin/run.sh run.sh
COPY api api
RUN poetry install --only-root --no-interaction --no-cache
# Install the migrations and run the server
CMD ["./run.sh"]

# Isolated DB worker image
FROM server_base as server_worker
COPY workers api
RUN poetry install --only-root --no-interaction --no-cache
CMD ["python", "-m", "api"]
