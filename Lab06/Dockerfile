FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --gid 10001 labuser \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin labuser

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN mkdir -p /app/data /app/evidence /app/report \
    && chown -R labuser:labuser /app/data /app/evidence /app/report

USER 10001:10001
EXPOSE 5006

# Flask listens on the container interface so bridge forwarding works. Compose
# publishes the port only on host loopback, so the lab remains localhost-only.
CMD ["python", "-m", "flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5006", "--no-reload"]
