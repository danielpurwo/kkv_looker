To run this pipeline, just install uv and run: uv run main.py

I chose a Star Schema approach for data storage to maintain data integrity, but utilized BigQuery SQL Views to provide a denormalized, flattened layer for Looker Studio. This balances storage efficiency with dashboard performance.

Data Architecture: Fact (BigQuery Cloud DB) | Dimensions (Google Sheets) | Automated via Python.

I built a Tool-Agnostic Data Layer using BigQuery Views. This ensures that whether the business uses Looker, Tableau, or Power BI, they are all looking at the same 'Single Source of Truth' without duplicating complex join logic in each tool.