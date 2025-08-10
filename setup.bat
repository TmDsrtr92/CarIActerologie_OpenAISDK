@echo off
echo Setting up CarIActerology development environment...

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Verifying installation...
python -c "import streamlit, plotly, pandas, numpy; print('All dependencies installed successfully')"

echo.
echo Setup complete! To activate the environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the application:
echo   streamlit run app.py

pause