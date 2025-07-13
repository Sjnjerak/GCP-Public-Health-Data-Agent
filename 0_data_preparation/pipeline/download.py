# -*- coding: utf-8 -*-
"""
Downloads NHANES data files from the CDC website.
"""
import os
import sys
import requests
import argparse
from pipeline.config import XPT_DIR, DOC_DIR, CYCLE_SUFFIX_MAP

# The new base URL for downloading public data files.
BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"
# Base URL for documentation pages
DOC_BASE_URL = "https://wwwn.cdc.gov/Nchs/Nhanes"

def get_file_suffix(cycle, file_prefix):
    """Gets the correct file suffix for a given cycle and file prefix."""
    if any(f"_{s}" in file_prefix for s in ["B", "C", "D", "E", "F", "G", "H", "I"]):
        return ""
    if cycle == "2017-2018" and file_prefix.startswith("P_"):
        return "_J"
    return CYCLE_SUFFIX_MAP.get(cycle, "")

def download_nhanes_file(cycle, file_prefix, suffix):
    """Downloads a single NHANES file using the new URL structure."""
    start_year = cycle.split('-')[0]

    # Construct the filename
    if cycle == "2017-2018" and file_prefix == "P_ALB_CR":
        file_name = "ALB_CR_J.xpt"
    else:
        # Ensure the extension is lowercase .xpt as seen in the example URL
        file_name = f"{file_prefix}{suffix}.xpt"

    # Construct the full URL
    url = f"{BASE_URL}/{start_year}/DataFiles/{file_name}"
    local_xpt_path = os.path.join(XPT_DIR, file_name)

    print(f"Downloading: {url}")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            # Check for valid content type, which should be 'application/octet-stream' or similar binary type
            if "application/octet-stream" not in r.headers.get("Content-Type", ""):
                print(f"Warning: Unexpected content type {r.headers.get('Content-Type')}. Proceeding with download.", file=sys.stderr)

            with open(local_xpt_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Check if the file was downloaded
        if os.path.exists(local_xpt_path) and os.path.getsize(local_xpt_path) > 0:
            print(f"Successfully downloaded to: {local_xpt_path}")
            return local_xpt_path
        else:
            print(f"Error: Download failed, file is empty for {url}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None

def download_nhanes_doc(cycle, file_prefix, suffix):
    """Downloads a single NHANES documentation file."""
    # Unlike data files, doc files don't have special naming conventions for P_ALB_CR
    if cycle == "2017-2018" and file_prefix == "P_ALB_CR":
        file_name = "ALB_CR_J.htm"
    else:
        file_name = f"{file_prefix}{suffix}.htm"

    # Construct the full URL
    url = f"{DOC_BASE_URL}/{cycle}/{file_name}"
    local_doc_path = os.path.join(DOC_DIR, file_name)

    print(f"Downloading documentation: {url}")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            # It's common for doc files to be missing, so we check for 404
            if r.status_code == 404:
                print(f"Warning: Documentation not found at {url} (404). Skipping.", file=sys.stderr)
                return None
            r.raise_for_status() # Raise an exception for other bad status codes

            # Check for valid content type, which should be 'text/html'
            if "text/html" not in r.headers.get("Content-Type", ""):
                print(f"Warning: Unexpected content type {r.headers.get('Content-Type')} for doc file. Proceeding.", file=sys.stderr)

            with open(local_doc_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        if os.path.exists(local_doc_path) and os.path.getsize(local_doc_path) > 0:
            print(f"Successfully downloaded documentation to: {local_doc_path}")
            return local_doc_path
        else:
            print(f"Error: Download failed, file is empty for {url}", file=sys.stderr)
            if os.path.exists(local_doc_path):
                os.remove(local_doc_path) # Clean up empty file
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error downloading documentation {url}: {e}", file=sys.stderr)
        return None

def main():
    """Main function to download a file."""
    parser = argparse.ArgumentParser(description="Download a single NHANES file and/or its documentation.")
    parser.add_argument("cycle", help="The survey cycle (e.g., '1999-2000').")
    parser.add_argument("file_prefix", help="The file prefix (e.g., 'DEMO').")
    parser.add_argument("--data-only", action="store_true", help="Only download the data file.")
    parser.add_argument("--doc-only", action="store_true", help="Only download the documentation file.")
    args = parser.parse_args()

    if args.data_only and args.doc_only:
        print("Error: Cannot use --data-only and --doc-only together.", file=sys.stderr)
        sys.exit(1)

    suffix = get_file_suffix(args.cycle, args.file_prefix)
    if not args.doc_only:
        download_nhanes_file(args.cycle, args.file_prefix, suffix)
    if not args.data_only:
        download_nhanes_doc(args.cycle, args.file_prefix, suffix)

if __name__ == "__main__":
    main()
