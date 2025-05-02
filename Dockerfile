FROM python:3.13-alpine

RUN mkdir -p /app
RUN addgroup --system send-catcher && \
    adduser --system --ingroup send-catcher --no-create-home send-catcher
USER send-catcher
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py" ]