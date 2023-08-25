import pydeck as pdk
import pandas as pd

# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                     'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')

df = pd.read_csv(UK_ACCIDENTS_DATA)

# 1. Color Scheme
color_scheme = [
    [1, 152, 189, 255],
    [73, 227, 206, 255],
    [216, 254, 181, 255],
    [254, 237, 177, 255],
    [254, 173, 84, 255],
    [209, 55, 78, 255]
]

# 4. Lighting Effects
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
    get_position=['lng', 'lat'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,                 
    coverage=1,
    # 2. Hexagon Radius
    radius=500, #aadjust as needed
    # 3. Opacity 
    opacity=0.8, # adjust as needed
    # 1. Color Scheme
    color_range=color_scheme,
    # 4. Lighting Effects 
    material={"ambientColor": [255, 255, 255], "shininess": 50, "shininess": 10, "lightSettings": lighting_effects}
    )

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
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
    map_style=pdk.map_styles.LIGHT,
    # 6. Tooltip
    tooltip=tooltip
)
r.to_html('demo.html')