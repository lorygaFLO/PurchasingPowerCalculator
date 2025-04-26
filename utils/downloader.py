import os
import pandas as pd
from datetime import datetime
from utils.scraper import get_cost_of_living_data
from utils.constants import BASEPATH


def download_historical_data(start_year, end_year):
    """
    Scarica i dati storici sul costo della vita da Numbeo per un intervallo di anni.
    
    Args:
        start_year (int): L'anno di inizio per il download dei dati
        end_year (int): L'anno di fine per il download dei dati
        
    Returns:
        pandas.DataFrame: DataFrame combinato con tutti i dati scaricati, o None se nessun dato è stato scaricato
    """
    # Creiamo una lista per memorizzare i DataFrame di ogni anno
    all_data_frames = []
    
    for year in range(end_year, start_year - 1, -1):
        try:
            print(f"Fetching data for year {year}...")
            data = get_cost_of_living_data(year)
            
            # Aggiungiamo una colonna 'year' al DataFrame
            data['year'] = year
            
            # Aggiungiamo il DataFrame alla lista
            all_data_frames.append(data)
            
            print(f"Data for year {year} fetched successfully")
            
        except Exception as e:
            print(f"Failed to fetch data for year {year}: {str(e)}")
            print("Stopping historical data collection")
            break
    
    # Combiniamo tutti i DataFrame in uno solo
    if all_data_frames:
        return pd.concat(all_data_frames, ignore_index=True)
    else:
        return None