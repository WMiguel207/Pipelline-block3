import logging
import os
import re
from dotenv import load_dotenv
load_dotenv()

from google.cloud import bigquery, storage

path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print("EXISTS on gcp_to_bq:", os.path.exists(path))

def list_files(bucket_name, prefix):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs if blob.name.lower().endswith(".csv")]


def sanitize_table_name(name):
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_").lower()
    return cleaned

def load_to_staging(uri, table_id):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",  # sempre limpa staging
    )

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()


    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()

def merge_orders(dataset, staging_table, target_table):
    client = bigquery.Client()

    query = f"""
    MERGE `{target_table}` T
    USING `{staging_table}` S
    ON T.order_id = S.order_id

    WHEN MATCHED THEN
      UPDATE SET
        customer_id = S.customer_id,
        status = S.status,
        order_date = S.order_date

    WHEN NOT MATCHED THEN
      INSERT (order_id, customer_id, status, order_date)
      VALUES (S.order_id, S.customer_id, S.status, S.order_date)
    """

    client.query(query).result()

def run_extraction():
    bucket = os.getenv("GCS_BUCKET", "outcoder-miguel-block3-source")
    dataset = os.getenv("BQ_DATASET", "miguel-490720.miguel_block3")
    prefix = os.getenv("GCS_PREFIX", "v1/")

    files = list_files(bucket, prefix)
    if not files:
        logging.warning("No CSV files found in gs://%s/%s", bucket, prefix)
        return 0

    loaded_count = 0
    for file in files:
        source_name = file.split("/")[-1].replace(".csv", "")
        table_name = sanitize_table_name(source_name)
        if not table_name:
            raise ValueError(f"Invalid table name from file: {file}")

        uri = f"gs://{bucket}/{file}"
        table_id = f"{dataset}.raw_{table_name}"

        logging.info("Loading %s into %s", file, table_id)
        try:
            staging_table = f"{dataset}._stg_{table_name}"
            target_table = f"{dataset}.raw_{table_name}"

            load_to_staging(uri, staging_table)

            # só faz MERGE se for orders
            if table_name == "orders":
                merge_orders(dataset, staging_table, target_table)
            else:
                load_to_staging(uri, target_table)  # fallback simples
                loaded_count += 1
        except Exception:
            logging.exception("Failed loading file %s into %s", file, table_id)
            raise

    logging.info("Extraction finished. %s file(s) loaded.", loaded_count)
    return loaded_count
