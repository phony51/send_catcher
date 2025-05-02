FROM python:3.13-alpine

RUN mkdir -p /app &&

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

USER send-catcher

ENTRYPOINT [ "python3", "main.py" ]