# Backtrader Fibonacci Retracement Strategy

![License](https://img.shields.io/badge/License-MIT-green)

This project contains a Backtrader strategy for trading using Fibonacci retracement levels combined with Simple Moving Averages (SMA). The strategy aims to identify buy and sell signals based on these technical indicators and execute trades accordingly.

> **Note**: This project is currently in the development stages. Contributions and feedback are welcome!

## Features

- **Fibonacci Retracement Levels**: Calculates and uses Fibonacci retracement levels for trading decisions.
- **Simple Moving Averages**: Implements short and long-period SMAs to determine the trend.
- **Buy/Sell Signals**: Generates buy and sell signals based on the SMA and Fibonacci retracement levels.
- **Stop Loss and Take Profit**: Includes mechanisms for stop loss and take profit orders.

## Requirements

- Python 3.8 or later
- Backtrader
- Pandas
- NumPy

You can install the necessary packages using pip:
```bash
pip install backtrader pandas numpy
```

## Project Structure
The project contains the following files and directories
- `backtest.py`: Main script to run the backtest.
- `strategies/`:
    - `fibonacci_retracement.py:` Contains the strategy logic using Fibonacci retracement and SMAs.
- `data/`: Directory for historical data CSV files.

## Data
Ensure you have a CSV file with historical trading data in the data/ directory. The CSV file should include the following columns:
- `Date`: Date of the trading data (format: YYYY-MM-DD)
- `Open`: Opening price
- `High`: Highest price
- `Low`: Lowest price
- `Close`: closing price
- `Volume`: Trading volume

Example CSV filename: `fixed_EUR_USD_Historical_Data.csv`

## Strategy
The `CombinedSMARetracementStrategy` in `strategies/fibonacci_retracement.py` uses the following parameters:
- `sma_short_period`: Short-period SMA (e.g., 2 days)
- `sma_long_period`: Long-period SMA (e.g., 4 days)
- `stop_loss`: Stop loss percentage (e.g., 1%)
- `take_profit`: Take profit percentage (e.g., 2%)
- `fib_levels`: Fibonacci retracement levels (50%, 61.8%, 38.2%)

## Buy Signal Condition
The buy signal is generated if:
- The short-period SMA is above the long-period SMA (indicating an uptrend).
- The current close price is below the 50% Fibonacci retracement level and previous close price was above it (indicating a pullback).

## sell Signal Condition
The sell signal is generated if:
- The short-period SMA is below the long-period SMA (indicating a downtrend).
- The current close price is above the 50% retracement level and the previous close was below it (indicating a pullback).

## Running the Backtest
To run the backtest, execute the `backtest.py` script:
```bash
python backtest.py
```
The script will:
1. Load the historical data from the CSV file.
2. Calculate Fibonacci retracement levels.
3. Initialize and run the Backtrader strategy.
4. Print the starting and ending portfolio values.

Starting Portfolio Value: 10000.00
Initial Fibonacci Levels: {'50%': 154.79, '61.8%': 154.12, '38.2%': 155.45}
Buy Signal - Current Close: 153.89, Previous Close: 155.77, Fib Levels: {'50%': 154.79, '61.8%': 154.12, '38.2%': 155.45}
Sell Signal - Current Close: 153.89, Previous Close: 155.77, Fib Levels: {'50%': 154.79, '61.8%': 154.12, '38.2%': 155.45}
Ending Portfolio Value: 10000.00

## Troubleshooting
- Not Enough Data: Ensure your dataset has more rows than the maximum SMA period used in the strategy.
- IndexError: Verify that your data has no missing values or gaps.
- Array Assignment Index Out of Range: Verify compatibility between dataset and SMA periods.

## Contributing
Contributions to improve this project are welcome! if you have suggestions, bug reports, or would like to contribute code, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.






