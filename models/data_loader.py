import pandas as pd

def load_data(filepath):
    """
    Load data from a CSV or JSON file into a pandas DataFrame.
    
    Args:
        filepath (str): Path to the file to be loaded.

    Returns:
        DataFrame: Loaded data.
    """
    try:
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            return pd.read_json(filepath)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
