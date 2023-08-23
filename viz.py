# Imports
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union

def concat_csv_from_directory(directory: Union[str, Path]) -> pd.DataFrame:
    """Concatenate CSV files from the data directory that start with "CRASH"

    Args:
        directory (Union[str, Path]): The directory path where CSV files are located

    Returns:
        pd.DataFrame: A concateated dataframe of all CSV files in the directory
    """
    
    # List of columns to be read
    columns = [
        "CRN", "INJURY_COUNT", "FATAL_COUNT", "MCYCLE_DEATH_COUNT", "BICYCLE_DEATH_COUNT",
        "PED_DEATH_COUNT", "CRASH_MONTH", "CRASH_YEAR",
        "DEC_LAT", "DEC_LONG"
    ]
    

    path = Path(directory)
    csv_files = [f for f in path.glob('CRASH*.csv')]
    
    # Using list comprehension to read the CSV files into dataframes
    list_of_dataframes = [pd.read_csv(filename, usecols=columns) for filename in csv_files]
    
    concatenated_dataframe = pd.concat(list_of_dataframes, ignore_index=True)
    
    return concatenated_dataframe

# Fetch crash data directly by passing the directory path to the function
crash_data = concat_csv_from_directory(Path.cwd() / "data")