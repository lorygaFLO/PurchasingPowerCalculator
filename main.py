# -*- coding: utf-8 -*-
"""
Purchasing Power Calculator

This script allows you to calculate purchasing power in different cities
based on Numbeo's cost of living data.
"""

import os
import pandas as pd
import json
from datetime import datetime
from utils.scraper import get_data
from utils.constants import BASEPATH
from utils.downloader import download_historical_data
from utils.habits_file import create_user_consumption_habits
from utils.utils import *



def main():
    # File paths
    data_dir = os.path.join(BASEPATH, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Get historical cost of living data starting from last year
    current_year = datetime.now().year
    start_year = 2000
    
    # Download historical data
    combined_data = download_historical_data(start_year, current_year - 1)
    
    # Save the combined DataFrame to a single CSV file
    if combined_data is not None:
        output_file = os.path.join(data_dir, 'cost_of_living_all_years.csv')
        combined_data.to_csv(output_file, index=False, sep=';')
        print(f"Combined data for all years saved to {output_file}")
        
        # Create a JSON file with spending categories initialized to zero
        create_user_consumption_habits(combined_data, data_dir)
    else:
        print("No data was collected.")
        return
    
    # Calcola il costo della vita basato sulle abitudini di consumo
    calculate_cost_of_living_by_habits(combined_data, data_dir)



if __name__ == "__main__":
    main()
