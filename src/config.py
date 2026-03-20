import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GCP_KEY_PATH = str(BASE_DIR / "keys" / "service-account.json")
PROJECT_ID = "dck-retail-project"  # Ganti ID lo
DATASET_ID = "retail_data"

# Otomatis set environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_KEY_PATH