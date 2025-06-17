@echo off
echo Creating Python virtual environment 'venv'...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment. Please ensure Python 3 is installed and accessible as 'python'.
    goto :eof
)

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat && pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies. Please check requirements.txt and your internet connection.
) else (
    echo Installation of dependencies complete.
)

echo Setup complete. To activate the virtual environment in your current command prompt, run: venv\Scripts\activate.bat
