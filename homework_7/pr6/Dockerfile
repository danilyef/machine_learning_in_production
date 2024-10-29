FROM apache/airflow:2.10.0

COPY ./dags/ /opt/airflow/dags
COPY ./inference_pipeline/ /opt/airflow/inference_pipeline
COPY requirements.txt .
RUN pip install -r requirements.txt


