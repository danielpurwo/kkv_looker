import pandas as pd
from src.helpers import get_sheet_data # Pake fungsi gspread yang kita bahas tadi
from src.config import *

def fetch_and_join_dimensions():
    print("🧹 Fetching Dimensions from Hybrid Sources...")

    # 1. Fetch Google Sheets (Customer Segment)
    df_customer = get_sheet_data(SHEET_ID_CUSTOMER)

    # 2. Fetch Google Sheets (Promo Dependency)
    df_promo = get_sheet_data(SHEET_ID_PROMO)

    # 3. Ambil CSV dari GDrive & Join di Python (Channel)
    # Tips: Pake URL export CSV biar gampang ditarik Pandas
    def download_drive_csv(file_id):
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        return pd.read_csv(url)

    df_channel_raw = download_drive_csv(CSV_ID_CHANNEL)
    df_type_raw = download_drive_csv(CSV_ID_CHANNEL_TYPE)

    # JOIN Logic: merge dim_channel and dim_channel_type
    df_channel_final = pd.merge(
        df_channel_raw, 
        df_type_raw, 
        on='channel_type_id', 
        how='left'
    )

    return {
        "dim_customer_segmentation": df_customer,
        "dim_promo_dependency": df_promo,
        "dim_channel": df_channel_final
    }
    
if __name__ == "__main__":
    print("🧪 Testing Dimension Fetching...")
    
    # 1. Panggil fungsinya dan simpan hasilnya ke variabel
    all_dimensions = fetch_and_join_dimensions()
    
    # 2. Looping dictionary-nya untuk print head masing-masing table
    for table_name, df in all_dimensions.items():
        print(f"\n--- Table: {table_name} ---")
        print(f"Total Rows: {len(df)}")
        print(df.head()) # Ini yang lo cari!
        print("-" * 30)