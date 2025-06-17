# IBKR Python Trading System

A comprehensive Python-based algorithmic trading system using Interactive Brokers API.

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Development Phases](#development-phases)
- [Testing Strategy](#testing-strategy)
- [Risk Management](#risk-management)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Project Overview

This project implements an automated trading system that interfaces with Interactive Brokers (IBKR) to execute trading strategies, manage portfolios, and monitor market conditions.

### Key Features
- Real-time market data streaming
- Multiple trading strategy support
- Risk management and position sizing
- Performance tracking and reporting
- Paper trading and backtesting capabilities

## Prerequisites

Before you begin, ensure you have a basic understanding of:
- Python 3.8+
- Financial markets and trading concepts.
- Interactive Brokers TWS or IB Gateway.
- An IBKR Pro or Prime account (a paper trading account is sufficient for initial setup and testing).

For detailed software and environment setup, please see the [Installation Guide](./docs/installation.md).

## Installation

For detailed instructions on setting up your development environment and installing necessary dependencies, please refer to the [Installation Guide](./docs/installation.md).

The guide covers:
- Using the automated installation scripts (`install.sh` for Linux/macOS, `install.bat` for Windows).
- Manual installation steps.
- Setting up Interactive Brokers TWS/Gateway.

Quick start for local development after cloning:
```bash
# For Linux/macOS
./install.sh
source venv/bin/activate

# For Windows (in Command Prompt)
install.bat
venv\Scripts\activate.bat
```
Then, you can run tests or scripts:
```bash
pytest
python scripts/run_trading_bot.py --mode paper
```

## Project Structure

```
ibkr-trading-system/
├── README.md
├── requirements.txt
├── setup.py
├── install.sh
├── install.bat
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── credentials.py
├── src/
│   ├── __init__.py
│   ├── connection/
│   │   ├── __init__.py
│   │   ├── ib_connector.py
│   │   └── connection_manager.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── market_data.py
│   │   ├── historical_data.py
│   │   └── data_storage.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py
│   │   ├── moving_average.py
│   │   ├── mean_reversion.py
│   │   └── momentum.py
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── order_manager.py
│   │   └── position_manager.py
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── risk_manager.py
│   │   └── portfolio_manager.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── helpers.py
│   │   └── validators.py
│   └── monitoring/
│       ├── __init__.py
│       ├── performance_tracker.py
│       └── alerts.py
├── tests/
│   ├── __init__.py
│   ├── test_connection.py
│   ├── test_strategies.py
│   └── test_risk.py
├── notebooks/
│   ├── strategy_development.ipynb
│   └── backtesting.ipynb
├── scripts/
│   ├── run_trading_bot.py
│   └── backtest.py
└── docs/
    ├── installation.md
    ├── configuration.md
    └── api_reference.md
```

## Development Phases

### Phase 1: Foundation Setup

#### Step 1.1: Environment Setup
**Tasks:**
- Complete the environment setup as described in the [Installation Guide](./docs/installation.md).
- Install IB API Python client (`ib_insync` or `ibapi`) - *This will be part of `requirements.txt`.*
- Set up TWS/IB Gateway and configure a paper trading account as per the [Installation Guide](./docs/installation.md).

**Expected Outcome:**
- Working development environment.
- Successful connection to IBKR paper trading account.

#### Step 1.2: Project Architecture
**Tasks:**
- Implement logging system.
- Implement configuration management.
- Create base classes and interfaces for core components.

**Expected Outcome:**
- Organized codebase with clear separation of concerns.
- Centralized configuration and logging.

### Phase 2: Data Management
(And subsequent phases remain the same as original README)
#### Step 2.1: Market Data Streaming
...
#### Step 2.2: Historical Data Collection
...
### Phase 3: Trading Strategy Development
...
### Phase 4: Order Execution System
...
### Phase 5: Risk Management
...
### Phase 6: Backtesting System
...
### Phase 7: Monitoring and Alerts
...
### Phase 8: Production Deployment
...

## Testing Strategy

### Unit Tests
- Test each component in isolation.
- Mock IBKR API calls.
- Validate calculations and logic.

### Integration Tests
- Test component interactions.
- Verify data flow.
- Validate order execution flow.

### Paper Trading
- Run strategies on paper account.
- Monitor for issues.
- Validate performance metrics.

## Risk Management

### Pre-Production Checklist
- [ ] All strategies backtested
- [ ] Risk limits configured
- [ ] Stop-loss mechanisms tested
- [ ] Error handling comprehensive
- [ ] Monitoring alerts active
- [ ] Documentation complete

### Production Risk Controls
- Maximum position sizes
- Daily loss limits
- Correlation limits
- Margin requirements
- Circuit breakers

## Deployment

### Local Development
For initial setup and installation, please see the [Installation Guide](./docs/installation.md).

To run the system after setup:
1.  Ensure your virtual environment is activated:
    ```bash
    # Linux/macOS
    source venv/bin/activate
    # Windows
    venv\Scripts\activate.bat
    ```
2.  Ensure TWS or IB Gateway is running and you are logged into your paper/live account.
3.  Run your desired scripts, for example:
    ```bash
    python scripts/run_trading_bot.py --mode paper
    ```

### Production Deployment
- Use dedicated server or cloud instance.
- Ensure reliable internet connection.
- Set up process monitoring (e.g., `systemd`, `supervisor`).
- Configure automated restarts.
- Implement backup systems.

## Contributing

Please read `CONTRIBUTING.md` (once created) for details on our code of conduct and the process for submitting pull requests. For now, feel free to open issues or suggest improvements.

## License

This project is licensed under the MIT License - see the `LICENSE` file (once created) for details.

## Disclaimer

This software is for educational purposes only. Use at your own risk. The authors and contributors are not responsible for any financial losses incurred through the use of this software.
