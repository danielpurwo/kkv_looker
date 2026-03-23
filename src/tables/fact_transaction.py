import pandas as pd
import numpy as np
import uuid
from src.helpers import fetch_all_external_data

def generate_complex_transactions(dim_date, dim_product, dim_customer, dim_store):
    print("🧹 Cleaning data types and column names...")
    
    # --- JURUS ANTI-ERROR 1: Paksa Lowercase & Strip ---
    for df in [dim_date, dim_product, dim_customer, dim_store]:
        df.columns = [str(col).strip().lower() for col in df.columns]

    # --- JURUS ANTI-HANTU: Mapping Nama Kolom ---
    # Kadang di GSheet namanya 'home_city_id', kadang 'city_id'
    if 'home_city_id' not in dim_customer.columns:
        city_cols = [c for c in dim_customer.columns if 'city' in c]
        if city_cols:
            print(f"⚠️ Warning: 'home_city_id' gak ketemu, pake '{city_cols[0]}'")
            dim_customer = dim_customer.rename(columns={city_cols[0]: 'home_city_id'})

    # --- JURUS ANTI-ERROR 2: Paksa Tipe Data ID jadi Numeric ---
    # 'coerce' bakal ganti data yang bukan angka jadi NaN, biar gak crash
    dim_customer['home_city_id'] = pd.to_numeric(dim_customer['home_city_id'], errors='coerce')
    dim_store['city_id'] = pd.to_numeric(dim_store['city_id'], errors='coerce')
    dim_product['brand_id'] = pd.to_numeric(dim_product['brand_id'], errors='coerce')
    dim_store['brand_id'] = pd.to_numeric(dim_store['brand_id'], errors='coerce')

    fact_rows = []
    dim_trx_rows = []
    trx_id_counter = 1

    # --- FIX 1: Dinamis ambil Tahun & Bulan ---
    years = dim_date['year'].unique()
    monthly_factors = {}
    for year in years:
        for month in range(1, 13):
            monthly_factors[(year, month)] = {
                'rev_factor': np.random.uniform(0.90, 1.10),
                'cost_factor': np.random.uniform(0.85, 1.15),
                'promo_prob_factor': np.random.uniform(0.5, 1.5)
            }

    # --- FIX 2: Safe Sampling ---
    sample_size = min(len(dim_date), 100)
    sampled_dates = dim_date.sample(sample_size)

    for _, date_row in sampled_dates.iterrows():
        # Fallback factor kalau tahun/bulan gak match di dictionary
        factors = monthly_factors.get((date_row['year'], date_row['month']), 
                                     {'rev_factor': 1.0, 'cost_factor': 1.0, 'promo_prob_factor': 1.0})
        
        daily_volatility = np.random.uniform(0.8, 1.2)
        num_transactions = int(500 * daily_volatility)

        for _ in range(num_transactions):
            # 1. Pilih Customer
            cust = dim_customer.sample(1).iloc[0]
            
            # 2. Pilih Store (Logic Home City)
            # Pastiin kolomnya ada, kalau gak ada ambil random store
            match_store = dim_store[dim_store['city_id'] == cust['home_city_id']]
            
            if not match_store.empty and np.random.random() < 0.9:
                store = match_store.sample(1).iloc[0]
            else:
                store = dim_store.sample(1).iloc[0]
            
            # 3. Tentukan isi keranjang (Basket Size)
            r = np.random.random()
            if r < 0.12: num_items = 1
            elif r < 0.50: num_items = np.random.randint(2, 5)
            elif r < 0.93: num_items = np.random.randint(4, 7)
            else: num_items = np.random.randint(7, 12)

            trx_code = f"TRX-{uuid.uuid4().hex[:6].upper()}"
            discount_pct = round(np.random.uniform(0, 15), 2)
            current_channel_id = np.random.choice([1, 2, 3, 4], p=[0.7, 0.1, 0.1, 0.1])
            omni_flag = 1 if current_channel_id > 1 else 0
            
            # 4. Filter produk berdasarkan Brand Store
            available_prods = dim_product[dim_product['brand_id'] == store['brand_id']]
            if available_prods.empty: continue
            
            # Ambil produk acak sebanyak num_items
            num_to_pick = min(len(available_prods), num_items)
            basket_prods = available_prods.sample(num_to_pick)

            header_revenue = 0
            categories_in_trx = set()
            
            # 5. Loop per Item (Fact Table)
            for _, prod in basket_prods.iterrows():
                qty = np.random.randint(1, 4)
                
                line_revenue = round(qty * prod['price'] * factors['rev_factor'] * np.random.uniform(0.98, 1.02), 2)
                line_cost = round(qty * prod['unit_cost'] * factors['cost_factor'] * np.random.uniform(0.99, 1.01), 2)
                
                header_revenue += line_revenue
                categories_in_trx.add(prod['category'])
                
                promo_chance = max(0.1, min(0.9, 0.3 * factors['promo_prob_factor']))
                promo_id = np.random.choice([0, 1, 2, 3], p=[(1-promo_chance), promo_chance*0.5, promo_chance*0.3, promo_chance*0.2])

                fact_rows.append({
                    'date_id': date_row['date_id'],
                    'store_id': store['store_id'],
                    'brand_id': store['brand_id'],
                    'channel_id': current_channel_id,
                    'segment_id': np.random.choice([1, 2, 3, 4, 5]),
                    'customer_id': cust['customer_id'],
                    'product_id': prod['product_id'],
                    'transaction_id_num': trx_id_counter,
                    'quantity': qty,
                    'revenue_myr': line_revenue,
                    'total_cost_myr': line_cost,
                    'promo_dependency_id': promo_id,
                    'oos_flag': np.random.choice([0, 1], p=[0.97, 0.03])
                })

            # 6. Simpan Header Data (Dim Transaction)
            dim_trx_rows.append({
                'transaction_id_num': trx_id_counter,
                'transaction_code': trx_code,
                'discount_amount': round(header_revenue * (discount_pct/100), 2),
                'total_amount': round(header_revenue, 2), # Ganti ABV jadi total_amount biar lebih umum
                'categories_count': len(categories_in_trx),
                'is_omnichannel': omni_flag
            })
            
            trx_id_counter += 1

    print(f"✅ Generation Complete: {len(fact_rows)} fact rows created.")
    return {
        "fact_transaction": pd.DataFrame(fact_rows),
        "dim_transaction": pd.DataFrame(dim_trx_rows)
    }
    
    
# --- BLOCK UNTUK TESTING ---
if __name__ == "__main__":
    print("🚀 Running Fact Transaction with 100% REAL DATA...")
    raw_data = fetch_all_external_data()
    
    results = generate_complex_transactions(
        dim_date=raw_data['date'], 
        dim_product=raw_data['product'], 
        dim_customer=raw_data['customer'], 
        dim_store=raw_data['store']
    )

    for name, df in results.items():
        print(f"\n--- Top 5 {name} ---")
        print(df.head())
        print(f"Total rows: {len(df)}")