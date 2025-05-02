FROM python:3.13-slim

RUN mkdir -p /app/{sessions,logs} && \
    chmod -R 755 /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py" ]