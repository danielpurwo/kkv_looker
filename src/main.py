from src.helpers import fetch_external_dimensions
from src.tables.fact_transaction import generate_complex_transactions
from src.database import push_to_bigquery
# Import static dims lainnya (Promo, Channel, dll)
from src.tables.dimensions import generate_static_dimensions

def run_pipeline():
    print("🚀 Starting Hybrid Data Pipeline...")
    
    # 1. Ambil data dimensi dari GSheet (LIVE!)
    df_date, df_product = fetch_external_dimensions()
    
    # 2. Ambil data statis lainnya (Promo, dll)
    static_dims = generate_static_dimensions()
    
    # 3. Generate Fact pake data dari GSheet biar SINKRON
    # Pastiin fungsi generate_complex_transactions lo nerima df_date & df_product
    fact_data = generate_complex_transactions(df_date, df_product)
    
    # 4. Gabungin semua buat ditembak
    all_tables = {**static_dims, **fact_data}
    
    # 5. Tembak ke BigQuery
    for name, df in all_tables.items():
        push_to_bigquery(df, name)

if __name__ == "__main__":
    run_pipeline()