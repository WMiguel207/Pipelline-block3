import os
from dotenv import load_dotenv
from google.cloud import bigquery
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

project = os.getenv("GCP_PROJECT")
dataset = os.getenv("GCP_DATASET")

print("PROJECT:", os.getenv("GCP_PROJECT"))
print("DATASET:", os.getenv("GCP_DATASET"))

if not project or not dataset:
    raise ValueError("Missing GCP_PROJECT or GCP_DATASET in .env")

client = bigquery.Client(project=project)

query = f"""
SELECT 'raw_customers' AS t,
       COUNT(*) AS row_count,
       COUNT(DISTINCT customer_id) AS pk
FROM `{project}.{dataset}.raw_customers`

UNION ALL

SELECT 'raw_products',
       COUNT(*),
       COUNT(DISTINCT product_id)
FROM `{project}.{dataset}.raw_products`

UNION ALL

SELECT 'raw_orders',
       COUNT(*),
       COUNT(DISTINCT order_id)
FROM `{project}.{dataset}.raw_orders`

UNION ALL

SELECT 'raw_order_items',
       COUNT(*),
       COUNT(DISTINCT CONCAT(order_id, '-', product_id))
FROM `{project}.{dataset}.raw_order_items`
"""

results = client.query(query).result()

print("\n=== IDEMPOTENCY CHECK ===\n")

all_ok = True

for row in results:
    table = row["t"]
    row_count = row["row_count"]
    pk = row["pk"]

    status = "OK" if row_count == pk else "DUPLICATED ❌"

    if row_count != pk:
        all_ok = False

    print(f"{table:20} rows={row_count:6} pk={pk:6} → {status}")

print("\n=========================")

if not all_ok:
    raise Exception("Idempotency check FAILED")
else:
    print("All tables are idempotent ✅")