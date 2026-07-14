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

# app.py intentionally binds 127.0.0.1 inside the container. A normal bridge
# port publish cannot reach a process bound only to the container loopback.
# The compose file keeps the required host-side 127.0.0.1 publish and documents
# this limitation instead of weakening the lab by binding the app to 0.0.0.0.
CMD ["python", "app.py"]
