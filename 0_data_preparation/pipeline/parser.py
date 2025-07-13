# -*- coding: utf-8 -*-
"""
Parses NHANES HTML documentation to extract column and value descriptions.
"""
import os
import re
from bs4 import BeautifulSoup

def parse_nhanes_doc(doc_path):
    """
    Parses an NHANES HTML documentation file to extract metadata.
    """
    if not doc_path or not os.path.exists(doc_path):
        return {}

    with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')

    column_metadata = {}

    # Find all 'Variable Name' sections
    variable_headers = soup.find_all('h3', id=re.compile(r'^Var_'))
    for header in variable_headers:
        variable_name = header.get('id').replace('Var_', '')
        column_metadata[variable_name] = {
            'description': header.get_text(strip=True),
            'values': {}
        }

        # Find the table with value descriptions following the header
        table = header.find_next_sibling('table')
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 2:
                    value_code = cols[0].get_text(strip=True)
                    value_desc = cols[1].get_text(strip=True)
                    # Try to convert value_code to a number if possible
                    try:
                        value_code = float(value_code)
                        if value_code.is_integer():
                            value_code = int(value_code)
                    except ValueError:
                        pass
                    column_metadata[variable_name]['values'][value_code] = value_desc

    return column_metadata
