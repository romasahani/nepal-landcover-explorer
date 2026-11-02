from pathlib import Path
import csv
import numpy as np
import rasterio
from pyproj import Geod

RASTER_PATH = Path("data/processed/nepal_worldcover_clipped.tif")
OUTPUT_PATH = Path("data/processed/landcover_statistics.csv")

CLASSES = {
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
}

geod = Geod(ellps="WGS84")

with rasterio.open(RASTER_PATH) as src:
    if src.crs.to_epsg() != 4326:
        raise ValueError("Expected raster CRS EPSG:4326")

    print("Raster:", RASTER_PATH)
    print("Dimensions:", src.width, "x", src.height)
    print("Processing raster blocks...")

    # Accumulate class pixel counts for each raster row.
    row_counts = np.zeros((src.height, 101), dtype=np.uint64)

    for _, window in src.block_windows(1):
        data = src.read(1, window=window)

        row_start = int(window.row_off)

        for local_row in range(data.shape[0]):
            global_row = row_start + local_row

            histogram = np.bincount(
                data[local_row].ravel().astype(np.int64),
                minlength=101
            ).astype(np.uint64)

            row_counts[global_row] += histogram[:101]

    # Calculate geodesic area of a pixel for each latitude row.
    pixel_areas = np.zeros(src.height, dtype=np.float64)

    for row in range(src.height):
        top = src.transform.f + row * src.transform.e
        bottom = top + src.transform.e
        left = src.transform.c
        right = left + src.transform.a

        area, _ = geod.polygon_area_perimeter(
            [left, right, right, left],
            [top, top, bottom, bottom]
        )

        pixel_areas[row] = abs(area)

    results = []
    total_area = 0.0

    for code, name in CLASSES.items():
        pixels_by_row = row_counts[:, code]

        pixel_count = int(pixels_by_row.sum())
        area_km2 = float(
            np.sum(pixels_by_row * pixel_areas) / 1_000_000
        )

        total_area += area_km2

        results.append({
            "class_code": code,
            "class_name": name,
            "pixels": pixel_count,
            "area_km2": area_km2,
        })

    for result in results:
        result["percentage"] = (
            result["area_km2"] / total_area * 100
            if total_area else 0
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "class_code",
                "class_name",
                "pixels",
                "area_km2",
                "percentage",
            ]
        )
        writer.writeheader()

        for result in results:
            writer.writerow({
                **result,
                "area_km2": round(result["area_km2"], 3),
                "percentage": round(result["percentage"], 3),
            })

    print("\nLAND-COVER STATISTICS")
    print("-" * 65)

    for result in sorted(
        results,
        key=lambda x: x["area_km2"],
        reverse=True
    ):
        print(
            f"{result['class_name']:<25}"
            f"{result['area_km2']:>12,.2f} km²"
            f"{result['percentage']:>9.2f}%"
        )

    print("-" * 65)
    print(f"Total mapped area: {total_area:,.2f} km²")
    print("CSV saved to:", OUTPUT_PATH)