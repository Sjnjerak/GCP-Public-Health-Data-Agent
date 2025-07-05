# -*- coding: utf-8 -*-
"""
Downloads NHANES data files from the CDC website.
"""
import os
import sys
import requests
import argparse
from pipeline.config import XPT_DIR, CYCLE_SUFFIX_MAP

# The new base URL for downloading public data files.
BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"

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

def main():
    """Main function to download a file."""
    parser = argparse.ArgumentParser(description="Download a single NHANES file.")
    parser.add_argument("cycle", help="The survey cycle (e.g., '1999-2000').")
    parser.add_argument("file_prefix", help="The file prefix (e.g., 'DEMO').")
    args = parser.parse_args()

    suffix = get_file_suffix(args.cycle, args.file_prefix)
    download_nhanes_file(args.cycle, args.file_prefix, suffix)

if __name__ == "__main__":
    main()
