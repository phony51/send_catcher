FROM python:3.13-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN chmod -R 777 /app
RUN ./setup.sh
ENTRYPOINT [ "python", "main.py" ]