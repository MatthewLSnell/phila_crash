# Mapping Philadelphia Motor Vehicle Crashes

This project showcases an interactive heatmap of motor vehicle crashes in Philadelphia from 2010 to 2021. Users can filter and explore data based on various criteria, such as total collisions, total injuries, motorcycle fatalities, and more. The visualization leverages the PyDeck library, and data is sourced from Pennsylvania's Department of Transportation Open Data Portal.

![Streamlit_app_cover](https://github.com/MatthewLSnell/phila_crash/blob/main/Interactive%20Heatmap%20Screenshot.png)

## Features

1. Interactive heatmap with 2D and 3D viewing options.
2. Filter data by:
   - Total Collisions
   - Total Injured
   - Total Fatalities
   - Motorcycle Fatalities
   - Pedestrian Fatalities
3. Customize the appearance of the map, including hexagon bin size and opacity.
4. Map rendered using the PyDeck library for enhanced visualization.

## Getting Started

### Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:
    ```bash
    cd <repository-name>
    ```

3. Install the required packages using:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit application using the provided command (replace with your specific command if different).

Your default web browser should open, displaying the interactive heatmap.

## Data Source

[The crash data is sourced from the Pennsylvania Department of Transporation Open Portal](https://pennshare.maps.arcgis.com/apps/webappviewer/index.html?id=8fdbf046e36e41649bbfd9d7dd7c7e7e)


## Contributing

Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is under the MIT License. See the `LICENSE` file for more details.
