import pydeck as pdk
import pandas as pd

df = pd.read_csv('data\PROCESSED_DATA\crash_data.csv')

df = df.loc[(df['CRN'] > 0)]

# 1. Color Scheme 
color_scheme = [
    [1, 152, 189, 255],
    [73, 227, 206, 255],
    [216, 254, 181, 255],
    [254, 237, 177, 255],
    [254, 173, 84, 255],
    [209, 55, 78, 255]
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

# Define a layer to display on a map
layer = pdk.Layer(
    'HexagonLayer',
    df,
    get_position=['DEC_LONG', 'DEC_LAT'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 150],
    extruded=True,                 
    coverage=1,
    # 2. Hexagon Radius
    radius=500, #aadjust as needed
    # 3. Opacity 
    opacity=0.4, # adjust as needed
    # 1. Color Scheme
    color_range=color_scheme,
    # 4. Lighting Effects 
    material={"ambientColor": [255, 255, 255], "shininess": 50, "lightSettings": lighting_effects}
    )

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-75.1652,
    latitude=39.9526,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)


# 6. Tooltip
tooltip = {
    "html": "<b>Elevation Value :</b> {elevationValue}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Render
r = pdk.Deck(
    layers=[layer], 
    initial_view_state=view_state,
    # 5. Map Styles
    map_style=pdk.map_styles.CARTO_DARK,
    # 6. Tooltip
    tooltip=tooltip
)
r.to_html('demo.html')
