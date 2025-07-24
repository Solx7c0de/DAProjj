import pandas as pd
import sys
import os

# Add scripts/ directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'scripts')))

# Step 1: Load the raw task data
df_raw = pd.read_excel('D:/CODE/DAProj/data/raw/tasks_raw_v1.xlsx', sheet_name='schedule')

# Step 2: Rename columns for consistency
df_raw.columns = df_raw.columns.str.strip().str.title()

# Step 3: Handle null or placeholder values in 'Predecessors'
null_values = ['none', 'nil', 'None', 'Nil', 'NIL', '-', ' ']
df_raw['Predecessors'] = df_raw['Predecessors'].replace(null_values, '', regex=True).fillna('')

# Step 4: Convert to list if multiple predecessors exist
df_raw['Predecessors'] = df_raw['Predecessors'].apply(lambda x: [i.strip() for i in x.split(',')] if x else [])

# Step 5: Explode the list into separate rows
df_exploded = df_raw.explode('Predecessors')

# Step 6: Treat empty predecessors as None
df_exploded['Predecessors'] = df_exploded['Predecessors'].replace('', None)

# Step 7: Reset index and save cleaned version if needed
df_cleaned = df_exploded.reset_index(drop=True)

# Rename 'Activity Id' to 'Activity'
df_cleaned.rename(columns={'Activity Id': 'Activity'}, inplace=True)

# Set 'Duration' equal to the 'Most Probable Time' column
df_cleaned['Duration'] = df_cleaned['Most Likely Time']

df_cleaned.to_csv('data/processed/tasks_cleaned_v1.csv', index=False)

#ensures unique date and time assigned to each file pre processed.
import os
import glob
from datetime import datetime

# Step X: Save cleaned DataFrame with auto-version and timestamp
os.makedirs('data/processed', exist_ok=True)

# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Count existing versions
existing_files = glob.glob('data/processed/tasks_cleaned_v*.csv')
version = len(existing_files) + 1

# Compose filename
filename = f"data/processed/tasks_cleaned_v{version}_{timestamp}.csv"

# Save file
df_cleaned.to_csv(filename, index=False)

print(f"✅ Cleaned data saved as: {filename}")



from cpm_utils import build_activity_graph

G = build_activity_graph(df_cleaned)
print(G.nodes(data=True))
print(G.edges())