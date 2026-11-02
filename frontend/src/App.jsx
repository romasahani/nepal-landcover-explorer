import { useEffect, useRef, useState } from "react";

import {
  MapContainer,
  TileLayer,
  ImageOverlay,
  useMap,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "./App.css";

const S3_PREVIEW_URL =
  "https://nepal-landcover-explorer-2026-roma.s3.ap-south-1.amazonaws.com/data/nepal_landcover_preview.png";

const S3_STATISTICS_URL =
  "https://nepal-landcover-explorer-2026-roma.s3.ap-south-1.amazonaws.com/data/landcover_statistics.csv";

const landCoverBounds = [
  [26.34375, 80.03025],
  [30.416916666666665, 88.16908333333333],
];

const classColors = {
  10: "#006400",
  20: "#FFBB22",
  30: "#FFFF4C",
  40: "#F096FF",
  50: "#FA0000",
  60: "#B4B4B4",
  70: "#F0F0F0",
  80: "#0064C8",
  90: "#0096A0",
  95: "#00CF75",
  100: "#FAE6A0",
};

function NepalView() {
  const map = useMap();

  return (
    <button
      className="reset-button"
      onClick={() => map.setView([28.25, 84.0], 7)}
    >
      Reset Nepal View
    </button>
  );
}

// Hover information component 
function LandCoverHover({ onHover }) {
  const imageRef = useRef(null);
  const canvasRef = useRef(null);

  const classNames = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare / sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    95: "Mangroves",
    100: "Moss and lichen",
  };

  useEffect(() => {
    const image = new Image();

    image.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = image.width;
      canvas.height = image.height;

      const context = canvas.getContext("2d", {
        willReadFrequently: true,
      });

      context.drawImage(image, 0, 0);
      imageRef.current = image;
      canvasRef.current = context;
    };

    image.onerror = () => {
      console.error("Could not load land-cover preview.");
    };

    image.crossOrigin = "anonymous";
    image.src = S3_PREVIEW_URL;

    return () => {
      imageRef.current = null;
      canvasRef.current = null;
    };
  }, []);

  useMapEvents({
    mousemove(event) {
      const image = imageRef.current;
      const context = canvasRef.current;

      if (!image || !context) return;

      const [south, west] = landCoverBounds[0];
      const [north, east] = landCoverBounds[1];

      const { lat, lng } = event.latlng;

      if (lat < south || lat > north || lng < west || lng > east) {
        onHover(null);
        return;
      }

      const x = Math.min(
        image.width - 1,
        Math.floor(((lng - west) / (east - west)) * image.width)
      );

      const y = Math.min(
        image.height - 1,
        Math.floor(((north - lat) / (north - south)) * image.height)
      );

      const pixel = context.getImageData(x, y, 1, 1).data;

      if (pixel[3] === 0) {
        onHover(null);
        return;
      }

      const color =
        "#" +
        [pixel[0], pixel[1], pixel[2]]
          .map((value) => value.toString(16).padStart(2, "0"))
          .join("")
          .toUpperCase();

      const classCode = Object.keys(classColors).find(
        (code) => classColors[code].toUpperCase() === color
      );

      onHover({
        className: classNames[classCode] || "No data",
        lat: lat.toFixed(5),
        lng: lng.toFixed(5),
      });
    },

    mouseout() {
      onHover(null);
    },
  });

  return null;
}


export default function App() {
  const [showBaseMap, setShowBaseMap] = useState(true);
  const [showLandCover, setShowLandCover] = useState(true);
  const [statistics, setStatistics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
   const [hoverInfo, setHoverInfo] = useState(null); 

  useEffect(() => {
    fetch(S3_STATISTICS_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not load land-cover statistics.");
        }
        return response.text();
      })
      .then((csv) => {
        const lines = csv.trim().split("\n");
        const rows = lines.slice(1).map((line) => {
          const [class_code, class_name, pixels, area_km2, percentage] =
            line.split(",");

          return {
            class_code: Number(class_code),
            class_name,
            pixels: Number(pixels),
            area_km2: Number(area_km2),
            percentage: Number(percentage),
          };
        });

        setStatistics(rows);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const totalArea = statistics.reduce(
    (sum, item) => sum + item.area_km2,
    0
  );

  const getClass = (name) =>
    statistics.find((item) => item.class_name === name);

  const formatArea = (value) =>
    value?.toLocaleString("en-US", {
      maximumFractionDigits: 2,
    }) ?? "—";

  return (
    <main className="app">
      <header className="header">
        <div>
          <p className="eyebrow">GEOSPATIAL EXPLORER</p>
          <h1>Nepal LandCover Explorer</h1>
          <p className="subtitle">
            Explore forests, croplands, water bodies, and settlements across Nepal.
          </p>
        </div>
      </header>

      <section className="workspace">
        <aside className="sidebar">
          <h2>Map layers</h2>

          <label className="layer-option">
            <input
              type="checkbox"
              checked={showBaseMap}
              onChange={(event) => setShowBaseMap(event.target.checked)}
            />
            OpenStreetMap base layer
          </label>

          <label className="layer-option">
            <input
              type="checkbox"
              checked={showLandCover}
              onChange={(event) => setShowLandCover(event.target.checked)}
            />
            ESA WorldCover 2021
          </label>

          <div className="statistics-section">
            <h2>Land-cover statistics</h2>

            {loading && <p>Loading statistics...</p>}
            {error && <p className="error-message">{error}</p>}

            {!loading && !error && (
              <>
                <div className="total-stat">
                  <span>Total mapped area</span>
                  <strong>{formatArea(totalArea)} km²</strong>
                </div>

                <div className="stats-grid">
                  <div className="stat-card">
                    <span>Tree cover</span>
                    <strong>
                      {getClass("Tree cover")?.percentage.toFixed(2)}%
                    </strong>
                  </div>

                  <div className="stat-card">
                    <span>Cropland</span>
                    <strong>
                      {getClass("Cropland")?.percentage.toFixed(2)}%
                    </strong>
                  </div>

                  <div className="stat-card">
                    <span>Built-up</span>
                    <strong>
                      {getClass("Built-up")?.percentage.toFixed(2)}%
                    </strong>
                  </div>

                  <div className="stat-card">
                    <span>Grassland</span>
                    <strong>
                      {getClass("Grassland")?.percentage.toFixed(2)}%
                    </strong>
                  </div>
                </div>

                <h2 className="breakdown-heading">Class breakdown</h2>

                {statistics.map((item) => (
                  <div className="stat-row" key={item.class_code}>
                    <div className="stat-row-heading">
                      <span
                        className="legend-swatch"
                        style={{
                          backgroundColor: classColors[item.class_code],
                        }}
                      />
                      <span className="stat-name">{item.class_name}</span>
                      <strong>{item.percentage.toFixed(2)}%</strong>
                    </div>

                    <div className="stat-track">
                      <div
                        className="stat-fill"
                        style={{
                          width: `${item.percentage}%`,
                          backgroundColor: classColors[item.class_code],
                        }}
                      />
                    </div>

                    <span className="stat-area">
                      {formatArea(item.area_km2)} km²
                    </span>
                  </div>
                ))}
              </>
            )}
          </div>

          <div className="notice">
            <strong>Dataset information</strong>
            <p>
              ESA WorldCover 2021, version 200. Original classification
              resolution: 10 m. The browser preview is downsampled.
            </p>
          </div>

          <h2>About this project</h2>
          <p className="description">
            An interactive geographic explorer for understanding Nepal's
            land cover using satellite-derived data.
          </p>
        </aside>

        <section className="map-panel" aria-label="Interactive map of Nepal">
          <MapContainer
            center={[28.25, 84.0]}
            zoom={7}
            minZoom={5}
            maxZoom={16}
            scrollWheelZoom
            className="map"
          >
            {showBaseMap && (
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
            )}

            {showLandCover && (
             <ImageOverlay
               url={S3_PREVIEW_URL}
               bounds={landCoverBounds}
               opacity={0.78}
               attribution="ESA WorldCover 2021"
               crossOrigin="anonymous"
             />
            )}

            <NepalView />
           
            {showLandCover && (
             <LandCoverHover onHover={setHoverInfo} />
           )}
          </MapContainer>

          {showLandCover && (
            <div className="map-info-panel">
              <strong>Land Cover Information</strong>

              {hoverInfo ? (
                <>
                  <h3>{hoverInfo.className}</h3>
                  <p>ESA WorldCover 2021</p>
                  <span>Latitude: {hoverInfo.lat}</span>
                  <br />
                  <span>Longitude: {hoverInfo.lng}</span>
                </>
              ) : (
                <p>Move your cursor over the colored land-cover map.</p>
              )}
            </div>
          )}

        </section>
      </section>

      <footer>
          Data: ESA WorldCover 2021, Version 200.
  © ESA WorldCover project 2021 / Contains modified Copernicus
  Sentinel data (2021) processed by ESA WorldCover consortium.
  Statistics are estimates calculated from the clipped raster
  using geodesic pixel areas and a generalized Nepal boundary.
  The displayed map preview is downsampled from the original
  10 m classification data.
      </footer>
    </main>
  );
}
