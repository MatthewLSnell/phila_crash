# Mapping Philadelphia Motor Vehicle Crashes

This project showcases an interactive heatmap of motor vehicle crashes in Philadelphia from 2010 to 2021. Users can filter and explore data based on various criteria, such as total collisions, total injuries, motorcycle fatalities, and more. The visualization leverages the PyDeck library, and data is sourced from the City of Philadelphia's Open Data Portal.

![Sample Image](sample_image.png)  <!-- Include a screenshot of the heatmap for better visualization -->

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

### Prerequisites

1. Python 3.x
2. Streamlit
3. PyDeck
4. Pandas
5. dotenv

You can install the required libraries using:

\```bash
pip install streamlit pydeck pandas python-dotenv
\```

### Setting up

1. Clone the repository:

\```bash
git clone <repository-link>
\```

2. Navigate to the project directory:

\```bash
cd <directory-name>
\```

3. Create a `.env` file in the root directory and add your Mapbox API key:

\```
phila_crash_map_api_key=YOUR_MAPBOX_API_KEY
\```

### Running the App

From the project directory, run:

\```bash
streamlit run <script-name>.py
\```

Your default web browser should open, displaying the interactive heatmap.

## Data Source

The crash data is sourced from the City of Philadelphia's Open Data Portal.

## Contributing

Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is under the MIT License. See the `LICENSE` file for more details.
