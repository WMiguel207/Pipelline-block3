import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery

# garante que o .env da raiz será carregado
ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

# pega configs do .env
project = os.getenv("GCP_PROJECT")
dataset = os.getenv("GCP_DATASET")

if not project or not dataset:
    raise ValueError("Missing GCP_PROJECT or GCP_DATASET in .env")

client = bigquery.Client(project=project)

tables = [
    "raw_orders",
    "raw_order_items",
    "raw_customers",
    "raw_products",
]

print("\n=== RESET RAW TABLES ===\n")

for table in tables:
    table_id = f"{project}.{dataset}.{table}"
    query = f"TRUNCATE TABLE `{table_id}`"

    print(f"Truncating {table_id} ...")
    client.query(query).result()
    print(f"{table} cleared ✔️")

print("\nAll raw tables reset successfully.\n")