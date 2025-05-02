FROM python:3.13-alpine

RUN mkdir -p /app
USER send-catcher
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py" ]