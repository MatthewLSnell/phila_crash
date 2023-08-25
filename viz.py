# Imports
from pathlib import Path
import pandas as pd
from typing import Union
import pydeck as pdk

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

# Columns to visualize
columns_to_visualize = ["FATAL_COUNT", "INJURY_COUNT", "MCYCLE_DEATH_COUNT", "PED_DEATH_COUNT"]


# Set a default metric for visualization, e.g., FATAL_COUNT
metric = "FATAL_COUNT"

layer = pdk.Layer(
    'HexagonLayer',
    crash_data,
    get_position=['DEC_LONG', 'DEC_LAT'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    extruded=True,
    coverage=1,
    elevation_range=[0, 5000],
    get_elevation=metric,
    get_fill_color='[255, (1-elevationValue/5000)*255, 0]'
)

view_state = pdk.ViewState(
    longitude=-75.1652,
    latitude=39.9526,
    zoom=10,
    pitch=40.5
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html('demo.html')