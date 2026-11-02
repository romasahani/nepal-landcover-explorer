# Nepal LandCover Explorer

An interactive geospatial web application for exploring land-cover patterns across Nepal using ESA WorldCover 2021 data.

## Overview

Nepal LandCover Explorer visualizes land-cover information across Nepal through an interactive map. It combines satellite-derived land-cover data with a React-based interface to make geographic information easier to explore and understand.

The project uses ESA WorldCover 10m 2021 data as its primary source. The original raster datasets are processed, clipped to Nepal's geographic boundary, and converted into a web-friendly preview for visualization.

## Features

- Interactive map of Nepal using Leaflet.
- ESA WorldCover land-cover visualization.
- Color-coded land-cover classification.
- Land-cover class legend and filtering.
- Land-cover area statistics.
- Geographic exploration through map interaction.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Build tool | Vite |
| Interactive mapping | Leaflet, React-Leaflet |
| Geospatial data | ESA WorldCover 2021 |
| Data processing | Python |
| Raster processing | Rasterio |
| Data analysis | GeoPandas, NumPy |

## Data Source

**ESA WorldCover 2021**

- Provider: European Space Agency (ESA)
- Resolution: 10 metres
- Product: WorldCover 2021 v200

Data source: https://esa-worldcover.org/

The original raster data is processed into a Nepal-focused dataset. A downsampled PNG preview and land-cover statistics CSV are included in the frontend's public data directory.

**Note:** The web application currently displays a preview image rather than rendering the original 10-metre GeoTIFF directly.

## Project Structure

```text
nepal-landcover-explorer/
│
├── frontend/
│   ├── public/
│   │   └── data/
│   │       ├── landcover_statistics.csv
│   │       └── nepal_landcover_preview.png
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── scripts/
│   ├── create_mosaic.py
│   ├── clip_nepal.py
│   ├── create_preview.py
│   ├── calculate_statistics.py
│   ├── inspect_rasters.py
│   └── inspect_preview_source.py
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Node.js
- npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/romasahani/nepal-landcover-explorer.git
```

### 2. Navigate to the frontend

```bash
cd nepal-landcover-explorer/frontend
```

### 3. Install dependencies

```bash
npm install
```

### 4. Start the development server

```bash
npm run dev
```

Open the local URL displayed in your terminal.

### 5. Create a production build

```bash
npm run build
```

The production files will be generated in `frontend/dist/`.

## Future Improvements

- Integrate Amazon Location Service.
- Add cloud-based geospatial data storage using Amazon S3.
- Explore direct visualization of higher-resolution raster tiles.
- Add regional land-cover comparisons.
- Improve spatial querying and land-cover analysis.
- Deploy the application with a production hosting solution.

## Project Status

The React frontend, interactive map, land-cover preview, statistics, and raster-processing workflow are implemented. Cloud integration and public deployment are planned improvements.

## Author

**Roma Sahani**

Computer Engineering Student  
Tribhuvan University, IOE Purwanchal Campus

GitHub: https://github.com/romasahani

## Acknowledgements

- European Space Agency (ESA) for the WorldCover dataset.
- OpenStreetMap contributors for map data.
- React and Leaflet open-source communities.

## License

This project is intended for educational and research purposes. Please refer to the ESA WorldCover data terms when using or redistributing the dataset.
