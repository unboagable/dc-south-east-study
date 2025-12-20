"""Fetch EJScreen data for multiple block groups and cities."""
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

from config import (
    API_REQUEST_DELAY,
    BLOCK_GROUPS_ANACOSTIA,
    DC_AREA_ID,
    DC_CITY_NAME,
    EJScreen_API_URL,
    PROCESSED_DATA_DIR,
)


def get_ejscreen_data(
    params: Dict[str, str], area_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Fetch data from EJScreen API with given parameters.
    
    Args:
        params: API request parameters
        area_id: Optional area ID for tracking
        
    Returns:
        Flattened data dictionary or None if request failed
    """
    try:
        response = requests.get(EJScreen_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields
        demographics = data.get("data", {}).get("demographics", {})
        main_stats = data.get("data", {}).get("main", {})
        extras = data.get("extras", {})
        
        # Flatten the data
        flattened_data = {
            "area_id": area_id,  # Add area_id for tracking
            "total_population": demographics.get("TOTALPOP"),
            "percent_minority": demographics.get("PCT_MINORITY"),
            "per_capita_income": demographics.get("PER_CAP_INC"),
            "unemployment_rate": demographics.get("P_EMP_STAT_UNEMPLOYED"),
            "pm25_air_quality": main_stats.get("RAW_E_PM25"),
            "traffic_exposure": main_stats.get("RAW_E_TRAFFIC"),
            "diesel_particulate_matter": main_stats.get("RAW_E_DIESEL"),
            "life_expectancy": extras.get("RAW_HI_LIFEEXP", None),
        }
        
        return flattened_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {area_id}: {e}", file=sys.stderr)
        return None


def get_ejscreen_data_city(city: str, area_id: str) -> Optional[Dict[str, Any]]:
    """Fetch EJScreen data for a city.
    
    Args:
        city: City name
        area_id: City area ID
        
    Returns:
        Flattened data dictionary or None if request failed
    """
    params = {
        "namestr": city,
        "geometry": "",
        "distance": "",
        "unit": "9035",
        "areatype": "city",
        "areaid": area_id,
        "f": "json",
    }
    return get_ejscreen_data(params, area_id=area_id)


def get_ejscreen_data_bg(area_id: str) -> Optional[Dict[str, Any]]:
    """Fetch EJScreen data for a block group.
    
    Args:
        area_id: Block group ID
        
    Returns:
        Flattened data dictionary or None if request failed
    """
    params = {
        "namestr": area_id,
        "geometry": "",
        "distance": "",
        "unit": "9035",
        "areatype": "blockgroup",
        "areaid": area_id,
        "f": "json",
    }
    return get_ejscreen_data(params, area_id=area_id)


def fetch_multiple_block_groups(
    block_group_ids: List[str], delay: float = API_REQUEST_DELAY
) -> pd.DataFrame:
    """Fetch EJScreen data for multiple block groups.
    
    Args:
        block_group_ids: List of block group IDs
        delay: Delay in seconds between API requests
        
    Returns:
        DataFrame containing data for all block groups
    """
    data_list = []
    total = len(block_group_ids)
    
    print(f"Fetching data for {total} block groups...")
    
    for i, bg_id in enumerate(block_group_ids, 1):
        print(f"Processing {i}/{total}: {bg_id}")
        result = get_ejscreen_data_bg(bg_id)
        if result:
            data_list.append(result)
        else:
            print(f"  Warning: Failed to fetch data for {bg_id}", file=sys.stderr)
        
        # Avoid overwhelming the API
        if i < total:
            time.sleep(delay)
    
    if not data_list:
        print("Error: No data was successfully fetched", file=sys.stderr)
        return pd.DataFrame()
    
    return pd.DataFrame(data_list)


def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    """Save DataFrame to CSV file.
    
    Args:
        df: DataFrame to save
        output_path: Path to save CSV file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data saved to: {output_path}")


def main() -> None:
    """Main entry point for fetching study data."""
    # Fetch data for all block groups southeast of Anacostia
    print("=" * 60)
    print("Fetching EJScreen Data - Southeast Anacostia")
    print("=" * 60)
    df_anacostia = fetch_multiple_block_groups(BLOCK_GROUPS_ANACOSTIA)
    
    if not df_anacostia.empty:
        print(f"\nAnacostia Data Summary:")
        print(df_anacostia.head())
        print(f"\nShape: {df_anacostia.shape}")
        
        # Save to CSV
        output_path = PROCESSED_DATA_DIR / "block_group" / "anacostia_ejscreen_data.csv"
        save_dataframe(df_anacostia, output_path)
    
    # Fetch data for DC
    print("\n" + "=" * 60)
    print("Fetching EJScreen Data - Washington, DC")
    print("=" * 60)
    data_dc = get_ejscreen_data_city(DC_CITY_NAME, DC_AREA_ID)
    
    if data_dc:
        df_dc = pd.DataFrame([data_dc])
        print("\nDC Data Summary:")
        print(df_dc.head())
        
        # Save to CSV
        output_path = PROCESSED_DATA_DIR / "block_group" / "dc_ejscreen_data.csv"
        save_dataframe(df_dc, output_path)
    else:
        print("Failed to fetch DC data", file=sys.stderr)


if __name__ == "__main__":
    main()
