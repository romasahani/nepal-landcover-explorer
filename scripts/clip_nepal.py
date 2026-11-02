from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask

RASTER_PATH = Path("data/processed/nepal_worldcover_mosaic.tif")
BOUNDARY_PATH = Path("data/boundaries/ne_10m_admin_0_countries.shp")
OUTPUT_PATH = Path("data/processed/nepal_worldcover_clipped.tif")

print("Loading Nepal boundary...")

countries = gpd.read_file(BOUNDARY_PATH)
nepal = countries[countries["ADMIN"] == "Nepal"]

if nepal.empty:
    raise RuntimeError("Nepal boundary not found.")

print("Nepal boundary found.")

with rasterio.open(RASTER_PATH) as src:

    nepal = nepal.to_crs(src.crs)

    geometries = [
        geometry.__geo_interface__
        for geometry in nepal.geometry
    ]

    print("Clipping raster to Nepal...")

    clipped, transform = mask(
        src,
        geometries,
        crop=True,
        nodata=0
    )

    profile = src.profile.copy()

    profile.update(
        height=clipped.shape[1],
        width=clipped.shape[2],
        transform=transform,
        nodata=0,
        compress="LZW",
        tiled=True,
        BIGTIFF="IF_SAFER"
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(OUTPUT_PATH, "w", **profile) as dst:
        dst.write(clipped)

print("\nClipping completed!")
print("Output:", OUTPUT_PATH)
print("Dimensions:", clipped.shape[2], "x", clipped.shape[1])
print("File size:", round(OUTPUT_PATH.stat().st_size / (1024 * 1024), 2), "MB")