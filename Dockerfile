FROM python:3.13-alpine

RUN useradd -m -u 1000 send-catcher && \
    mkdir -p /app && \
    chown send-catcher:send-catcher /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

USER send-catcher

ENTRYPOINT [ "python3", "main.py" ]