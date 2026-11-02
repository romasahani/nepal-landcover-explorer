from pathlib import Path
import rasterio
from PIL import Image

raster_path = Path("data/processed/nepal_worldcover_clipped.tif")
preview_path = Path("frontend/public/data/nepal_landcover_preview.png")

with rasterio.open(raster_path) as src:
    print("=== CLIPPED RASTER ===")
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Dimensions:", src.width, "x", src.height)
    print("Resolution:", src.res)
    print("Transform:", src.transform)
    print("NoData:", src.nodata)

with Image.open(preview_path) as image:
    print("\n=== PREVIEW PNG ===")
    print("Dimensions:", image.size)
    print("Mode:", image.mode)
