FROM python:3.13-alpine

RUN mkdir -p /app
RUN addgroup --system send-catcher && \
    adduser --system --ingroup send-catcher --no-create-home send-catcher

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
USER send-catcher
ENTRYPOINT [ "python3", "main.py" ]