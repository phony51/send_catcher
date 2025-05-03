FROM python:3.13-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN ./setup.sh
ENTRYPOINT [ "python", "main.py" ]