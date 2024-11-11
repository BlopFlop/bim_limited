FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y netcat-traditional

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x dockerentrypoint.sh

ENTRYPOINT ["./dockerentrypoint.sh"]
