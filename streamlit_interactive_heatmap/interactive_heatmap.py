# Import the libraries and modules
import pydeck as pdk
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv
import streamlit as st


# Set the page to wide format
st.set_page_config(layout="wide")

# Load the environment variables
load_dotenv()

# Retrieve the mapbox API key
map_box_api_key = os.environ.get("phila_crash_map_api_key")

# Define a color scheme for the heatmap
color_scheme = [
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
    [252, 255, 164],
]


def create_color_legend():
    """Creates a color legend for the heatmap."""
    
    # Create a legend with color ranges
    legend_html = """
    <div style="position: absolute; top: 40px; right: 50px; background-color: rgba(0, 0, 0, 0.7); padding: 5px 5px 0px 5px; border-radius: 5px; z-index: 999; color: white; font-size: 0.3em;">
        <div style="display: flex; align-items: center; gap: 2px;">
    """

    for color in color_scheme:
        # Create a color block for each color in the scheme
        legend_html += f'<div style="background-color: rgba{tuple(color)}; width: 20px; height: 10px;"></div>'

    legend_html += """
        </div>
        <p style="font-size: 2.2em; margin-bottom: 0;">Low <span style="float: right;">High</span></p>
    </div>
    """
    return legend_html


def render_map(
    df: pd.DataFrame,
    mode: str ="3D",
    zoom: int =9,
    tooltip_title: str="",
    radius: int =500,
    filename: str ="interactive_heatmap.html",
    opacity_option: float = 0.3,
) -> pdk.Deck:
    """Renders the heatmap using the PyDeck library.

    Args:
        df (pd.DataFrame): Latitude and Longitude data.
        mode (str, optional): Rendering mode 2D or 3D. Defaults to "3D".
        zoom (int, optional): Initial zoom level. Defaults to 9.
        tooltip_title (str, optional): Title displayed in tooltip. Defaults to "".
        radius (int, optional): Size of hexagon bins. Defaults to 500.
        filename (str, optional): Output html filename. Defaults to "demo.html".
        opacity_option (float, optional): Opacity of hexagons. Defaults to 0.3.

    Returns:
        pdk.Deck: PyDeck Interactive Map object 
    """
    # 2 Lighting Effects
    lighting_effects = {
        "ambientRatio": 0.4,
        "diffuseRatio": 0.6,
        "specularRatio": 0.8,
        "lights": [
            {"type": "ambient", "intensity": 0.5},
            {
                "type": "directional",
                "intensity": 1.0,
                "direction": [3, 10, -5],
                "color": [255, 255, 255],
            },
        ],
    }

    # Determine elevation range based on mode
    elevation_range = [0, 150] if mode == "3D" else [0, 0]
    # pitch_value = 40.5 if mode == '3D' else 10
    pitch_value = 60 if mode == "3D" else 10

    # Define a layer to display on a map
    layer = pdk.Layer(
        "HexagonLayer",
        df,
        get_position=["DEC_LONG", "DEC_LAT"],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=elevation_range,
        extruded=True,
        coverage=1,
        radius=radius,
        opacity=opacity_option,
        color_range=color_scheme,
        material={
            "ambientColor": [255, 255, 255],
            "shininess": 50,
            "lightSettings": lighting_effects,
        },
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-75.1652,
        latitude=39.9926,
        zoom=zoom,
        min_zoom=5,
        max_zoom=15,
        pitch=pitch_value,
        bearing=-27.36,
    )

    # Tooltip
    tooltip = {
        "html": f"<b>{tooltip_title} :</b> {{elevationValue}}",
        "style": {
            "backgroundColor": "rgba(0, 0, 0, 0.7)",  # This sets the color to a transparent black
            "color": "white",
        },
    }

    # Render
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_provider="mapbox",
        map_style="mapbox://styles/mapbox/dark-v10",
        api_keys={"mapbox": map_box_api_key},
        tooltip=tooltip,
    )

    return r


@st.cache_data
def load_and_preprocess_data():
    """Loads and preprocesses the crash data."""
    df = pd.read_parquet("../data/PROCESSED_DATA/crash_data.parquet")
    df = df.dropna(subset=["DEC_LONG", "DEC_LAT"])

    return df

def about_section():
    """Displays the about section in the sidebar."""
    st.sidebar.header("About")
    about_content = """
        <style>
            .small-font {
                font-size: 0.7em;
            }
        </style>
        <div class="small-font">
            To explore the map in depth, you can:<br>
            1. Use the zoom in/out buttons.<br>
            2. Click and drag to move around.<br>
            3. Hold the SHIFT key and drag the mouse to adjust the map pitch.
        </div>
    """
    st.sidebar.markdown(about_content, unsafe_allow_html=True)


def interactive_heatmap():
    """
    Streamlit app main function for rendering the interactive heatmap. Includes options to filter
    and customize the appearance of the map.
    """

    st.markdown(
        "<h1 style='text-align: center; color: white;'>Mapping Philadelphia Motor Vehicle Crashes</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h6 style='text-align: center; color: white;'>This interactive map showcases the motor vehicle crashes that have occurred in Philadelphia from 2010 to 2021. The map is interactive and allows users to filter the data by total collisions, total injuries, total fatalities, motorcycle fatalities, and pedestrian fatalities. The map is rendered using the PyDeck library and the data is sourced from Pennsylvania's Department of Transportation.</h6>",
        unsafe_allow_html=True,
    )

    df = load_and_preprocess_data()

    # Add a selectbox (dropdown) for users to select a data filter
    st.sidebar.header("Map Filters")
    filter_option = st.sidebar.selectbox(
        "Filter Data By:",
        (
            "Total Collisions",
            "Total Injured",
            "Total Fatalities",
            "Motorcycle Fatalities",
            "Pedestrian Fatalities",
        ),
    )
    
    st.sidebar.markdown("---")  # Add separator

    # Add mappings for tooltip_title based on filter_option
    tooltip_titles = {
        "Total Collisions": "Total Collisions",
        "Total Injured": "Total Injured",
        "Total Fatalities": "Total Fatalities",
        "Motorcycle Fatalities": "Motorcycle Fatalities",
        "Pedestrian Fatalities": "Pedestrian Fatalities",
    }

    tooltip_title = tooltip_titles[filter_option]

    if filter_option == "Total Collisions":
        df = df.loc[(df["CRN"] > 0)]

    elif filter_option == "Total Injured":
        df = df.loc[(df["INJURY_COUNT"] > 0)]

    elif filter_option == "Total Fatalities":
        df = df.loc[(df["FATAL_COUNT"] > 0)]

    elif filter_option == "Motorcycle Fatalities":
        df = df.loc[(df["MCYCLE_DEATH_COUNT"] > 0)]

    elif filter_option == "Pedestrian Fatalities":
        df = df.loc[(df["PED_DEATH_COUNT"] > 0)]

    mode_option = st.sidebar.selectbox("Select Mode:", ("3D", "2D"))

    st.sidebar.header("Map Appearance")

    # Slider for selecting bin size
    bin_size_option = st.sidebar.slider(
        "Select Hexagon Bin Size (in meters):",
        min_value=100,
        max_value=1000,
        value=300,  # This sets the default value to 100
        step=100,  # This will make the slider increment by 50
    )

    opacity_option_percentage = st.sidebar.slider(
        "Select Hexagon Opacity (%):",
        min_value=30,  # minimum opacity in percentage
        max_value=100,  # maximum opacity in percentage
        value=50,  # default opacity in percentage
        step=10,  # step increment
    )

    # Convert the percentage value back to a decimal for use in the map rendering
    opacity_option_decimal = opacity_option_percentage / 100
    
    st.sidebar.markdown("---")  # Add separator
    
    about_section()

    # Display the legend here
    legend_html = create_color_legend()
    st.markdown(legend_html, unsafe_allow_html=True)

    # Render and display the map
    map_deck = render_map(
        df,
        mode=mode_option,
        zoom=9.95,
        tooltip_title=tooltip_title,
        radius=bin_size_option,
        opacity_option=opacity_option_decimal,
    )
    st.pydeck_chart(map_deck)


if __name__ == "__main__":
    # Displays the loading spiner and then runs the main streamlit app function
    with st.spinner("Map Loading..."):
        interactive_heatmap()
