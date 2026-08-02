FROM mirror.gcr.io/library/python:3.12.11-slim@sha256:47ae396f09c1303b8653019811a8498470603d7ffefc29cb07c88f1f8cb3d19f

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements.lock ./
RUN pip install --no-cache-dir --requirement requirements.lock

COPY pyproject.toml README.md main.py ./
COPY src ./src
COPY config ./config
RUN pip install --no-cache-dir --no-deps .

USER 65532:65532

CMD ["sh", "-c", "exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 60 --access-logfile - --error-logfile - main:app"]
