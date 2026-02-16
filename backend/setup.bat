@echo off
echo Setting up KB Builder Backend...
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To start the backend server, run:
echo   python app.py
