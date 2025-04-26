import os
import pandas as pd
import json
import numpy as np
from datetime import datetime
from utils.constants import BASEPATH

def calculate_cost_of_living_by_habits(data, data_dir):
    """
    Calcola il costo della vita in tutti i paesi basato sulle abitudini di consumo dell'utente
    e genera report per anno
    
    Args:
        data (pandas.DataFrame): DataFrame con i dati sul costo della vita
        data_dir (str): Percorso della directory dei dati
    """
    # Carica le abitudini di consumo dell'utente
    habits_file = os.path.join(data_dir, 'user_consumption_habits.json')
    
    if not os.path.exists(habits_file):
        raise FileNotFoundError("File delle abitudini di consumo non trovato. Controlla perché...")
    
    with open(habits_file, 'r', encoding='utf-8') as f:
        user_habits = json.load(f)
    
    # Ottieni tutti gli anni disponibili nei dati
    available_years = sorted(data['year'].unique())
    latest_year = max(available_years)
    
    print(f"\nCalcolo del costo della vita annuale basato sulle tue abitudini di consumo mensili per tutte le città disponibili...")
    
    # Crea un DataFrame per memorizzare i risultati di tutti gli anni
    all_years_results = []
    
    # Per ogni anno disponibile nei dati
    for year in available_years:
        year_data = data[data['year'] == year]
        
        # Raggruppa per città per evitare duplicati
        cities_data = year_data.groupby('City').first().reset_index()
        
        for _, city_row in cities_data.iterrows():
            city_name = city_row['City']
            country_name = city_row['Country'] if 'Country' in city_row else "N/A"
            
            annual_cost = 0.0
            city_breakdown = {}
            
            for category, amount in user_habits.items():
                if category in city_row and pd.notna(city_row[category]) and amount > 0:
                    try:
                        # Converti i valori in float per assicurarti che siano numerici
                        category_value = float(city_row[category])
                        amount_value = float(amount)
                        
                        # Moltiplica il valore di riferimento per la quantità consumata mensilmente
                        monthly_category_cost = category_value * amount_value
                        annual_category_cost = monthly_category_cost * 12  # Annualizza il costo
                        
                        annual_cost += annual_category_cost
                        city_breakdown[category] = annual_category_cost
                    except (ValueError, TypeError) as e:
                        # Salta questa categoria se la conversione fallisce, ma registra l'errore
                        if year == latest_year:  # Mostra errori solo per l'ultimo anno
                            print(f"Errore nell'elaborazione della categoria '{category}' per la città '{city_name}': {e}")
                            print(f"Valore nei dati: {city_row[category]}, Tipo: {type(city_row[category])}")
                            print(f"Quantità nelle abitudini: {amount}, Tipo: {type(amount)}")
            
            if annual_cost > 0:  # Solo se abbiamo calcolato un costo
                all_years_results.append({
                    'City': city_name,
                    'Country': country_name,
                    'Year': int(year),  # Convert numpy.int64 to Python int
                    'Annual Cost': float(annual_cost),  # Ensure it's a Python float
                    'Cost Breakdown': city_breakdown
                })
    
    # Crea un DataFrame con i risultati di tutti gli anni
    all_years_df = pd.DataFrame([{
        'City': r['City'], 
        'Country': r['Country'],
        'Year': r['Year'],
        'Annual Cost': r['Annual Cost']
    } for r in all_years_results])
    
    # Salva i risultati di tutti gli anni in un unico file CSV
    all_years_file = os.path.join(data_dir, 'cost_breakdown.csv')
    all_years_df = all_years_df.sort_values(by='Annual Cost', ascending=True)
    all_years_df.to_csv(all_years_file, index=False, sep=';', decimal=',')
    print(f"\nRisultati completi per tutti gli anni salvati in {all_years_file}")
    
    # Filtra i risultati solo per l'ultimo anno
    latest_results = [r for r in all_years_results if r['Year'] == int(latest_year)]
    latest_results.sort(key=lambda x: x['Annual Cost'])
    
    # Crea un DataFrame con i risultati dell'ultimo anno
    latest_df = all_years_df[all_years_df['Year'] == latest_year]
    
    # Calcola la differenza percentuale rispetto alla media per l'ultimo anno
    average_annual_cost = latest_df['Annual Cost'].mean()
    latest_df['Difference from Average %'] = ((latest_df['Annual Cost'] - average_annual_cost) / average_annual_cost) * 100
    
    # Mostra i risultati solo per l'ultimo anno
    print(f"\nRisultati per l'anno {latest_year}:")
    print(f"Costo della vita annuale medio: {average_annual_cost:.2f}")
    print("\nTop 10 città più economiche (costo annuale):")
    for i, r in enumerate(latest_results[:10], 1):
        print(f"{i}. {r['City']} ({r['Country']}): {r['Annual Cost']:.2f} ({((r['Annual Cost'] - average_annual_cost) / average_annual_cost * 100):.1f}% rispetto alla media)")
    
    print("\nTop 10 città più costose (costo annuale):")
    for i, r in enumerate(latest_results[-10:][::-1], 1):
        print(f"{i}. {r['City']} ({r['Country']}): {r['Annual Cost']:.2f} ({((r['Annual Cost'] - average_annual_cost) / average_annual_cost * 100):.1f}% rispetto alla media)")
    
    # Funzione helper per convertire tipi NumPy in tipi Python nativi
    def json_serializable(obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    # Converti tutti i valori in tipi serializzabili JSON
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
    
    # Salva i dettagli di breakdown in un file JSON (solo per l'ultimo anno)
    breakdown_file = os.path.join(data_dir, f'cost_breakdown_{latest_year}.json')
    with open(breakdown_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=4, ensure_ascii=False)
    print(f"Dettaglio dei costi per categoria per l'anno {latest_year} salvato in {breakdown_file}")
