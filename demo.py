from json import tool
import pydeck as pdk
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv
import streamlit as st 
import jinja2
import matplotlib.pyplot as plt

# Set the page to wide format
st.set_page_config(layout="wide")

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

def create_legend_html(labels: list) -> str:
    """Creates an HTML legend from a list dictionary of the format {'text': str, 'color': [r, g, b]}"""
    labels = list(labels)
    for label in labels:
        assert label['color'] and label['text']
        assert len(label['color']) in (3, 4)
        label['color'] = ', '.join([str(c) for c in label['color']])
    
    legend_template = jinja2.Template('''
    <style>
      .legend {
        width: 300px;
        display: flex;
        align-items: center;
      }
      .square {
        height: 10px;
        width: 10px;
        border: 1px solid grey;
        margin-right: 8px;
      }
    </style>
    <h2>Legend</h2>
    {% for label in labels %}
    <div class='legend'>
      <div class="square" style="background:rgba({{ label['color'] }})"></div>
      <span>{{label['text']}}</span>
    </div>
    {% endfor %}
    <br />
    ''')
    
    return legend_template.render(labels=labels)

# def generate_legend_labels(df, filter_option):
#     # Define the dataframe column to be considered based on filter_option
#     column_mappings = {
#         'Total Collisions': 'CRN',
#         'Total Injured': 'INJURY_COUNT',
#         'Total Fatalities': 'FATAL_COUNT',
#         'Motorcycle Fatalities': 'MCYCLE_DEATH_COUNT',
#         'Pedestrian Fatalities': 'PED_DEATH_COUNT'
#     }

#     column_to_consider = column_mappings[filter_option]

#     # Calculate quantiles
#     min_val = df[column_to_consider].min()
#     max_val = df[column_to_consider].max()
    
#     # Calculate bin edges based on the number of colors in the scheme
#     bin_edges = np.linspace(min_val, max_val, len(color_scheme) + 1)
    
#     labels = []
#     min_val = df[column_to_consider].min()
#     for i in range(len(bin_edges) - 1):
#         labels.append({
#             "text": f"{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}",
#             "color": color_scheme[i]
#         })

#     return labels

def generate_legend_labels(min_agg_val, max_agg_val):
    # Calculate bin edges based on the number of colors in the scheme
    bin_edges = np.linspace(min_agg_val, max_agg_val, len(color_scheme) + 1)
    
    labels = []
    for i in range(len(bin_edges) - 1):
        print(f"Bin edge {i}: {bin_edges[i]:.2f}")
        labels.append({
            "text": f"{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}",
            "color": color_scheme[i]
        })
        
    return labels

def calculate_hexbin_aggregates(df, radius, filter_option):
    # Convert latitude and longitude to meters 
    # Using an approximation: 1 degree is around 111km
    df['x_m'] = df['DEC_LONG'] * 111000 * np.cos(df['DEC_LAT'])
    df['y_m'] = df['DEC_LAT'] * 111000

    if filter_option == 'Total Collisions':
        # For counting, set C to an array of ones.
        C_values = np.ones(len(df))
    else:
        C_values = df[column_mappings[filter_option]]
    
    # Calculate hexbin
    hb = plt.hexbin(df['x_m'], df['y_m'], gridsize=radius, reduce_C_function=np.sum, C=C_values)
    
    # Close the matplotlib plot window, as we only need the data
    plt.close()  
    
    min_agg_val, max_agg_val = hb.get_array().min(), hb.get_array().max()
    print(f"Min aggregated value: {min_agg_val}")
    print(f"Max aggregated value: {max_agg_val}")

    # Get min and max bin count values
    min_agg_val, max_agg_val = hb.get_array().min(), hb.get_array().max()

    return min_agg_val, max_agg_val



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

def render_map(df, mode='3D', zoom=9, tooltip_title='', radius=500, filename='demo.html'):
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
    # pitch_value = 40.5 if mode == '3D' else 10
    pitch_value = 60 if mode == '3D' else 10

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
        radius=radius,
        opacity=0.4,
        color_range=color_scheme,
        material={"ambientColor": [255, 255, 255], "shininess": 50, "lightSettings": lighting_effects}
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-75.1252,
        latitude=39.9926,
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
            # "backgroundColor": "steelblue",
            "backgroundColor": "rgba(0, 0, 0, 0.7)",  # This sets the color to a transparent black
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
    
    # Slider for selecting bin size
    bin_size_option = st.slider(
        'Select Hexagon Bin Size (in meters):',
        min_value=400,
        max_value=700,
        step=100,
        value=500  # This is the default value
    )
    

    
    map_deck = render_map(df, mode=mode_option, zoom=9.75, tooltip_title=tooltip_title, radius=bin_size_option)
    
    # Generate and display the legend dynamically
    # labels = generate_legend_labels(df, filter_option)
    min_agg_val, max_agg_val = calculate_hexbin_aggregates(df, bin_size_option, filter_option)
    print(f"Returned min aggregated value: {min_agg_val}")
    print(f"Returned max aggregated value: {max_agg_val}")
    labels = generate_legend_labels(min_agg_val, max_agg_val)
    legend_html = create_legend_html(labels)
    st.markdown(legend_html, unsafe_allow_html=True)
    
    
    st.pydeck_chart(map_deck)
    
if __name__ == '__main__':
    main()
