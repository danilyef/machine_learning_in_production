from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta
from kubernetes.client import models as k8s


volume = k8s.V1Volume(
    name='training-storage',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='training-storage')
)

volume_mount = k8s.V1VolumeMount(
    name='training-storage', 
    mount_path='/tmp/', 
    sub_path=None
)

with DAG(
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval=None,
    dag_id="training_dag",
) as dag:
    
    load_data = KubernetesPodOperator(
        name="load_data",
        image='yf19001/custom_airflow:latest',
        cmds=["python", "/opt/airflow/training_pipeline/load_data.py"],
        task_id="load_data",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    train_model = KubernetesPodOperator(
        name="train_model",
        image='yf19001/custom_airflow:latest',
        cmds=["python", "/opt/airflow/training_pipeline/train.py"],
        task_id="train_model",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    upload_model = KubernetesPodOperator(
        name="upload_model",
        image='yf19001/custom_airflow:latest',
        cmds=["python", "/opt/airflow/training_pipeline/save_model.py"],
        task_id="upload_model",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    load_data >> train_model >> upload_model
