# -*- coding: utf-8 -*-
"""
Main script to run the NHANES data pipeline.
"""
import os
from pipeline.config import (
    NHANES_FILES_TO_PROCESS,
    XPT_DIR,
    CSV_DIR,
    setup_directories,
)
from pipeline.download import download_nhanes_file, get_file_suffix
from pipeline.convert import convert_xpt_to_csv
from pipeline.upload import upload_to_bigquery


def main():
    """Main function to orchestrate the data pipeline."""
    print("--- Starting NHANES Data Pipeline ---")
    setup_directories()

    for cycle, prefixes in NHANES_FILES_TO_PROCESS.items():
        print(f"\nProcessing cycle: {cycle}")
        for prefix in prefixes:
            suffix = get_file_suffix(cycle, prefix)
            table_id_prefix = prefix.replace("P_", "")
            table_id = f"{table_id_prefix}{suffix}_{cycle.replace('-', '_')}"

            xpt_path = download_nhanes_file(cycle, prefix, suffix)
            if xpt_path and os.path.exists(xpt_path) and os.path.getsize(xpt_path) > 0:
                csv_path = convert_xpt_to_csv(xpt_path)
                if csv_path:
                    upload_to_bigquery(csv_path, table_id)
            else:
                print(f"Skipping conversion and upload for {prefix} due to download failure.")
            print("-" * 20)

    print("\n--- NHANES Data Pipeline Finished ---")


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        )
        print(
            "Please ensure you have authenticated with 'gcloud auth application-default login'"
        )

    main()