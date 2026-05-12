FROM python:3.11-slim
WORKDIR /app
RUN pip install pandas boto3 duckdb
COPY etl_worker.py .
RUN mkdir -p /app/data
CMD ["python", "-u", "etl_worker.py"]
