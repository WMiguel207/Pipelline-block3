import logging
import os
from pickle import load
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # PRIMEIRO

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from extraction.gcs_to_bq import run_extraction

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_dbt():
    root = Path(__file__).resolve().parents[1]

    dbt_project_dir = root / "dbt_project"
    profiles_dir = root / "config"

    subprocess.run(
        ["dbt", "run", "--profiles-dir", str(profiles_dir)],
        check=True,
        cwd=str(dbt_project_dir)
    )

    subprocess.run(
        ["dbt", "test", "--profiles-dir", str(profiles_dir)],
        check=True,
        cwd=str(dbt_project_dir)
    )

def main():
    try:
        logging.info("Starting pipeline")

        loaded_files = run_extraction()
        logging.info("Extraction completed. Loaded files: %s", loaded_files)

        run_dbt()
        logging.info("DBT completed")

    except Exception as e:
        logging.exception("Pipeline failed: %s", str(e))
        raise

if __name__ == "__main__":
    main()
