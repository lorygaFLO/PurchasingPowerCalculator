# -*- coding: utf-8 -*-
"""
Module for scraping cost of living data from Numbeo.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def get_cost_of_living_data(year=2023):
    """
    Downloads cost of living data from Numbeo for the specified year.
    
    Args:
        year (int): The year for which to download data (default: 2023)
        
    Returns:
        pandas.DataFrame: DataFrame containing cost of living data
    """
    # URL di Numbeo con tutti gli item ID per le diverse categorie di spesa
    url = f'https://www.numbeo.com/cost-of-living/historical-prices-by-country?displayCurrency=EUR&year={year}&itemId=101&itemId=100&itemId=228&itemId=224&itemId=60&itemId=66&itemId=64&itemId=62&itemId=110&itemId=118&itemId=121&itemId=14&itemId=19&itemId=17&itemId=15&itemId=11&itemId=16&itemId=113&itemId=9&itemId=12&itemId=8&itemId=119&itemId=111&itemId=112&itemId=115&itemId=116&itemId=13&itemId=27&itemId=26&itemId=29&itemId=28&itemId=114&itemId=6&itemId=4&itemId=5&itemId=3&itemId=2&itemId=1&itemId=7&itemId=105&itemId=106&itemId=44&itemId=40&itemId=42&itemId=24&itemId=20&itemId=18&itemId=109&itemId=108&itemId=107&itemId=206&itemId=25&itemId=30&itemId=33&itemId=34'
            
    try:
        # Download the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Raise an exception for HTTP errors
        
        # Usa StringIO per evitare il FutureWarning
        html_io = StringIO(page.text)
        
        # Extract tables from the page
        df_prices = pd.read_html(html_io)[-1]
        
        # Remove the 'Rank' column that we don't need
        if 'Rank' in df_prices.columns:
            df_prices = df_prices.drop("Rank", axis=1)
        
        return df_prices
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None