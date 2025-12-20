"""Merge EJScreen data with TIGER/Line shapefiles for spatial analysis."""
import sys
from pathlib import Path
from typing import Optional

import geopandas as gpd
import pandas as pd

from config import (
    OUTPUT_SHAPEFILE,
    OUTPUT_SHAPEFILE_DIR,
    PROCESSED_DATA_DIR,
    TRACT_SHAPEFILE,
)


def merge_data_with_shapefile(
    shapefile_path: Path,
    data_path: Path,
    output_path: Path,
    geoid_column: str = "GEOID",
    data_id_column: str = "ID",
) -> gpd.GeoDataFrame:
    """Merge CSV data with a shapefile based on geographic identifiers.
    
    Args:
        shapefile_path: Path to TIGER/Line shapefile
        data_path: Path to CSV data file
        output_path: Path to save merged shapefile
        geoid_column: Column name in shapefile for geographic ID
        data_id_column: Column name in CSV for geographic ID
        
    Returns:
        Merged GeoDataFrame
        
    Raises:
        FileNotFoundError: If input files don't exist
        ValueError: If merge fails
    """
    if not shapefile_path.exists():
        raise FileNotFoundError(f"Shapefile not found: {shapefile_path}")
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    # Load TIGER/Line shapefile
    print(f"Loading shapefile from: {shapefile_path}")
    tracts_gdf = gpd.read_file(shapefile_path)
    
    # Load dataset
    print(f"Loading data from: {data_path}")
    data_df = pd.read_csv(data_path)
    
    # Convert GEOID to string for joining
    # Remove ".0" suffix if present (from float conversion)
    data_df[data_id_column] = data_df[data_id_column].astype(str).str.split(".").str[0]
    tracts_gdf[geoid_column] = tracts_gdf[geoid_column].astype(str)
    
    # Merge the shapefile and data
    print("Merging shapefile with data...")
    merged_gdf = tracts_gdf.merge(
        data_df, left_on=geoid_column, right_on=data_id_column, how="left"
    )
    
    # Check merge success
    matched_count = merged_gdf[data_id_column].notna().sum()
    print(f"Matched {matched_count} out of {len(merged_gdf)} features")
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save merged shapefile
    print(f"Saving merged shapefile to: {output_path}")
    merged_gdf.to_file(output_path)
    
    return merged_gdf


def plot_merged_data(
    gdf: gpd.GeoDataFrame,
    column: str = "LOWINCPCT",
    cmap: str = "OrRd",
    output_file: Optional[Path] = None,
) -> None:
    """Plot merged geodataframe with specified column.
    
    Args:
        gdf: GeoDataFrame to plot
        column: Column name to visualize
        cmap: Colormap name
        output_file: Optional path to save the plot
    """
    import matplotlib.pyplot as plt
    
    if column not in gdf.columns:
        print(f"Warning: Column '{column}' not found in data", file=sys.stderr)
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    gdf.plot(column=column, cmap=cmap, legend=True, ax=ax)
    ax.set_title(f"Map of {column}")
    ax.set_axis_off()
    
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()


def main() -> None:
    """Main entry point for merging data with shapefiles."""
    # Define file paths
    shapefile_path = TRACT_SHAPEFILE
    data_path = (
        PROCESSED_DATA_DIR
        / "track"
        / "DC-filtered_EJScreen_2024_Tract_StatePct_with_AS_CNMI_GU_VI.csv"
    )
    output_path = OUTPUT_SHAPEFILE
    
    try:
        merged_gdf = merge_data_with_shapefile(
            shapefile_path, data_path, output_path
        )
        
        print(f"\nMerged GeoDataFrame shape: {merged_gdf.shape}")
        print(f"Columns: {list(merged_gdf.columns)}")
        
        # Uncomment to plot the data
        # plot_merged_data(merged_gdf, column='LOWINCPCT')
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

