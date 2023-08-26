# Imports
from pathlib import Path
import pandas as pd
from typing import Union
import pydeck as pdk

# An array defining a series of colors, which are RGBA values 
COLOR_RANGE = [
    [0, 0, 4, 223],
    [20, 11, 53, 239],
    [58, 9, 99],
    [96, 19, 110],
    [133, 33, 107],
    [169, 46, 94],
    [203, 65, 73],
    [230, 93, 47],
    [247, 131, 17],
    [252, 173, 18],
    [245, 219, 75],
    [252, 255, 164]
]

# Specifies the configuaration of the light settings
LIGHT_SETTINGS = {
    'lightsPosition': [-74.08, 40.8, 8000, -73.5, 41, 8000],
    'ambientRatio': 0.8,
    'diffuseRatio': 0.6,
    'specularRatio': 0.8,
    'lightsStrength': [1, 0, 1, 0],
    'numberOfLights': 2
}

# Assuming we have some values for these (you can change them as needed)
color_variable = 'INJURY_COUNT'  # Example, you can modify as per your use-case
current_mode = '2d'  # Or '2d' based on user input or other logic
radius = 300  # This is just an example value

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

def hex_intensity_calculator(color_variable):
    """Returns a function that calculates the intensity of a hexagon based on the color variable"""
    if color_variable == 'collisions':
        return lambda points: len(points)
    else:
        return lambda points: sum(p.get(color_variable, 0) for p in points)

def render_layer(color_variable, current_mode, radius):
    """Returns a dictionary of layer configurations based on the color variable, current mode and radius"""
    options = {
        'extruded': current_mode == '3d',
        'opacity': 0.4 if current_mode == '3d' else 0.3,
        'coverage': 0.9 if current_mode == '3d' else 1,
        'radius': float(radius)
    }
    return options

# Use the render_layer function to get layer configurations
layer_config = render_layer(color_variable, current_mode, radius)

# Use hex_intensity_calculator function for getting elevation value
elevation_calculator = hex_intensity_calculator(color_variable)

# This sets the map to Carto's Dark Matter style.
CARTO_DARK_MATTER_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"

# Modify layer configurations
layer = pdk.Layer(
    'HexagonLayer',
    crash_data,
    map_style=CARTO_DARK_MATTER_STYLE,  # Use Carto's Dark Matter style
    get_position=['DEC_LONG', 'DEC_LAT'],
    auto_highlight=True,
    pickable=True,
    coverage=layer_config['coverage'],
    radius=layer_config['radius'],
    elevation_scale=25,
    extruded=layer_config['extruded'],
    elevation_range=[0, 250],
    get_elevation=lambda row: elevation_calculator([row]),  # Use the elevation calculator here
    get_fill_color='[180, 0, 200, 140]',  # This can be modified as required
    color_range=COLOR_RANGE,
    opacity=layer_config['opacity'],
    light_settings=LIGHT_SETTINGS,  # Incorporate the light settings
    tooltip={
        "text": "Injury Count: {INJURY_COUNT}\nFatal Count: {FATAL_COUNT}\nMotorcycle Death Count: {MCYCLE_DEATH_COUNT}\nBicycle Death Count: {BICYCLE_DEATH_COUNT}\nPedestrian Death Count: {PED_DEATH_COUNT}"
    }
)

view_state = pdk.ViewState(
    longitude=-75.1652,
    latitude=39.9526,
    zoom=10.9,
    bearing=0,
    pitch=10
    # pitch=40.5
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style='light')
r.to_html('demo.html')


