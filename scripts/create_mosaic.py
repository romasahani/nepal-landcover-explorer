from pathlib import Path
import rasterio
from rasterio.merge import merge

DATA_DIR = Path("data/raw/worldcover")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(DATA_DIR.glob("*.tif"))

if len(files) != 8:
    raise RuntimeError(f"Expected 8 tiles, found {len(files)}")

print(f"Opening {len(files)} raster tiles...")

sources = [rasterio.open(file) for file in files]

try:
    print("Creating mosaic...")

    mosaic, transform = merge(
        sources,
        nodata=0,
        dtype="uint8"
    )

    output_file = OUTPUT_DIR / "nepal_worldcover_mosaic.tif"

    profile = sources[0].profile.copy()
    profile.update(
        driver="GTiff",
        height=mosaic.shape[1],
        width=mosaic.shape[2],
        transform=transform,
        count=1,
        dtype="uint8",
        nodata=0,
        compress="LZW",
        tiled=True,
        BIGTIFF="IF_SAFER"
    )

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(mosaic)

    print("\nMosaic created successfully!")
    print("Output:", output_file)
    print("Dimensions:", mosaic.shape[2], "x", mosaic.shape[1])
    print("Bounds:", rasterio.transform.array_bounds(
        mosaic.shape[1], mosaic.shape[2], transform
    ))

finally:
    for src in sources:
        src.close()