import gspread
import pandas as pd
from src.config import GCP_KEY_PATH

def get_sheet_data(spreadsheet_id, sheet_name=None):
    """Fungsi sakti buat narik data GSheet jadi Pandas DataFrame"""
    # Login pake kunci JSON yang sama buat BigQuery
    gc = gspread.service_account(filename=GCP_KEY_PATH)
    
    # Buka spreadsheet berdasarkan ID
    sh = gc.open_by_key(spreadsheet_id)
    
    # Pilih sheet (default sheet pertama kalau gak disebut)
    worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
    
    # Ambil semua data dan jadikan DataFrame
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def fetch_external_dimensions():
    print("🔍 Fetching dimensions from Google Sheets...")
    
    # ID GSheet yang lo kasih tadi
    PRODUCT_SHEET_ID = "1K8kdcsgXif88DfwXU12jYelEQpZZSt0lTZwRy8HwCj8"
    DATE_SHEET_ID = "1zqsoAlROIAfy6RL7tMTGjuSZGAuGzqUDwWGFGUZXPT0"
    
    # Tarik datanya
    df_product = get_sheet_data(PRODUCT_SHEET_ID)
    df_date = get_sheet_data(DATE_SHEET_ID)
    
    print(f"✅ Sync Success: {len(df_product)} products & {len(df_date)} dates ready.")
    return df_date, df_product