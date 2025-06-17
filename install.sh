#!/bin/bash
echo "Creating Python virtual environment 'venv' using python3.12..."
python3.12 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment using python3.12. Please ensure Python 3.12 and its venv module are correctly installed."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check requirements.txt and your internet connection."
    # It's debatable whether to exit here or let the user proceed with an incomplete env
    # For now, let's inform and continue, as the venv is created.
else
    echo "Installation of dependencies complete."
fi

echo "Setup complete. To activate the virtual environment in your current shell, run: source venv/bin/activate"
