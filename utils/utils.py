import os
import pandas as pd
import json
import numpy as np
from datetime import datetime
from utils.constants import BASEPATH
from utils.scraper import get_cost_of_living_data, get_annual_income_data

def calculate_cost_of_living_by_habits(data, data_dir):
    """
    Calculates the cost of living in all countries based on the user's consumption habits
    and generates reports per year.
    
    Args:
        data (pandas.DataFrame): DataFrame with cost of living data
        data_dir (str): Path to the data directory
    """
    # Load the user's consumption habits
    habits_file = os.path.join(data_dir, 'user_consumption_habits.json')
    
    if not os.path.exists(habits_file):
        raise FileNotFoundError("Consumption habits file not found. Please check...")
    
    with open(habits_file, 'r', encoding='utf-8') as f:
        user_habits = json.load(f)
    
    # Check if all values in the habits file are still zero (not modified by the user)
    all_zeros = all(value == 0 for value in user_habits.values())
    if all_zeros:
        print("\nWARNING: The consumption habits file has not been modified.")
        print("All values are still zero. Please modify the 'user_consumption_habits.json' file")
        print("in the 'data' folder by entering your monthly consumption values before running this calculation.")
        return
    # Get all available years in the data
    available_years = sorted(data['year'].unique())
    latest_year = max(available_years)
    
    print(f"\nCalculating annual cost of living based on your monthly consumption habits for all available cities...")
    
    # Create a DataFrame to store results for all years
    all_years_results = []
    
    # For each available year in the data
    for year in available_years:
        year_data = data[data['year'] == year]
        
        # Group by city to avoid duplicates
        cities_data = year_data.groupby('City').first().reset_index()
        
        for _, city_row in cities_data.iterrows():
            city_name = city_row['City']
            country_name = city_row['Country'] if 'Country' in city_row else "N/A"
            annual_cost = 0.0
            
            # Handle non-numeric values for annual income
            try:
                annual_income = float(city_row.get('Average Monthly Net Salary (After Tax)_y', 0)) * 12
            except ValueError:
                annual_income = 0.0  # Set to 0 if the value is not numeric
            
            city_breakdown = {}
            
            for category, amount in user_habits.items():
                if category in city_row and pd.notna(city_row[category]) and amount > 0:
                    try:
                        # Convert values to float to ensure they are numeric
                        category_value = float(city_row[category])
                        amount_value = float(amount)
                        
                        # Multiply the reference value by the monthly consumption amount
                        monthly_category_cost = category_value * amount_value
                        annual_category_cost = monthly_category_cost * 12  # Annualize the cost
                        
                        annual_cost += annual_category_cost
                        city_breakdown[category] = annual_category_cost
                    except (ValueError, TypeError) as e:
                        # Skip this category if conversion fails, but log the error
                        if year == latest_year:  # Show errors only for the latest year
                            print(f"Error processing category '{category}' for city '{city_name}': {e}")
                            print(f"Value in data: {city_row[category]}, Type: {type(city_row[category])}")
                            print(f"Amount in habits: {amount}, Type: {type(amount)}")
            
            if annual_cost > 0:  # Only if we calculated a cost
                all_years_results.append({
                    'City': city_name,
                    'Country': country_name,
                    'Year': int(year),  # Convert numpy.int64 to Python int
                    'Annual Cost': float(annual_cost),  # Ensure it's a Python float
                    'Annual Income': float(annual_income),
                    'Cost Breakdown': city_breakdown
                })
    
    # Create a DataFrame with results for all years
    all_years_df = pd.DataFrame([{
        'City': r['City'], 
        'Country': r['Country'],
        'Year': r['Year'],
        'Annual Cost': r['Annual Cost'],
        'Annual Income': r['Annual Income']
    } for r in all_years_results])
    
    # Save results for all years in a single CSV file
    all_years_file = os.path.join(data_dir, 'cost_breakdown.csv')
    all_years_df = all_years_df.sort_values(by='Annual Cost', ascending=True)
    all_years_df.to_csv(all_years_file, index=False, sep=';', decimal=',')
    print(f"\nComplete results for all years saved in {all_years_file}")
    
    # Filter results only for the latest year
    latest_results = [r for r in all_years_results if r['Year'] == int(latest_year)]
    latest_results.sort(key=lambda x: x['Annual Cost'])
    
    # Create a DataFrame with results for the latest year
    latest_df = all_years_df[all_years_df['Year'] == latest_year]
    
    # Calculate the percentage difference from the average for the latest year
    average_annual_cost = latest_df['Annual Cost'].mean()
    latest_df['Difference from Average %'] = ((latest_df['Annual Cost'] - average_annual_cost) / average_annual_cost) * 100
    
    # Display results only for the latest year
    print(f"\nResults for the year {latest_year}:")
    print(f"Average annual cost of living: {average_annual_cost:.2f}")
    print("\nTop 10 cheapest cities (annual cost):")
    for i, r in enumerate(latest_results[:10], 1):
        print(f"{i}. {r['City']} ({r['Country']}): {r['Annual Cost']:.2f} ({((r['Annual Cost'] - average_annual_cost) / average_annual_cost * 100):.1f}% compared to the average)")
    
    print("\nTop 10 most expensive cities (annual cost):")
    for i, r in enumerate(latest_results[-10:][::-1], 1):
        print(f"{i}. {r['City']} ({r['Country']}): {r['Annual Cost']:.2f} ({((r['Annual Cost'] - average_annual_cost) / average_annual_cost * 100):.1f}% compared to the average)")
    
    
    # Helper function to convert NumPy types to native Python types
    def json_serializable(obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    # Convert all values to JSON serializable types
    serializable_results = []
    for result in latest_results:
        serializable_result = {}
        for key, value in result.items():
            if key == 'Cost Breakdown':
                serializable_breakdown = {}
                for cat, cost in value.items():
                    serializable_breakdown[cat] = json_serializable(cost)
                serializable_result[key] = serializable_breakdown
            else:
                serializable_result[key] = json_serializable(value)
        serializable_results.append(serializable_result)
    
    # Save breakdown details in a JSON file (only for the latest year)
    breakdown_file = os.path.join(data_dir, f'cost_breakdown_{latest_year}.json')
    with open(breakdown_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=4, ensure_ascii=False)
    print(f"Cost breakdown by category for the year {latest_year} saved in {breakdown_file}")
