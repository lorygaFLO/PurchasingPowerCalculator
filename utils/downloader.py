import os
import pandas as pd
from datetime import datetime
from utils.scraper import get_data
from utils.constants import BASEPATH


def download_historical_data(start_year, end_year):
    """
    Scarica i dati storici sul costo della vita e i guadagni annuali in un'unica operazione.
    """
    all_data_frames = []
    
    for year in range(end_year, start_year - 1, -1):
        try:
            print(f"Fetching combined cost of living and income data for year {year}...")
            combined_data = get_data(year)
            
            if combined_data is not None:
                # Aggiungi l'anno ai dati
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