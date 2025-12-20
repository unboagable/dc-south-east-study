"""Fetch and process EJScreen API data for a single block group."""
import sys
from typing import Any, Dict, Optional

import pandas as pd
import requests

from config import EJScreen_API_URL


def fetch_ejscreen_data(
    area_id: str,
    area_type: str = "blockgroup",
    city_name: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Fetch data from the EJScreen API.
    
    Args:
        area_id: Area identifier
        area_type: Type of area (blockgroup, city, etc.)
        city_name: Optional city name for city-type queries
        
    Returns:
        JSON response data or None if request failed
    """
    params = {
        "namestr": city_name if city_name else area_id,
        "geometry": "",
        "distance": "",
        "unit": "9035",
        "areatype": area_type,
        "areaid": area_id,
        "f": "json",
    }
    
    try:
        response = requests.get(EJScreen_API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {area_id}: {e}", file=sys.stderr)
        return None


def extract_ejscreen_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and flatten relevant fields from EJScreen API response.
    
    Args:
        data: JSON response from EJScreen API
        
    Returns:
        Flattened dictionary with relevant fields
    """
    demographics = data.get("data", {}).get("demographics", {})
    main_stats = data.get("data", {}).get("main", {})
    extras = data.get("extras", {})
    
    # Flatten the data into a single dictionary
    return {**demographics, **main_stats, **extras}


def print_summary(data: Dict[str, Any]) -> None:
    """Print a summary of key EJScreen data fields.
    
    Args:
        data: Flattened EJScreen data dictionary
    """
    demographics = data.get("data", {}).get("demographics", {})
    main_stats = data.get("data", {}).get("main", {})
    extras = data.get("extras", {})
    
    print("Demographics:")
    print(f"  Total Population: {demographics.get('TOTALPOP', 'N/A')}")
    print(f"  Percent Minority: {demographics.get('PCT_MINORITY', 'N/A')}%")
    print(f"  Per Capita Income: ${demographics.get('PER_CAP_INC', 'N/A')}")
    print(f"  Unemployment Rate: {demographics.get('P_EMP_STAT_UNEMPLOYED', 'N/A')}%")
    
    print("\nEnvironmental Factors:")
    print(f"  Air Quality (PM2.5): {main_stats.get('RAW_E_PM25', 'N/A')} µg/m³")
    print(f"  Traffic Exposure: {main_stats.get('RAW_E_TRAFFIC', 'N/A')} vehicles/day")
    print(
        f"  Diesel Particulate Matter: {main_stats.get('RAW_E_DIESEL', 'N/A')} µg/m³"
    )
    
    life_expectancy = extras.get("RAW_HI_LIFEEXP", "N/A")
    print(f"\nHealth Indicator - Life Expectancy: {life_expectancy} years")


def main() -> None:
    """Main entry point for fetching EJScreen API data."""
    # Example: Fetch data for a specific block group
    area_id = "110010088022"
    
    data = fetch_ejscreen_data(area_id, area_type="blockgroup")
    
    if data is None:
        print("Failed to fetch data from API", file=sys.stderr)
        sys.exit(1)
    
    # Print summary
    print_summary(data)
    
    # Extract and flatten fields
    flattened_data = extract_ejscreen_fields(data)
    
    # Create DataFrame
    df = pd.DataFrame([flattened_data])
    
    print("\nDataFrame:")
    print(df)
    
    print("\nDataFrame Statistics:")
    print(df.describe())


if __name__ == "__main__":
    main()

