# Purchasing Power Calculator

This project allows you to calculate purchasing power in different cities around the world based on Numbeo's cost of living data. The application automatically downloads historical data, lets you customize your spending habits, and compares the cost of living between different cities and years.

## Features

- Automatically download historical cost of living data from Numbeo
- Retrieve annual income data for comprehensive analysis
- Create a customizable JSON template for your spending habits
- Calculate daily cost of living in different cities based on your personal consumption patterns
- Compare cost of living between different years and locations
- Generate detailed reports for analysis

## Requirements

- Python 3.6 or higher
- pandas
- numpy
- requests
- beautifulsoup4
- lxml

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lorygaFLO/PurchasingPowerCalculator.git
   cd PurchasingPowerCalculator
   ```
2. Install dependencies


## Usage

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the main program:
   ```
   python main.py
   ```

3. The program will automatically:
   - Download historical cost of living data from Numbeo
   - Create a user consumption habits template file (`data/user_consumption_habits.json`)
   - Calculate the cost of living based on these habits

4. Edit the generated JSON file to customize your consumption habits and preferences.

5. Run the program again to recalculate with your personalized consumption patterns.

## Project Structure

```
PurchasingPowerCalculator/
├── .vscode/
│   └── launch.json       # Debugger configuration
├── data/                 # Directory for generated data
│   ├── cost_of_living_all_years.csv    # Combined historical data
│   └── user_consumption_habits.json    # User's consumption patterns
├── utils/
│   ├── __init__.py
│   ├── constants.py      # Project constants
│   ├── downloader.py     # Historical data downloader
│   ├── habits_file.py    # User habits template creator
│   ├── scraper.py        # Data scraping module
│   └── utils.py          # Utility functions
├── main.py               # Main script
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.