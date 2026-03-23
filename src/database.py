# src/database.py
import pandas_gbq
from src.config import PROJECT_ID, DATASET_ID, GCP_KEY_PATH

def push_to_bigquery(df, table_name):
    """
    Mengirim DataFrame ke BigQuery.
    Menggunakan mode 'replace' biar pas Trial & Error data lo selalu bersih.
    """
    table_id = f"{DATASET_ID}.{table_name}"
    
    print(f"📡 Ingesting {table_name} ({len(df)} rows) to BigQuery...")
    
    try:
        pandas_gbq.to_gbq(
            df,
            destination_table=table_id,
            project_id=PROJECT_ID,
            if_exists='replace', # Menghapus data lama, ganti baru (Clean!)
            progress_bar=True
        )
        print(f"✅ {table_name} is LIVE.")
    except Exception as e:
        print(f"❌ Failed to push {table_name}: {e}")