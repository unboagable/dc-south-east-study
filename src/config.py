"""Configuration constants for the DC South East Study project."""
from pathlib import Path
from typing import List

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Shapefile paths
SHAPEFILE_DIR = RAW_DATA_DIR / "shapefiles"
TRACT_SHAPEFILE = SHAPEFILE_DIR / "tl_2024_11_tract" / "tl_2024_11_tract.shp"
BLOCK_GROUP_SHAPEFILE = SHAPEFILE_DIR / "tl_2024_11_bg" / "tl_2024_11_bg.shp"

# Output paths
OUTPUT_SHAPEFILE_DIR = PROCESSED_DATA_DIR / "shapefiles" / "track"
OUTPUT_SHAPEFILE = OUTPUT_SHAPEFILE_DIR / "merged_shapefile.shp"

# API configuration
EJScreen_API_URL = "https://ejscreen.epa.gov/mapper/ejscreenRESTbroker1.aspx"
API_REQUEST_DELAY = 1  # seconds between API requests

# Block group IDs for southeast of Anacostia
BLOCK_GROUPS_ANACOSTIA: List[str] = [
    "110010074011",
    "110010074012",
    "110010074021",
    "110010074022",
    "110010075011",
    "110010075012",
    "110010075021",
    "110010075022",
    "110010076011",
    "110010076012",
    "110010076021",
    "110010076022",
    "110010077011",
    "110010077012",
    "110010077021",
    "110010077022",
    "110010078011",
    "110010078012",
    "110010078021",
    "110010078022",
    "110010079011",
    "110010079012",
    "110010079021",
    "110010079022",
    "110010080011",
    "110010080012",
    "110010080021",
    "110010080022",
    "110010081011",
    "110010081012",
    "110010081021",
    "110010081022",
    "110010082011",
    "110010082012",
    "110010082021",
    "110010082022",
]

# DC city configuration
DC_CITY_NAME = "Washington"
DC_AREA_ID = "1150000"

