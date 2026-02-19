import pandas as pd
import json
import os
from datetime import datetime

def process_data(file_path):
    print(f"Loading data from {file_path} using pandas...")
    
    # Load the Excel file using pandas and calamine engine
    try:
        # We use calamine engine as requested to avoid openpyxl
        df = pd.read_excel(file_path, sheet_name='2023 - 2025 EN', engine='calamine')
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        # Try without explicit engine if calamine fails, maybe default works
        try:
            df = pd.read_excel(file_path, sheet_name='2023 - 2025 EN')
        except:
            return None

    # Mapping for column renaming
    col_map = {
        'Created on': 'created_on',
        'Start date': 'start_date',
        'Start hour': 'start_hour',
        'End date': 'end_date',
        'End hour': 'end_hour',
        'LOR': 'lor',
        'Financial damage': 'damage',
        'Attempt': 'attempt',
        'Type of bicycle': 'bike_type',
        'Offence type': 'offence_type',
        'Record reason': 'record_reason'
    }
    
    # Rename columns that exist
    df = df.rename(columns=col_map)
    
    # Mapping for Berlin Districts based on LOR prefix
    district_map = {
        '01': 'Mitte',
        '02': 'Friedrichshain-Kreuzberg',
        '03': 'Pankow',
        '04': 'Charlottenburg-Wilmersdorf',
        '05': 'Spandau',
        '06': 'Steglitz-Zehlendorf',
        '07': 'Tempelhof-Schöneberg',
        '08': 'Neukölln',
        '09': 'Treptow-Köpenick',
        '10': 'Marzahn-Hellersdorf',
        '11': 'Lichtenberg',
        '12': 'Reinickendorf'
    }

    # Normalize Bike Types
    bike_type_map = {
        "Men's bike": "Mens bicycle",
        "Women's Bicycle": "Womens bicycle",
        "various bicycles": "Various bicycles",
        "various bicycle": "Various bicycles"
    }

    # Drop rows without start_date
    df = df.dropna(subset=['start_date'])
    
    # Clean Dates
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df = df.dropna(subset=['start_date'])

    # Process LOR to District
    def get_district(lor):
        lor_str = str(lor).split('.')[0].zfill(8)
        district_id = lor_str[0:2]
        return district_map.get(district_id, 'Unknown')

    df['district'] = df['lor'].apply(get_district)
    
    # Normalize Bike Type
    df['bike_type'] = df['bike_type'].map(bike_type_map).fillna(df['bike_type'])
    
    # Clean Damage
    df['damage'] = pd.to_numeric(df['damage'], errors='coerce')
    
    # Handle missing damage with median
    median_damage = df['damage'].median()
    df['damage'] = df['damage'].fillna(median_damage)

    # Add helper columns
    df['year'] = df['start_date'].dt.year
    df['month'] = df['start_date'].dt.month
    df['weekday'] = df['start_date'].dt.day_name()
    
    # Format date for JSON
    df['start_date_str'] = df['start_date'].dt.strftime('%Y-%m-%d')
    
    # Prepare output data
    output_cols = ['start_date_str', 'start_hour', 'district', 'damage', 'bike_type', 'offence_type', 'year', 'month', 'weekday']
    # Final cleanup to match JSON format
    clean_df = df[output_cols].copy()
    clean_df = clean_df.rename(columns={'start_date_str': 'start_date'})
    
    # Convert to list of dicts
    clean_data = clean_df.to_dict(orient='records')

    # Save clean data
    os.makedirs('data', exist_ok=True)
    with open('data/thefts_clean.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    
    # Save dimension tables
    dimensions = {
        'districts': sorted(df['district'].unique().tolist()),
        'bike_types': sorted(df['bike_type'].dropna().unique().tolist()),
        'offence_types': sorted(df['offence_type'].dropna().unique().tolist()),
        'years': sorted(df['year'].unique().tolist())
    }
    
    with open('data/dimensions.json', 'w') as f:
        json.dump(dimensions, f, indent=2)
        
    print(f"Processed {len(clean_data)} records.")
    print("Data Agent: Cleaning and standardization complete.")
    return clean_data

if __name__ == "__main__":
    process_data("3_Bike_Thefts_FINAL_EXCEL.xlsx")
