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
from pipeline.download import download_nhanes_file, download_nhanes_doc, get_file_suffix
from pipeline.convert import convert_xpt_to_csv
from pipeline.upload import upload_to_bigquery
from pipeline.parser import parse_nhanes_doc


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

            # Download the data file
            xpt_path = download_nhanes_file(cycle, prefix, suffix)
            # Download the documentation file
            doc_path = download_nhanes_doc(cycle, prefix, suffix)

            column_metadata = {}
            if doc_path:
                column_metadata = parse_nhanes_doc(doc_path)

            if xpt_path and os.path.exists(xpt_path) and os.path.getsize(xpt_path) > 0:
                csv_path = convert_xpt_to_csv(xpt_path, column_metadata)
                if csv_path:
                    upload_to_bigquery(csv_path, table_id, column_metadata)
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