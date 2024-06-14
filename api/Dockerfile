FROM python:3.12-alpine AS api-base
WORKDIR /api
COPY ./pyproject.toml /api
RUN pip3 install --no-cache-dir --upgrade poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
ENTRYPOINT  ["/bin/sh", "run.sh"]
