from airflow import DAG
from airflow.operators import PythonOperator
from SelectLatLong import Select50LatLongs
from HitModel import CallAPIHitModel
from datetime import datetime
from SaveData import WriteMetadata


with DAG(dag_id="Sevir_Result_Cache",
         start_date=datetime(2022, 3, 30),
         schedule_interval="@hourly",
         catchup=False) as dag:

    task1 = PythonOperator(
        task_id="Select50LatLongs",
        python_callable=Select50LatLongs)

    task2 = PythonOperator(
        task_id="CallAPIHitModel",
        python_callable=CallAPIHitModel)

    task3 = PythonOperator(
        task_id="WriteMetadata",
        python_callable=WriteMetadata)

task1 >> task2
task2 >> task3