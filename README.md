To run this pipeline, just install uv and run: uv run main.py

I chose a Star Schema approach for data storage to maintain data integrity, but utilized BigQuery SQL Views to provide a denormalized, flattened layer for Looker Studio. This balances storage efficiency with dashboard performance.

Data Architecture: Fact (BigQuery Cloud DB) | Dimensions (Google Sheets) | Automated via Python.