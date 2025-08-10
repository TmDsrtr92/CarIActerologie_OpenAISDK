# Development Setup Guide

## Prerequisites

- Python 3.11 or higher
- Git
- Poetry (optional, for dependency management)

## Quick Setup

### Option 1: Using setup.bat (Windows)
```bash
# Run the automated setup
setup.bat

# Then run the application
run.bat
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

### Option 3: Using Poetry (if installed)
```bash
# Install dependencies
poetry install

# Activate shell
poetry shell

# Run application
streamlit run app.py
```

## Development Workflow

### Running the Application
```bash
# Make sure virtual environment is activated
streamlit run app.py

# Or use the run script
run.bat
```

### Adding Dependencies
```bash
# Add to requirements.txt, then:
pip install -r requirements.txt

# Or with Poetry:
poetry add <package-name>
```

### Code Quality
```bash
# Format code (once dependencies are installed)
black .

# Lint code
ruff check .

# Type checking
mypy .
```

## Project Structure

```
CarIActerology_OpenAISDK/
├── app.py                  # Main Streamlit application
├── pages/                  # Multi-page application files
│   ├── 1_Chat.py          # Chat interface
│   ├── 2_Analysis.py      # Character analysis
│   ├── 3_Dashboard.py     # Progress dashboard
│   ├── 4_Reports.py       # Report generation
│   └── 5_Settings.py      # User settings
├── modules/                # Business logic (future)
├── data/                   # Data storage
├── tests/                  # Test suite
├── .streamlit/            # Streamlit configuration
├── venv/                  # Virtual environment
├── requirements.txt        # Dependencies
├── pyproject.toml         # Poetry configuration
├── setup.bat              # Windows setup script
└── run.bat                # Windows run script
```

## Troubleshooting

### Common Issues

1. **Import errors on Dashboard/Reports/Settings pages**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that virtual environment is activated

2. **Streamlit not found**
   - Activate virtual environment: `venv\Scripts\activate`
   - Reinstall: `pip install streamlit`

3. **Module import errors**
   - Ensure you're running from the project root directory
   - Check that all required packages are in requirements.txt

### Development Tips

- Use `streamlit run app.py --server.runOnSave true` for auto-reload
- Access the app at `http://localhost:8501`
- Use `Ctrl+C` to stop the Streamlit server

## Next Steps (Phase 2)

Once the UI is stable, we'll integrate:
- OpenAI Agents SDK for AI functionality
- Mem0 for memory management
- FAISS for vector storage
- Supabase for data persistence