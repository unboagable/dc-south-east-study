"""Filter EJScreen data for DC (District of Columbia)."""
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def identify_columns(data: pd.DataFrame) -> None:
    """Print all available columns in the dataset.
    
    Args:
        data: DataFrame to analyze
    """
    print("Available columns:")
    for col in data.columns:
        print(f"  - {col}")


def filter_dc_data(
    input_file: Path,
    output_file: Path,
    state_column: str = "ST_ABBREV",
    state_value: str = "DC",
) -> pd.DataFrame:
    """Filter EJScreen data for a specific state.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        state_column: Name of the state column
        state_value: State abbreviation to filter for
        
    Returns:
        Filtered DataFrame
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        KeyError: If state_column doesn't exist in the DataFrame
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the CSV file
    df = pd.read_csv(input_file, index_col=0, encoding="utf-8")
    
    # Identify columns
    identify_columns(df)
    
    # Filter rows where state_column matches state_value
    if state_column not in df.columns:
        raise KeyError(f"Column '{state_column}' not found in dataset")
    
    filtered_df = df[df[state_column] == state_value].copy()
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the filtered data
    filtered_df.to_csv(output_file, index=False)
    print(f"\nFiltered data saved to: {output_file}")
    print(f"Filtered {len(filtered_df)} rows out of {len(df)} total rows")
    
    return filtered_df


def main() -> None:
    """Main entry point for filtering DC data."""
    # Define file paths
    input_file = RAW_DATA_DIR / "EJScreen_2024_Tract_StatePct_with_AS_CNMI_GU_VI.csv"
    output_file = (
        PROCESSED_DATA_DIR
        / "track"
        / "DC-filtered_EJScreen_2024_Tract_StatePct_with_AS_CNMI_GU_VI.csv"
    )
    
    try:
        filter_dc_data(input_file, output_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
