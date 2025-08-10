# Poetry Setup Guide

Poetry is now successfully installed and configured for this project!

## What Was Done

1. **Poetry Installed**: Version 2.1.4 installed to `C:\Users\tom\AppData\Roaming\Python\Scripts\poetry`
2. **Virtual Environment Created**: Poetry created its own isolated virtual environment
3. **Dependencies Installed**: All packages from `pyproject.toml` installed including:
   - **Runtime**: streamlit, plotly, pandas, numpy, python-dateutil
   - **Development**: pytest, ruff, black, mypy, pre-commit

## Usage

### Running the Application
```bash
# Option 1: Using PowerShell script (Windows - Recommended)
.\run_poetry.ps1 run streamlit run app.py

# Option 2: Direct run with Poetry (if Poetry is in PATH)
poetry run streamlit run app.py

# Option 3: Enter Poetry shell first
poetry shell
streamlit run app.py
```

### Development Commands
```bash
# Windows PowerShell script commands (Recommended)
.\run_poetry.ps1 install                    # Install dependencies
.\run_poetry.ps1 add package-name          # Add new dependency
.\run_poetry.ps1 add --group dev package-name  # Add development dependency
.\run_poetry.ps1 run pytest               # Run tests
.\run_poetry.ps1 run black .               # Format code
.\run_poetry.ps1 run ruff check .          # Lint code
.\run_poetry.ps1 run mypy .                # Type checking

# Direct Poetry commands (if Poetry is in PATH)
poetry install
poetry add package-name
poetry add --group dev package-name
poetry run pytest
poetry run black .
poetry run ruff check .
poetry run mypy .
```

### Environment Info
```bash
# Windows PowerShell script commands
.\run_poetry.ps1 env info                  # Show virtual environment path
.\run_poetry.ps1 show                      # Show installed packages
.\run_poetry.ps1 show --outdated          # Check for dependency updates

# Direct Poetry commands (if Poetry is in PATH)
poetry env info
poetry show
poetry show --outdated
```

## Benefits

- **Isolated Environment**: Poetry manages its own virtual environment
- **Dependency Resolution**: Poetry resolves dependency conflicts automatically
- **Lock File**: `poetry.lock` ensures reproducible builds
- **Development Tools**: All linting, formatting, and testing tools included
- **Easy Updates**: Simple dependency management and updates

## Files Created/Modified

- `pyproject.toml`: Project configuration and dependencies
- `poetry.lock`: Locked dependency versions for reproducibility
- `run_poetry.ps1`: PowerShell script for Poetry commands (Windows PATH fix)
- Virtual environment: Created automatically by Poetry

## Windows PATH Issue Resolution

Poetry was installed but not added to Windows PATH. The `run_poetry.ps1` script solves this by:
1. Providing direct access to Poetry executable at `C:\Users\tom\AppData\Roaming\Python\Scripts\poetry.exe`
2. Enabling PowerShell script execution with `RemoteSigned` policy
3. Acting as a wrapper for all Poetry commands

## Integration with Existing Setup

Poetry works alongside the existing setup:
- ✅ `requirements.txt` still works for Streamlit Cloud deployment  
- ✅ `setup.bat` and `run.bat` still work for simple pip-based setup
- ✅ Poetry provides advanced dependency management for development

You can now use either approach:
- **Simple**: Use `setup.bat` and `run.bat` for basic setup
- **Advanced**: Use Poetry for professional development workflow