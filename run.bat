@echo off
echo Starting CarIActerology application...

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running Streamlit application...
streamlit run app.py

pause