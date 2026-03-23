# 🛒 KKV Retail Analytics: End-to-End Data Pipeline

An automated data engineering pipeline designed to bridge fragmented retail data (Google Sheets/Drive) into a centralized, high-performance Cloud Warehouse (Google BigQuery) for BI orchestration via Looker Studio.

## 🏗️ Data Architecture Overview
This project implements a **Hybrid Medallion-style Architecture** tailored for high-growth retail environments:

* **Extraction Layer:** Multi-source ingestion from Google Sheets (Dimensions) and Google Drive (Raw CSVs) using Python.
* **Storage Layer (Star Schema):** Data is stored in BigQuery using a Star Schema (Fact & Dimension tables) to ensure strict data integrity and storage efficiency.
* **Analytics Layer (Tool-Agnostic):** A denormalized **SQL View** layer acts as the "Single Source of Truth." This ensures that BI tools (Looker, Power BI, or Tableau) consume consistent, pre-joined data without duplicating complex logic in the visualization layer.



## 🛠️ Tech Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | Python 3.12+ (uv) | Ingestion, Cleaning, & Loading |
| **Warehouse** | Google BigQuery | Cloud Storage & Compute |
| **BI Tool** | Looker Studio | Executive & Growth Command Center |
| **Environment** | `uv` package manager | Fast, reproducible virtual environments |

## 🚀 Getting Started

### Prerequisites
1.  Python 3.12+ installed.
2.  Google Cloud Service Account with `BigQuery Data Editor` and `Job User` permissions.
3.  `.env` or `config.py` populated with your `PROJECT_ID`, `DATASET_ID`, and `GCP_KEY_PATH`.

### Installation & Execution
This project uses **uv** for ultra-fast dependency management:

```bash
# Install dependencies and run the pipeline in one command
uv run python -m src.main
```

## 🧠 Key Engineering Decisions

1. The "View" vs "Table" Strategy
I utilized BigQuery SQL Views for the final presentation layer.
* **Performance:** Offloads heavy JOIN operations to BigQuery’s engine.
* **Flexibility:** Allows schema updates without re-running the ingestion.

2. Structural Noise & Data Integrity
The Python generator includes logic for Structural Noise, simulating realistic retail volatility (seasonal factors, weekend spikes) to provide more meaningful insights during the BI prototyping phase.

3. Idempotency (Write-Truncate)
The pipeline is designed to be Idempotent. Using a WRITE_TRUNCATE strategy during development ensures a clean state on every run, preventing data duplication during trial and error.


👨‍💻 Developer
Daniel – Head of Business Solution of Analyset