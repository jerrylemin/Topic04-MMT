FROM python:3.12-slim
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 labuser
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /app/scripts/docker_entrypoint.sh \
    && mkdir -p /app/data /app/evidence /app/report \
    && chown -R labuser:labuser /app
USER labuser
EXPOSE 5005
HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5005/health', timeout=2)"]
CMD ["/app/scripts/docker_entrypoint.sh"]
