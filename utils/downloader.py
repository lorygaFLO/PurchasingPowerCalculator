import os
import pandas as pd
from datetime import datetime
from utils.scraper import get_cost_of_living_data, get_annual_income_data
from utils.constants import BASEPATH


def download_historical_data(start_year, end_year):
    """
    Scarica i dati storici sul costo della vita e i guadagni annuali.
    """
    all_data_frames = []
    
    for year in range(end_year, start_year - 1, -1):
        try:
            print(f"Fetching cost of living data for year {year}...")
            cost_data = get_cost_of_living_data(year)
            
            print(f"Fetching annual income data for year {year}...")
            income_data = get_annual_income_data(year)
            
            if cost_data is not None and income_data is not None:
                # Unisci i dati sui costi e i guadagni
                combined_data = pd.merge(cost_data, income_data, on=['City'], how='inner')
                combined_data['year'] = year
                all_data_frames.append(combined_data)
                
                print(f"Data for year {year} fetched successfully")
            else:
                print(f"Data for year {year} is incomplete, skipping...")
        except Exception as e:
            print(f"Failed to fetch data for year {year}: {str(e)}")
            break
    
    if all_data_frames:
        return pd.concat(all_data_frames, ignore_index=True)
    else:
        return None