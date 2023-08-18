from pathlib import Path
import pandas as pd
from typing import Union
import plotly.express as px


def concat_csv_from_directory(directory: Union[str, Path]) -> pd.DataFrame:
    """Concatenate CSV files from the data directory that start with "CRASH"

    Args:
        directory (Union[str, Path]): The directory path where CSV files are located

    Returns:
        pd.DataFrame: A concateated dataframe of all CSV files in the directory
    """
    path = Path(directory)
    csv_files = [f for f in path.glob('CRASH*.csv')]
    
    # Using list comprehension to read the CSV files into dataframes
    list_of_dataframes = [pd.read_csv(filename) for filename in csv_files]
    
    concatenated_dataframe = pd.concat(list_of_dataframes, ignore_index=True)
    
    return concatenated_dataframe

# Fetch crash data directly by passing the directory path to the function
crash_data = concat_csv_from_directory(Path.cwd() / "data")

def dataframe_summary(df: pd.DataFrame) -> None:
    """
    Display a summary of the given dataframe, including shape, dtypes, value counts of dtypes, 
    descriptive statistics for numerical columns, and information for non-numerical columns.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        None
    """
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # Ensure all rows and columns are displayed
        print("1. Shape of the dataframe:")
        print(df.shape)
        print("\n---\n")
        
        print("2. Comprehensive Info:")
        df.info()
        print("\n---\n")
        
        print("3. Value counts of data types:")
        print(df.dtypes.value_counts())
        print("\n---\n")
        
        print("4. Missing Values:")
        missing_counts = df.isnull().sum()
        missing_percentage = (df.isnull().sum() / df.shape[0]) * 100
        missing_df = pd.DataFrame({"Missing Count": missing_counts, "Missing Percentage (%)": missing_percentage})
        print(missing_df)
        print("\n---\n")
        
        print("5. Descriptive statistics for numerical columns:")
        print(df.describe())
        print("\n---\n")
        
        print("6. Descriptive statistics for non-numerical columns:")
        print(df.describe(include=['object', 'category']))
        print("\n---\n")
    

def plot_object_columns(df: pd.DataFrame) -> None:
    """
    Plot countplots for object columns in the dataframe that have fewer than 10 unique values.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        None
    """

    # Filter columns with object dtype and fewer than 10 unique values
    filtered_columns = [col for col in df.select_dtypes(include='object') if df[col].nunique() < 10]

    for col in filtered_columns:
        fig = px.histogram(df, x=col, title=f"Countplot for {col}")
        fig.show()

def get_outliers(df):
    '''Identify the number of outliers +/- 3 standard deviations. 
    Pass this function a dataframe and it returns a dictionary'''

    outs = {}

    df = df.select_dtypes(include=['int64'])


    for col in df.columns:

        # calculate summary statistics
        data_mean, data_std = np.mean(df[col]), np.std(df[col])

        # identify outliers
        cut_off = data_std * 3
        lower, upper = data_mean - cut_off, data_mean + cut_off

        # identify outliers
        outliers = [x for x in df[col] if x < lower or x > upper]

        outs[col] = len(outliers)

    return outs