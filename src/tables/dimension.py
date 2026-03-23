import pandas as pd

def generate_static_dimensions():
    # 1. Segments
    dim_customer_segment = pd.DataFrame([
        {'segment_id': 1, 'segment_name': 'High-Value'},
        {'segment_id': 2, 'segment_name': 'Bulk Buyers'},
        {'segment_id': 3, 'segment_name': 'Regulars'},
        {'segment_id': 4, 'segment_name': 'Promo-Driven'},
        {'segment_id': 5, 'segment_name': 'New Customers'}
    ])

    # 2. Channels
    dim_channel = pd.DataFrame([
        {'channel_id': 1, 'channel_name': 'In-Store', 'channel_type_id': 1},
        {'channel_id': 2, 'channel_name': 'WhatsApp', 'channel_type_id': 2},
        {'channel_id': 3, 'channel_name': 'META', 'channel_type_id': 2},
        {'channel_id': 4, 'channel_name': 'Website', 'channel_type_id': 2}
    ])

    # 3. Promo Dependency
    dim_promo_dependency = pd.DataFrame([
        {'promo_dependency_id': 1, 'promo_type': 'Non-Promo', 'description': 'Full Price Items'},
        {'promo_dependency_id': 2, 'promo_type': 'Seasonal Sale', 'description': 'Festive/Seasonal Discounts'},
        {'promo_dependency_id': 3, 'promo_type': 'Member Exclusive', 'description': 'Loyalty Program Offers'},
        {'promo_dependency_id': 4, 'promo_type': 'Flash Sale', 'description': 'Limited Time Deals'}
    ])

    return {
        "dim_brand": dim_brand,
        "dim_customer_segmentation": dim_customer_segment,
        "dim_channel": dim_channel,
        "dim_promo_dependency": dim_promo_dependency
    }