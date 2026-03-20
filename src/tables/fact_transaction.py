import pandas as pd
import numpy as np
import uuid

def generate_complex_transactions(dim_date, dim_product, dim_customer, dim_store):
    fact_rows = []
    dim_trx_rows = []
    trx_id_counter = 1

    # Logic Affinity lo
    product_affinities = {
        "Hardware": "Hardware", "Household": "Household", "Food & Snacks": "Food & Snacks",
        "Beauty & Personal Care": "Beauty & Personal Care", "Stationery": "Stationery",
        "Phone & Tech Accessories": "Phone & Tech Accessories"
    }

    # --- FIX 1: MONTHLY FACTORS (Anomali Bulanan) ---
    monthly_factors = {}
    for year in [2024, 2025]:
        for month in range(1, 13):
            monthly_factors[(year, month)] = {
                'rev_factor': np.random.uniform(0.90, 1.10),
                'cost_factor': np.random.uniform(0.85, 1.15),
                'promo_prob_factor': np.random.uniform(0.5, 1.5)
            }

    sampled_dates = dim_date.sample(100)

    for _, date_row in sampled_dates.iterrows():
        factors = monthly_factors[(date_row['year'], date_row['month'])]
        daily_volatility = np.random.uniform(0.8, 1.2)
        num_transactions = int(500 * daily_volatility)

        for _ in range(num_transactions):
            # 1. Pilih Customer & Store (Logic Home City lo)
            cust = dim_customer.sample(1).iloc[0]
            if np.random.random() < 0.9:
                store = dim_store[dim_store['city_id'] == cust['home_city_id']].sample(1).iloc[0]
            else:
                store = dim_store.sample(1).iloc[0]
            
            # 2. Tentukan isi keranjang (Basket Size)
            r = np.random.random()
            if r < 0.12: num_items = 1
            elif r < 0.50: num_items = np.random.randint(2, 5)
            elif r < 0.93: num_items = np.random.randint(4, 7)
            else: num_items = np.random.randint(7, 12)

            trx_code = f"TRX-{uuid.uuid4().hex[:6].upper()}"
            discount_pct = round(np.random.uniform(0, 15), 2)
            current_channel_id = np.random.choice([1, 2, 3, 4], p=[0.7, 0.1, 0.1, 0.1])
            omni_flag = 1 if current_channel_id > 1 else 0
            
            # 3. Filter produk berdasarkan Brand Store
            available_prods = dim_product[dim_product['brand_id'] == store['brand_id']]
            if available_prods.empty: continue
            
            # 4. Logic Affinity (Produk yang sering dibeli bareng)
            first_prod = available_prods.sample(1).iloc[0]
            basket_pids = [first_prod['product_id']]
            
            # ... (Logic affinity lo tetep jalan di sini) ...
            while len(basket_pids) < num_items:
                random_prod = available_prods.sample(1).iloc[0]
                if random_prod['product_id'] not in basket_pids:
                    basket_pids.append(random_prod['product_id'])

            header_revenue = 0
            categories_in_trx = set()
            
            # 5. Loop per Item (Fact Table)
            for p_id in basket_pids:
                prod = dim_product[dim_product['product_id'] == p_id].iloc[0]
                qty = np.random.randint(1, 4)
                
                # Structural Noise (Revenue & Cost)
                line_revenue = round(qty * prod['price'] * factors['rev_factor'] * np.random.uniform(0.98, 1.02), 2)
                line_cost = round(qty * prod['unit_cost'] * factors['cost_factor'] * np.random.uniform(0.99, 1.01), 2)
                
                header_revenue += line_revenue
                categories_in_trx.add(prod['category'])
                
                # Promo logic
                promo_chance = max(0.1, min(0.9, 0.6 * factors['promo_prob_factor']))
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
                'ABV': round(header_revenue, 2),
                'avg_categories_per_receipt': len(categories_in_trx),
                'omnichannel_rate': omni_flag
            })
            
            trx_id_counter += 1

    # RETURN DUA-DUANYA DALAM DICTIONARY
    return {
        "fact_transaction": pd.DataFrame(fact_rows),
        "dim_transaction": pd.DataFrame(dim_trx_rows)
    }