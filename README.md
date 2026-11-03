# Nepal LandCover Explorer

An interactive geospatial web application for exploring land-cover patterns across Nepal using ESA WorldCover 2021 data.

**Live Demo:** https://charming-fairy-cae772.netlify.app/

**Source Code:** https://github.com/romasahani/nepal-landcover-explorer

## Overview

Nepal LandCover Explorer makes satellite-derived land-cover information easier to explore through an interactive web map, land-cover classification, and statistical summaries.

The project uses ESA WorldCover 2021 v200, a global land-cover dataset with an original spatial resolution of 10 metres. The raster data is processed into a Nepal-focused dataset, then converted into a downsampled preview suitable for browser-based visualization.

Amazon S3 stores and delivers the land-cover preview image and statistical CSV file to the deployed application.

## Features

- Interactive map for exploring Nepal.
- ESA WorldCover land-cover visualization.
- Color-coded land-cover classification.
- Land-cover class legend and layer controls.
- Interactive land-cover identification using cursor position.
- Geographic coordinate display.
- Land-cover area and percentage statistics.
- Zoom and map navigation controls.

## Live Application

Visit the deployed application:

**https://charming-fairy-cae772.netlify.app/**

The frontend is hosted on Netlify. Land-cover preview and statistics data are delivered from Amazon S3.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Build tool | Vite |
| Interactive mapping | Leaflet, React-Leaflet |
| Base map | OpenStreetMap |
| Land-cover dataset | ESA WorldCover 2021 v200 |
| Cloud storage and data delivery | Amazon S3 |
| Data processing | Python |
| Raster processing | Rasterio |
| Geospatial analysis | GeoPandas, NumPy |

## Dataset

### ESA WorldCover 2021 v200

- **Provider:** European Space Agency (ESA)
- **Original spatial resolution:** 10 metres
- **Product:** WorldCover 2021 v200
- **Source:** https://esa-worldcover.org/

The source raster tiles are processed to create a Nepal-focused land-cover dataset and a browser-friendly visualization.

The dataset contains land-cover classes such as tree cover, shrubland, grassland, cropland, built-up areas, bare or sparse vegetation, snow and ice, water bodies, wetlands, and mangroves.

### Data and visualization limitations

The web application displays a downsampled PNG preview rather than rendering the original 10-metre GeoTIFF directly. Therefore, the displayed preview should not be treated as a full-resolution analysis product.

The statistics represent the processed dataset and depend on the methodology used by the project's data-processing scripts.

## Architecture

1. **Data processing:** Python geospatial scripts process raster data and generate the land-cover preview and statistics CSV.
2. **Cloud storage:** Amazon S3 stores the generated preview image and statistics CSV.
3. **Frontend:** React provides the application interface, while Leaflet and React-Leaflet provide interactive mapping.
4. **Base map:** OpenStreetMap supplies the geographic base layer.
5. **Deployment:** Netlify hosts the frontend, which retrieves the required data from Amazon S3.

Amazon S3 is the AWS service currently integrated into the application. Amazon Location Service is not yet integrated.

## Getting Started

### Prerequisites

- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/romasahani/nepal-landcover-explorer.git
```

### 2. Navigate to the frontend directory

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

Open the local URL printed in your terminal, usually `http://localhost:5173`.

### 5. Create a production build

```bash
npm run build
```

The production files are generated in `frontend/dist/`.

## Project Structure

```text
nepal-landcover-explorer/
├── frontend/
│   ├── public/
│   │   └── data/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── scripts/
│   ├── create_mosaic.py
│   ├── clip_nepal.py
│   ├── create_preview.py
│   ├── calculate_statistics.py
│   ├── inspect_rasters.py
│   └── inspect_preview_source.py
├── .gitignore
└── README.md
```

The frontend retrieves its deployed data assets from Amazon S3. The local `frontend/public/data/` directory may also contain data files used during development, depending on the current repository contents.

## Future Improvements

- Integrate Amazon Location Service.
- Improve visualization using raster tiles or other scalable geospatial delivery methods.
- Add regional land-cover comparisons.
- Expand spatial querying and land-cover analysis.
- Improve data filtering and accessibility.

## Project Status

The application is publicly deployed and includes an interactive React map, ESA WorldCover visualization, land-cover statistics, and a Python raster-processing workflow.

Amazon S3 is integrated for storing and delivering the generated land-cover preview and statistics data.

## Application Preview

![Nepal LandCover Explorer application screenshot](https://github.com/user-attachments/assets/e16fdd5c-816e-4a2a-80e9-624289b714bf)

## Author

**Roma Sahani**

Computer Engineering Student  
Tribhuvan University, IOE Purwanchal Campus

GitHub: https://github.com/romasahani

## Acknowledgements

- European Space Agency for the WorldCover dataset.
- OpenStreetMap contributors for geographic map data.
- React and Leaflet open-source communities.

## Data and Licensing

This project is intended for educational and research purposes. Consult the ESA WorldCover terms and the relevant OpenStreetMap attribution and licensing requirements before redistributing data or using it in other applications.