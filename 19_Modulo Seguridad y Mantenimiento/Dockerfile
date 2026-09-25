# BUILDER
FROM python:3.12-slim AS builder
WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.0

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
COPY app ./app

RUN poetry build

# RUNNER
FROM python:3.12-slim AS runner

# 1. Usuario sin privilegios
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2. Copiamos el Wheel asignándole el dueño appuser
COPY --chown=appuser:appgroup --from=builder /build/dist/*.whl ./

# 3. Instalamos el Wheel
RUN pip install --no-cache-dir ./*.whl

# 4. Le decimos a Docker que ejecute con el user sin root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
