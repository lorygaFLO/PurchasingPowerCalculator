# Purchasing Power Calculator

This project allows you to calculate purchasing power in different cities around the world based on Numbeo's cost of living data. The application lets you customize your spending habits and compare the cost of living between different cities and years.

## Features

- Download updated cost of living data from Numbeo
- Create a customizable template for your spending habits
- Calculate daily cost of living in different cities based on your habits
- Compare cost of living between different years
- View comparative charts

## Requirements

- Python 3.6 or higher
- pandas
- numpy
- matplotlib
- requests
- beautifulsoup4

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lorygaFLO/PurchasingPowerCalculator.git
   cd PurchasingPowerCalculator
   ```

2. Install dependencies:
   ```
   pip install pandas numpy matplotlib requests beautifulsoup4
   ```

## Usage

1. Run the main program:
   ```
   python main.py
   ```

2. From the main menu, select option 1 to create a spending habits template.

3. Edit the generated file (`data/ExpHabits_template.csv`) by entering quantities for each spending category, then rename it to `ExpHabits_user.csv`.

4. Use option 2 to calculate the daily cost of living for the selected year.

5. Use option 3 to compare the cost of living between two different years.

## Project Structure

```
PurchasingPowerCalculator/
├── .vscode/
│   └── launch.json       # Debugger configuration
├── data/                 # Directory for generated data
├── plots/                # Directory for generated charts
├── src/
│   ├── __init__.py
│   ├── scraper.py        # Data scraping module
│   ├── data_processor.py # Data processing module
│   └── visualizer.py     # Visualization module
├── main.py               # Main script
└── README.md             # Documentation
```

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.