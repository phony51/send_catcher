FROM python:3.13-alpine

RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    libffi-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 send-catcher && \
    mkdir -p /app && \
    chown send-catcher:send-catcher /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

USER send-catcher

ENTRYPOINT [ "python3", "main.py" ]