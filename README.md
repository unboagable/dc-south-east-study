# DC South East Study

Anacostia DC Air pollution and water warning system using EJScreen data.

## Overview

This project analyzes environmental justice data for the District of Columbia, with a focus on the Anacostia area. It integrates EJScreen API data with TIGER/Line shapefiles to create spatial visualizations and analyses of environmental and demographic indicators.

## Features

- **Data Filtering**: Filter EJScreen data for DC (District of Columbia)
- **API Integration**: Fetch environmental and demographic data from the EJScreen API
- **Spatial Analysis**: Merge data with TIGER/Line shapefiles for geographic visualization
- **Batch Processing**: Fetch data for multiple block groups with rate limiting

## Project Structure

```
dc-south-east-study/
├── data/
│   ├── raw/              # Raw data files and shapefiles
│   └── processed/        # Processed data and merged shapefiles
├── notebooks/            # Jupyter notebooks for analysis
├── src/                  # Source code
│   ├── config.py         # Configuration constants
│   ├── start.py          # Filter EJScreen data for DC
│   ├── get_data_from_api.py  # Single API data fetch
│   ├── get_study_data.py      # Batch API data fetching
│   └── clean_data.py     # Merge data with shapefiles
├── pyproject.toml        # Poetry dependencies
└── requirements.txt      # pip dependencies
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (recommended) or pip

### Installing Poetry

**macOS (using Homebrew):**
```bash
brew install pipx
pipx ensurepath
pipx install poetry
```

**Windows (using Scoop):**
```bash
scoop install pipx
pipx ensurepath
pipx install poetry
```

**Alternative (using pip):**
```bash
pip install poetry
```

### Installing Dependencies

**Using Poetry (recommended):**
```bash
poetry install
```

**Using pip:**
```bash
pip install -r requirements.txt
```

## Usage

### Filter EJScreen Data for DC

Filter the national EJScreen dataset to only include DC data:

```bash
poetry run python src/start.py
# or
python src/start.py
```

This will:
- Read the EJScreen tract-level data
- Filter for DC (ST_ABBREV == 'DC')
- Save filtered data to `data/processed/track/`

### Fetch Data from EJScreen API

**Single Block Group:**
```bash
poetry run python src/get_data_from_api.py
```

**Multiple Block Groups (Anacostia area):**
```bash
poetry run python src/get_study_data.py
```

This will:
- Fetch data for all block groups in southeast Anacostia
- Fetch city-level data for Washington, DC
- Save results to CSV files in `data/processed/block_group/`

### Merge Data with Shapefiles

Merge filtered CSV data with TIGER/Line shapefiles for spatial analysis:

```bash
poetry run python src/clean_data.py
```

This will:
- Load TIGER/Line tract shapefiles
- Merge with filtered EJScreen data
- Save merged shapefile to `data/processed/shapefiles/track/`

## Configuration

Configuration constants are defined in `src/config.py`, including:
- File paths
- API endpoints
- Block group IDs
- Request delays

## Development

### Code Quality

The project uses modern Python practices:
- Type hints
- Pathlib for file paths
- Error handling
- Configuration management

### Development Tools

Development dependencies (installed with Poetry):
- `black`: Code formatting
- `ruff`: Fast linting
- `mypy`: Type checking
- `pytest`: Testing

Run formatting:
```bash
poetry run black src/
```

Run linting:
```bash
poetry run ruff check src/
```

## Data Sources

- **EJScreen**: EPA's Environmental Justice Screening and Mapping Tool
- **TIGER/Line**: U.S. Census Bureau geographic boundary files

## License

See LICENSE file for details.

## Contributing

1. Ensure code follows the project's style guidelines
2. Add type hints to all functions
3. Include docstrings for public functions
4. Test your changes before submitting
