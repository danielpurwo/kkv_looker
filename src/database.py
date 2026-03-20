from google.cloud import bigquery
from src.config import PROJECT_ID, DATASET_ID

client = bigquery.Client()

def push_to_bigquery(df, table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    
    print(f"📡 Ingesting {table_name} ({len(df)} rows)...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"✅ {table_name} is LIVE.")