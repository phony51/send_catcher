FROM python:3.13-alpine

RUN mkdir -p /app
RUN addgroup --system send-catcher
RUN adduser --system --ingroup send-catcher --no-create-home send-catcher
RUN chown -R send-catcher:send-catcher /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=send-catcher:send-catcher . .
USER send-catcher
ENTRYPOINT [ "python3", "main.py" ]