FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc gdb make binutils socat \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 labuser

WORKDIR /lab
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
RUN make all \
    && mkdir -p evidence report \
    && chown -R labuser:labuser /lab

USER labuser
EXPOSE 5002
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5002/health', timeout=2).read()" || exit 1
CMD ["sh", "-c", "python app.py & app=$!; ip=$(hostname -i); ip=${ip%% *}; socat TCP-LISTEN:5002,bind=$ip,reuseaddr,fork TCP:127.0.0.1:5002 & proxy=$!; trap 'kill $app $proxy 2>/dev/null' TERM INT; wait $app; status=$?; kill $proxy 2>/dev/null || true; exit $status"]
