from pathlib import Path
import rasterio

DATA_DIR = Path.home() / "Documents/nepal-landcover-explorer/data/raw/worldcover"
files = sorted(DATA_DIR.glob("*.tif"))

print(f"Found {len(files)} GeoTIFF files\n")

if len(files) != 8:
    print("WARNING: Expected 8 tiles.")

reference = None
valid = True

for file in files:
    print(f"\n--- {file.name} ---")

    with rasterio.open(file) as src:
        metadata = (
            src.crs,
            src.width,
            src.height,
            src.res,
            src.count,
            src.dtypes
        )

        if reference is None:
            reference = metadata
        elif metadata != reference:
            valid = False
            print("WARNING: Metadata differs from other tiles.")

        print(f"CRS:        {src.crs}")
        print(f"Dimensions: {src.width} x {src.height}")
        print(f"Resolution: {src.res}")
        print(f"Bounds:     {src.bounds}")
        print(f"Data type:  {src.dtypes[0]}")
        print(f"NoData:     {src.nodata}")
        print(f"Bands:      {src.count}")

print("\nValidation:", "PASS" if valid and len(files) == 8 else "CHECK REQUIRED")