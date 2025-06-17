# Installation Guide

This guide provides instructions on how to set up the project environment for the IBKR Python Trading System.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+ (it's recommended to manage Python versions using tools like `pyenv` or `conda`)
- `pip` (Python package installer)
- `git` (version control system)

## Option 1: Using Installation Scripts (Recommended)

We provide scripts to automate the setup process for Linux/macOS and Windows.

### For Linux/macOS:
1.  Open your terminal.
2.  Navigate to the root directory of the cloned project.
3.  Make the script executable (if you haven't already or if you pulled changes):
    ```bash
    chmod +x install.sh
    ```
4.  Run the installation script:
    ```bash
    ./install.sh
    ```
    This script will:
    - Create a Python virtual environment named `venv` in the project root.
    - Activate the virtual environment.
    - Install the required Python packages from `requirements.txt`.
5.  After the script completes, activate the virtual environment in your current shell session by running:
    ```bash
    source venv/bin/activate
    ```

### For Windows:
1.  Open Command Prompt or PowerShell.
2.  Navigate to the root directory of the cloned project.
3.  Run the installation script:
    ```batch
    install.bat
    ```
    This script will:
    - Create a Python virtual environment named `venv` in the project root.
    - Activate the virtual environment and install dependencies from `requirements.txt`.
4.  After the script completes, if you need to manually activate the environment in a new terminal, run:
    ```batch
    venv\Scripts\activate.bat
    ```

## Option 2: Manual Installation Steps

If you prefer to set up the environment manually, follow these steps:

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a Virtual Environment:**
    Navigate to the project's root directory and run:
    ```bash
    python3 -m venv venv
    ```
    (On Windows, you might use `python` instead of `python3`)

3.  **Activate the Virtual Environment:**
    -   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows (Command Prompt):**
        ```batch
        venv\Scripts\activate.bat
        ```
    -   **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        (If you encounter issues with script execution policy on PowerShell, you might need to run: `Set-ExecutionPolicy Unrestricted -Scope Process`)

4.  **Install Dependencies:**
    With the virtual environment activated, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Setting up Interactive Brokers (IBKR) Software

To connect to Interactive Brokers, you need either Trader Workstation (TWS) or IB Gateway.

1.  **Download and Install TWS or IB Gateway:**
    -   Visit the [Interactive Brokers software downloads page](https://www.interactivebrokers.com/en/index.php?f=16040) to get the latest versions.
    -   Follow their installation instructions.

2.  **Configure API Settings:**
    -   In TWS: Go to `File > Global Configuration > API > Settings`.
    -   Ensure "Enable ActiveX and Socket Clients" is checked.
    -   Note the "Socket port" number (default is `7496` for TWS live account, `7497` for TWS paper account, `4001` for Gateway live, `4002` for Gateway paper). You'll need this for the application configuration.
    -   It's recommended to add `127.0.0.1` to the "Trusted IP Addresses" if running the trading system on the same machine as TWS/Gateway.

3.  **Paper Trading Account:**
    -   It is **highly recommended** to start with a paper trading account to test your strategies and the system without risking real money.
    -   You can request a paper trading account through your IBKR account management portal.
    -   Ensure TWS or IB Gateway is logged into your paper trading account when you intend to do paper trading with this system.

## Next Steps

Once the environment is set up and IBKR software is configured:
- Configure your application-specific settings in the `config/` directory (see `docs/configuration.md`).
- You can start exploring the system, for example, by running the trading bot script as described in the main `README.md`.
