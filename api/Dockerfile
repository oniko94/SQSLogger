FROM python:3.12-alpine
WORKDIR /api
# Install the system dependencies
RUN pip3 install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
# Install the project dependencies in a separate cached layer
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-root --no-interaction --no-cache --only=main
# The most frequently changed layer (source code/migrations)
COPY alembic.ini alembic.ini
COPY migrations migrations
COPY run.sh run.sh
COPY api api
RUN poetry install --only-root --no-interaction --no-cache
# Execute the script that applies the migration and starts the application
CMD [ "./run.sh"]
