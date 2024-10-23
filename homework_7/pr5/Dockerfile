FROM apache/airflow:2.10.0

COPY ./dags/ /opt/airflow/dags
COPY ./training_pipeline/ /opt/airflow/training_pipeline
COPY requirements.txt .
RUN pip install -r requirements.txt