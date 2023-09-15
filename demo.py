from json import tool
import pydeck as pdk
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv
import streamlit as st 

load_dotenv() 

map_box_api_key = os.environ.get("phila_crash_map_api_key")

    # Define the dataframe column to be considered based on filter_option
column_mappings = {
        'Total Collisions': 'CRN',
        'Total Injured': 'INJURY_COUNT',
        'Total Fatalities': 'FATAL_COUNT',
        'Motorcycle Fatalities': 'MCYCLE_DEATH_COUNT',
        'Pedestrian Fatalities': 'PED_DEATH_COUNT'
    }




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
    [252, 255, 164]
]

def render_map(df, mode='3D', zoom=9, tooltip_title='', filename='demo.html'):
    # 1. Color Scheme 
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
    [252, 255, 164]
]

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
                "color": [255, 255, 255]
            }
        ]
    }
    
    
    # Determine elevation range based on mode 
    elevation_range = [0, 150] if mode == '3D' else [0, 0]
    pitch_value = 40.5 if mode == '3D' else 10

    # Define a layer to display on a map
    layer = pdk.Layer(
        'HexagonLayer',
        df,
        get_position=['DEC_LONG', 'DEC_LAT'],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=elevation_range,
        extruded=True,
        coverage=1,
        radius=300,
        opacity=0.4,
        color_range=color_scheme,
        material={"ambientColor": [255, 255, 255], "shininess": 50, "lightSettings": lighting_effects}
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-75.1652,
        latitude=39.9526,
        zoom=zoom,
        min_zoom=5,
        max_zoom=15,
        pitch=pitch_value,
        bearing=-27.36
    )

    # Tooltip
    tooltip = {
        "html": f"<b>{tooltip_title} :</b> {{elevationValue}}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    
    
    

    # Render
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_provider='mapbox',
        map_style='mapbox://styles/mapbox/dark-v10',
        api_keys={'mapbox': map_box_api_key},
        tooltip=tooltip
    )

    return r

def main():
    st.title("Philadelphia Crash Map")
    
    df = pd.read_csv('data\PROCESSED_DATA\crash_data.csv')
    print(f"Initial data shape: {df.shape}")
    
    # Add a selectbox (dropdown) for users to select a data filter
    filter_option = st.selectbox(
        'Filter Data By:',
        (
            'Total Collisions',
            'Total Injured',
            'Total Fatalities',
            'Motorcycle Fatalities',
            'Pedestrian Fatalities'
        )
    )
    
    # Add mappings for tooltip_title based on filter_option
    tooltip_titles = {
        'Total Collisions': 'Total Collisions',
        'Total Injured': 'Total Injured',
        'Total Fatalities': 'Total Fatalities',
        'Motorcycle Fatalities': 'Motorcycle Fatalities',
        'Pedestrian Fatalities': 'Pedestrian Fatalities'
    }
    
    tooltip_title = tooltip_titles[filter_option] 
    
    if filter_option == 'Total Collisions':
        df = df.loc[(df['CRN'] > 0)]
        
    elif filter_option == 'Total Injured':
        df = df.loc[(df['INJURY_COUNT'] > 0)]
        
    elif filter_option == 'Total Fatalities':
        df = df.loc[(df['FATAL_COUNT'] > 0)]
        
    elif filter_option == 'Motorcycle Fatalities':
        df = df.loc[(df['MCYCLE_DEATH_COUNT'] > 0)]
        
    elif filter_option == 'Pedestrian Fatalities':
        df = df.loc[(df['PED_DEATH_COUNT'] > 0)]
        
    print(f"Filtered data shape for {filter_option}: {df.shape}")
    print(f"Max value for {filter_option}: {df[column_mappings[filter_option]].max()}")
    
    df = df.dropna(subset=['DEC_LONG', 'DEC_LAT']) 
    
    mode_option = st.selectbox('Select Mode:', ('2D', '3D'))
    
    map_deck = render_map(df, mode=mode_option, zoom=9.75, tooltip_title=tooltip_title)
    
    st.pydeck_chart(map_deck)
    
if __name__ == '__main__':
    main()
