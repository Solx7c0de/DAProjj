import pandas as pd
import os
from datetime import datetime

def clean_crash_cost_excel(file_path: str):
    df = pd.read_excel(file_path, sheet_name='schedule')

    # Normalize columns
    df.columns = df.columns.str.strip().str.title()
    df.rename(columns={'Activity Id': 'Activity'}, inplace=True)

    # Clean Predecessors
    nulls = ['none', 'nil', '-', '', ' ']
    df['Predecessors'] = df['Predecessors'].replace(nulls, '', regex=True).fillna('')
    df['Predecessors'] = df['Predecessors'].apply(lambda x: [i.strip() for i in str(x).split(',')] if x else [])
    df = df.explode('Predecessors')
    df['Predecessors'] = df['Predecessors'].replace('', None)

    # Set Duration as Most Likely Time
    df['Duration'] = df['Mostlikely'] if 'Mostlikely' in df.columns else df['Most Likely']
    
    # Save to processed with timestamp
    os.makedirs('data/processed', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/processed/crash_cleaned_v1_{timestamp}.csv"
    df.to_csv(filename, index=False)

    print(f"✅ Crash-ready cleaned data saved to: {filename}")
    return df
