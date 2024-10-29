from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta
from kubernetes.client import models as k8s


volume = k8s.V1Volume(
    name='inference-storage',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='inference-storage')
)

volume_mount = k8s.V1VolumeMount(
    name='inference-storage', 
    mount_path='/tmp/', 
    sub_path=None
)

with DAG(
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval=None,
    dag_id="inference_dag",
) as dag:
    
    load_data = KubernetesPodOperator(
        name="load_data",
        image='yf19001/custom_airflow_inference:latest',
        cmds=["python", "/opt/airflow/inference_pipeline/load_data.py"],
        task_id="load_data",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    load_model = KubernetesPodOperator(
        name="load_model",
        image='yf19001/custom_airflow_inference:latest',
        cmds=["python", "/opt/airflow/inference_pipeline/load_model.py"],
        task_id="load_model",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    run_inference = KubernetesPodOperator(
        name="run_inference",
        image='yf19001/custom_airflow_inference:latest',
        cmds=["python", "/opt/airflow/inference_pipeline/run_inference.py"],
        task_id="run_inference",
        in_cluster=False,
        is_delete_operator_pod=False,
        namespace="airflow",
        startup_timeout_seconds=800,
        image_pull_policy="Always",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    load_data >> load_model >> run_inference