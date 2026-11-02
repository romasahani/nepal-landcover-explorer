from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from PIL import Image

INPUT = Path("data/processed/nepal_worldcover_clipped.tif")
OUTPUT = Path("frontend/public/data/nepal_landcover_preview.png")

# ESA WorldCover class colors
COLORS = {
    10: (0, 100, 0),       # Tree cover
    20: (255, 187, 34),    # Shrubland
    30: (255, 255, 76),    # Grassland
    40: (240, 150, 255),   # Cropland
    50: (250, 0, 0),       # Built-up
    60: (180, 180, 180),   # Bare / sparse vegetation
    70: (240, 240, 240),   # Snow and ice
    80: (0, 100, 200),     # Water
    90: (0, 150, 160),     # Herbaceous wetland
    95: (0, 207, 117),     # Mangroves
    100: (250, 230, 160),  # Moss and lichen
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with rasterio.open(INPUT) as src:
    scale = 16
    height = src.height // scale
    width = src.width // scale

    print(f"Creating preview: {width} x {height}")

    data = src.read(
        1,
        out_shape=(height, width),
        resampling=Resampling.nearest
    )

    rgba = np.zeros((height, width, 4), dtype=np.uint8)

    for code, color in COLORS.items():
        mask = data == code
        rgba[mask, :3] = color
        rgba[mask, 3] = 255

    image = Image.fromarray(rgba, mode="RGBA")
    image.save(OUTPUT, optimize=True)

    print("Preview created:", OUTPUT)
    print("Geographic bounds:", src.bounds)
    print("Image dimensions:", image.size)
    print("File size:", round(OUTPUT.stat().st_size / 1024, 2), "KB")