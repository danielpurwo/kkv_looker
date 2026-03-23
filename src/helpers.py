import gspread
import pandas as pd
from src.config import *

def get_sheet_data(spreadsheet_id, sheet_name=None):
    gc = gspread.service_account(filename=GCP_KEY_PATH)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
    data = worksheet.get_all_records()
    
    df = pd.DataFrame(data)
    
    df.columns = [str(col).strip().replace('\xa0', ' ') for col in df.columns]
    
    return df

def get_drive_csv(file_id):
    # Gunakan jalur 'uc?export=download' untuk file CSV mentah
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    print(f"📥 Downloading CSV from Drive (ID: {file_id})...")
    return pd.read_csv(url)

def fetch_all_external_data():
    """Orchestrator: Ambil SEMUA dimensi dari luar"""
    print("🧹 Starting Hybrid Data Ingestion from GSheet & GDrive...")
    
    # 1. Tarik dari GSheet (via gspread)
    df_date = get_sheet_data(SHEET_ID_DATE)
    df_product = get_sheet_data(SHEET_ID_PRODUCT)
    df_customer = get_sheet_data(SHEET_ID_CUSTOMER)
    df_promo = get_sheet_data(SHEET_ID_PROMO)
    df_store = get_sheet_data(SHEET_ID_STORE)
    
    # 2. Tarik dari GDrive (Direct CSV)
    df_channel_raw = get_drive_csv(CSV_ID_CHANNEL)
    df_channel_type_raw = get_drive_csv(CSV_ID_CHANNEL_TYPE)
    
    print(f"✅ Success: 7 sources fetched (including Store data).")
    
    return {
        "date": df_date,
        "product": df_product,
        "customer": df_customer,
        "promo": df_promo,
        "store": df_store,
        "channel_raw": df_channel_raw,
        "type_raw": df_channel_type_raw
    }