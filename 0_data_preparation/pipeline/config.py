# -*- coding: utf-8 -*-
"""
Configuration for the NHANES data pipeline.
"""

import os

# --- Configuration ---
GCP_PROJECT_ID = "public-health-agent"
BIGQUERY_DATASET_ID = "nhanes_data"
BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"

# Dictionary of NHANES files to process
NHANES_FILES_TO_PROCESS = {
    "1999-2000": ["DEMO", "BMX", "BPX", "LAB18"],
    "2001-2002": ["DEMO", "BMX", "BPX", "L18_B"],
    "2003-2004": ["DEMO", "BMX", "BPX", "L18_C"],
    "2005-2006": ["DEMO", "BMX", "BPX", "ALB_CR_D"],
    "2007-2008": ["DEMO", "BMX", "BPX", "ALB_CR_E"],
    "2009-2010": ["DEMO", "BMX", "BPX", "ALB_CR_F"],
    "2011-2012": ["DEMO", "BMX", "BPX", "ALB_CR_G"],
    "2013-2014": ["DEMO", "BMX", "BPX", "ALB_CR_H"],
    "2015-2016": ["DEMO", "BMX", "BPX", "ALB_CR_I"],
    "2017-2018": ["DEMO", "BMX", "BPX", "P_ALB_CR"],
}

# Suffix mapping for different survey cycles
CYCLE_SUFFIX_MAP = {
    "1999-2000": "",
    "2001-2002": "_B",
    "2003-2004": "_C",
    "2005-2006": "_D",
    "2007-2008": "_E",
    "2009-2010": "_F",
    "2011-2012": "_G",
    "2013-2014": "_H",
    "2015-2016": "_I",
    "2017-2018": "_J",
}

# --- Directory Setup ---
CWD = os.path.join(os.getcwd(), "0_data_preparation")
XPT_DIR = os.path.join(CWD, "xpt_files")
CSV_DIR = os.path.join(CWD, "csv_files")
DOC_DIR = os.path.join(CWD, "doc_files")

def setup_directories():
    """Create local directories."""
    os.makedirs(XPT_DIR, exist_ok=True)
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(DOC_DIR, exist_ok=True)