# Stage 1: Export requirements
FROM python:3.10.10-slim-buster AS poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt \
    --output requirements.txt \
    --with-credentials \
    --without-hashes


# Stage 2: Build 
FROM python:3.10.10-slim-buster as build

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt update && apt install -y \
    build-essential \
    libc-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
RUN pip install --upgrade pip
COPY --from=poetry /app/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn

COPY .env .env

ADD alembic alembic
COPY alembic.ini .

COPY pyproject.toml .

ADD event_manager event_manager

# Stage 3: Final image
FROM python:3.10.10-slim-buster as output

RUN apt-get update && \
    apt-get -y install curl wget

WORKDIR /app

RUN useradd -m worker \
    && chown -R worker:worker /app

USER worker

ENV PYTHONPATH=/app \
    HOME=/home/worker \
    PATH="/home/worker/.local/bin:${PATH}"

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /app /app
# COPY --from=build /etc/passwd /etc/passwd

EXPOSE 8000

# Run migrations and start the application
CMD ["bash", "-c", "python -m alembic upgrade head && python -m uvicorn event_manager.main:app --host 0.0.0.0 --port 8001"]
