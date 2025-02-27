"""
Utility functions for the Real Estate Analytics application.

This module contains helpers for data loading/saving, formatting, and file operations.
"""

import os
import json
import csv
import pickle
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union, Optional

# Data directory configuration
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROPERTY_DATA_FILE = "properties.json"
ANALYSIS_DATA_FILE = "analysis_results.json"

# Ensure data directory exists
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)


def load_data(filepath: str = None, data_type: str = "properties") -> Union[List[Dict], Dict, None]:
    """
    Load data from a file (JSON, CSV, Pickle).
    
    Args:
        filepath: Path to the data file. If None, uses default locations.
        data_type: Type of data to load ('properties' or 'analysis')
        
    Returns:
        Loaded data as dictionary, list, or None if file doesn't exist
    """
    if not filepath:
        # Use default locations based on data type
        if data_type == "properties":
            filepath = os.path.join(DEFAULT_DATA_DIR, PROPERTY_DATA_FILE)
        elif data_type == "analysis":
            filepath = os.path.join(DEFAULT_DATA_DIR, ANALYSIS_DATA_FILE)
    
    if not os.path.exists(filepath):
        return None
    
    file_ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if file_ext == '.json':
            with open(filepath, 'r') as f:
                return json.load(f)
        elif file_ext == '.csv':
            return pd.read_csv(filepath).to_dict(orient='records')
        elif file_ext == '.pkl' or file_ext == '.pickle':
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        elif file_ext in ['.xls', '.xlsx']:
            return pd.read_excel(filepath).to_dict(orient='records')
        else:
            print(f"Unsupported file format: {file_ext}")
            return None
    except Exception as e:
        print(f"Error loading data from {filepath}: {str(e)}")
        return None


def save_data(data: Union[List, Dict], filepath: str = None, data_type: str = "properties") -> bool:
    """
    Save data to a file (JSON, CSV, Pickle).
    
    Args:
        data: Data to save (list or dictionary)
        filepath: Path to save the file. If None, uses default locations.
        data_type: Type of data to save ('properties' or 'analysis')
        
    Returns:
        Boolean indicating success
    """
    if not filepath:
        # Use default locations based on data type
        if data_type == "properties":
            filepath = os.path.join(DEFAULT_DATA_DIR, PROPERTY_DATA_FILE)
        elif data_type == "analysis":
            filepath = os.path.join(DEFAULT_DATA_DIR, ANALYSIS_DATA_FILE)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    file_ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if file_ext == '.json':
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        elif file_ext == '.csv':
            pd.DataFrame(data).to_csv(filepath, index=False)
        elif file_ext == '.pkl' or file_ext == '.pickle':
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
        elif file_ext in ['.xls', '.xlsx']:
            pd.DataFrame(data).to_excel(filepath, index=False)
        else:
            print(f"Unsupported file format: {file_ext}")
            return False
        return True
    except Exception as e:
        print(f"Error saving data to {filepath}: {str(e)}")
        return False


def format_currency(value: float) -> str:
    """Format a number as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format a number as percentage."""
    return f"{value:.2f}%"


def format_date(date_obj: datetime = None) -> str:
    """Format a date object as string."""
    if date_obj is None:
        date_obj = datetime.now()
    return date_obj.strftime("%Y-%m-%d")


def convert_to_number(value: str) -> Optional[float]:
    """
    Convert string to number, handling currency and percentage formats.
    
    Args:
        value: String value to convert
        
    Returns:
        Float value or None if conversion fails
    """
    if not value or not isinstance(value, str):
        return None
    
    # Remove currency symbols and commas
    clean_value = value.replace('$', '').replace(',', '').replace('%', '')
    
    try:
        return float(clean_value)
    except ValueError:
        return None


def get_property_by_id(properties: List[Dict], property_id: str) -> Optional[Dict]:
    """
    Find a property by its ID.
    
    Args:
        properties: List of property dictionaries
        property_id: ID to search for
        
    Returns:
        Property dictionary or None if not found
    """
    for prop in properties:
        if prop.get('id') == property_id:
            return prop
    return None


def generate_property_id() -> str:
    """Generate a unique property ID based on timestamp."""
    return f"prop_{int(datetime.now().timestamp())}"


def backup_data(data_type: str = "properties") -> bool:
    """
    Create a backup of the specified data file.
    
    Args:
        data_type: Type of data to backup ('properties' or 'analysis')
        
    Returns:
        Boolean indicating success
    """
    if data_type == "properties":
        src_file = os.path.join(DEFAULT_DATA_DIR, PROPERTY_DATA_FILE)
    elif data_type == "analysis":
        src_file = os.path.join(DEFAULT_DATA_DIR, ANALYSIS_DATA_FILE)
    else:
        return False
        
    if not os.path.exists(src_file):
        return False
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(DEFAULT_DATA_DIR, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    file_name = os.path.basename(src_file)
    backup_file = os.path.join(backup_dir, f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}")
    
    try:
        with open(src_file, 'rb') as src:
            with open(backup_file, 'wb') as dst:
                dst.write(src.read())
        return True
    except Exception as e:
        print(f"Backup failed: {str(e)}")
        return False


def export_to_csv(data: List[Dict], filepath: str) -> bool:
    """
    Export data to CSV file.
    
    Args:
        data: List of dictionaries to export
        filepath: Path to save the CSV file
        
    Returns:
        Boolean indicating success
    """
    try:
        pd.DataFrame(data).to_csv(filepath, index=False)
        return True
    except Exception as e:
        print(f"CSV export failed: {str(e)}")
        return False


def import_from_csv(filepath: str) -> Optional[List[Dict]]:
    """
    Import data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries or None if import fails
    """
    try:
        return pd.read_csv(filepath).to_dict(orient='records')
    except Exception as e:
        print(f"CSV import failed: {str(e)}")
        return None

