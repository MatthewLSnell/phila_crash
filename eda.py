# Standard Libraries
from pathlib import Path
from typing import Dict, Tuple, Union

# Data Handling Libraries
import pandas as pd
import numpy as np

# Visualization Libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Global Settings
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def concat_csv_from_directory(directory: Union[str, Path]) -> pd.DataFrame:
    """Concatenate CSV files from the specified directory that start with "CRASH"."""
    path = Path(directory)
    csv_files = [f for f in path.glob('CRASH*.csv')]
    list_of_dataframes = [pd.read_csv(filename) for filename in csv_files]
    concatenated_dataframe = pd.concat(list_of_dataframes, ignore_index=True)
    return concatenated_dataframe

def dataframe_summary(df: pd.DataFrame) -> None:
    """Display a comprehensive summary of the provided dataframe."""
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        # Various summary statistics presented
        sections = [
            ("Shape of the dataframe", df.shape),
            ("Comprehensive Info", df.info()),
            ("Value counts of data types", df.dtypes.value_counts()),
            ("Missing Values", pd.DataFrame({
                "Missing Count": df.isnull().sum(),
                "Missing Percentage (%)": (df.isnull().sum() / df.shape[0]) * 100
            })),
            ("Descriptive statistics for numerical columns", df.describe()),
            ("Descriptive statistics for non-numerical columns", df.describe(include=['object', 'category']))
        ]
        for title, content in sections:
            print(f"{title}:\n", content, "\n---\n")

def percentage_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the percentage of missing values for each column in the dataframe."""
    missing_counts = df.isnull().sum()
    return pd.DataFrame({
        "missing_count": missing_counts, 
        "missing_percentage": (missing_counts / len(df)) * 100
    })

def filter_columns_by_missing_data(df: pd.DataFrame, threshold: float = 15.0) -> pd.DataFrame:
    """Drop columns with missing data beyond a given threshold."""
    missing_df = percentage_missing(df)
    columns_to_drop = missing_df[missing_df['missing_percentage'] > threshold].index
    return df.drop(columns=columns_to_drop)

def plot_object_columns(df: pd.DataFrame) -> None:
    """Plot histograms for object columns in the dataframe with fewer than 10 unique values."""
    object_cols = df.select_dtypes(include='object')
    if not object_cols.empty:
        filtered_columns = [col for col in object_cols if df[col].nunique() < 10]
        for col in filtered_columns:
            fig = px.histogram(df, x=col, title=f"Countplot for {col}")
            fig.show()

# Need to improve this function and explore if it is even needed 
def get_outliers(df: pd.DataFrame, threshold: float = 1.5, include_non_numeric: bool = False) -> Dict[str, Union[int, Tuple[int, list]]]:
    """
    Identify the outliers in each column of the dataframe.
    
    For numeric columns, outliers are values outside of (Q1 - threshold*IQR) and (Q3 + threshold*IQR).
    For non-numeric columns, outliers are categories that appear fewer than threshold times.
    
    Args:
        df (pd.DataFrame): Input dataframe.
        threshold (float): Multiplier for IQR for numeric columns, or minimum count for non-numeric columns.
        include_non_numeric (bool): Flag to include non-numeric columns for outlier detection.
        
    Returns:
        dict: Dictionary with column names as keys. Values are a tuple where the first element is the count of outliers and the second element is the list of outlier values or indices.
    """
    outliers_dict = {}
    
    # For numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64'])
    for col in numeric_cols.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        outliers_dict[col] = (len(outliers), outliers.tolist())
    
    # For non-numeric columns (if the flag is set)
    if include_non_numeric:
        non_numeric_cols = df.select_dtypes(exclude=['int64', 'float64', 'float32', 'int32'])
        for col in non_numeric_cols.columns:
            value_counts = df[col].value_counts()
            rare_values = value_counts[value_counts < threshold].index.tolist()
            if rare_values:
                outlier_indices = df[df[col].isin(rare_values)].index.tolist()
                outliers_dict[col] = (len(outlier_indices), outlier_indices)
    
    return outliers_dict

# Main preprocessing steps
if __name__ == "__main__":
    crash_data = concat_csv_from_directory(Path.cwd() / "data")
    dataframe_summary(crash_data)
    crash_data = filter_columns_by_missing_data(crash_data)
    plot_object_columns(crash_data)
    outlier_counts = get_outliers(crash_data)
    print("Outliers count per numeric column:\n", outlier_counts)
