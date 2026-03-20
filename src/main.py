from src.tables.dimensions import generate_base_dimensions
from src.tables.fact_transaction import generate_transactions
from src.database import push_to_bigquery

def run_pipeline():
    print("🚀 Starting KKV Data Pipeline...")

    base_dims = generate_base_dimensions()
    transactions = generate_transactions(num_trx=2000)

    all_data = {**base_dims, **transactions}

    for table_name, df in all_data.items():
        push_to_bigquery(df, table_name)

    print("\n🔥 Pipeline Done!")

if __name__ == "__main__":
    run_pipeline()