import os
import pandas as pd
import json
from utils.constants import BASEPATH


def create_user_consumption_habits(df, data_dir):
    """
    Creates a JSON file with spending categories initialized to zero
    
    Args:
        df (pandas.DataFrame): DataFrame with cost of living data
        data_dir (str): Path to the data directory
    """
    # JSON file path
    json_file = os.path.join(data_dir, 'habits_config.json')
    
    # Check if file already exists
    if os.path.exists(json_file):
        print(f"Consumption habits file already exists at {json_file}")
        return
    
    # Get DataFrame columns that represent spending categories
    # Exclude columns like 'City', 'Country', 'Year', etc.
    expense_columns = [col for col in df.columns if col not in ['City', 'Country', 'Year', 'Month']]
    
    # Create a dictionary with spending categories initialized to zero
    consumption_habits = {}
    for column in expense_columns:
        # Clean column name to use as key
        category = column.strip()
        consumption_habits[category] = 0
    
    # Save dictionary to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(consumption_habits, f, indent=4, ensure_ascii=False)
    
    print(f"Consumption habits file created at {json_file}")
    print("You can modify this file to input your consumption habits.")
