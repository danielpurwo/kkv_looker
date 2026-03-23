# src/main.py
import pandas as pd
from src.helpers import fetch_all_external_data
from src.tables.fact_transaction import generate_complex_transactions
from src.database import push_to_bigquery

def run_pipeline():
    print("🚀 STARTING KKV ANALYTICS PIPELINE...")
    
    # 1. EXTRACT: Tarik SEMUA data (GSheet & Drive)
    # raw_data isinya: date, product, customer, promo, store, channel_raw, type_raw
    raw = fetch_all_external_data()
    
    # 2. TRANSFORM: Olah Dimensi Tambahan
    # Contoh: Gabungin Channel dan Channel Type dari Drive
    print("🧹 Joining Channel Dimensions...")
    dim_channel = pd.merge(
        raw['channel_raw'], 
        raw['type_raw'], 
        on='channel_type_id', 
        how='left'
    )
    
    # 3. GENERATE: Bikin Fact & Transaksi Header
    # Sekarang kita oper 4 data utama ke generator lo yang udah sakti itu
    print("🧪 Generating Fact Transactions with Structural Noise...")
    generated = generate_complex_transactions(
        dim_date=raw['date'],
        dim_product=raw['product'],
        dim_customer=raw['customer'],
        dim_store=raw['store']
    )
    
    # 4. CONSOLIDATE: Kumpulin semua tabel yang mau dikirim ke BigQuery
    all_tables = {
        "dim_date": raw['date'],
        "dim_product": raw['product'],
        "dim_customer": raw['customer'],
        "dim_store": raw['store'],
        "dim_promo": raw['promo'],
        "dim_channel": dim_channel,
        "fact_transaction": generated['fact_transaction'],
        "dim_transaction_header": generated['dim_transaction']
    }
    
    # 5. LOAD: Tembak semua ke BigQuery satu per satu
    print("📡 Initializing Load to Google Cloud...")
    for name, df in all_tables.items():
        push_to_bigquery(df, name)

    print("\n🏁 SUCCESS: Seluruh data KKV sudah mendarat di BigQuery!")
    print("💡 Silakan buka Looker Studio dan klik 'Refresh Data'.")

if __name__ == "__main__":
    run_pipeline()