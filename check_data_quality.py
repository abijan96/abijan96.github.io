import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def get_cell_source(cell):
    return ''.join(cell['source'])

print("="*80)
print("DATA QUALITY CHECKS - DETAILED REVIEW")
print("="*80)

# Check cells 12-28 for airport_codes data quality
print("\n>>> AIRPORTS DATA QUALITY")
print("\nCell 13 (shape/info):")
print(get_cell_source(nb['cells'][13])[:500])

print("\nCell 16 (filtering):")
print(get_cell_source(nb['cells'][16]))

print("\nCell 20 (null check):")
print(get_cell_source(nb['cells'][20]))

print("\nCell 22 (duplicates):")
print(get_cell_source(nb['cells'][22]))

# Check cells 29-53 for flights data quality
print("\n>>> FLIGHTS DATA QUALITY")
print("\nCell 30 (shape/info):")
print(get_cell_source(nb['cells'][30])[:500])

print("\nCell 31 (cancelled filter):")
print(get_cell_source(nb['cells'][31]))

print("\nCell 40 (duplicates check):")
print(get_cell_source(nb['cells'][40]))

print("\nCell 41 (duplicates removal):")
print(get_cell_source(nb['cells'][41]))

print("\nCell 46 (missing values check):")
print(get_cell_source(nb['cells'][46]))

print("\nCell 48 (missing values visualization):")
print(get_cell_source(nb['cells'][48])[:500])

print("\nCell 49 (median imputation):")
print(get_cell_source(nb['cells'][49]))

# Check cells 54-73 for tickets data quality
print("\n>>> TICKETS DATA QUALITY")
print("\nCell 55 (shape/info):")
print(get_cell_source(nb['cells'][55])[:500])

print("\nCell 57 (roundtrip filter):")
print(get_cell_source(nb['cells'][57]))

print("\nCell 62 (duplicates check):")
print(get_cell_source(nb['cells'][62]))

print("\nCell 63 (duplicates removal):")
print(get_cell_source(nb['cells'][63]))

print("\nCell 64 (null check):")
print(get_cell_source(nb['cells'][64]))

print("\nCell 71 (median imputation):")
print(get_cell_source(nb['cells'][71]))

print("\n" + "="*80)
print("CHECKING FOR DOCUMENTED INSIGHTS")
print("="*80)

# Cell 24 - Airport remarks
print("\nCell 24 - Airport Remarks:")
print(get_cell_source(nb['cells'][24]))

# Cell 45 - Flights observations
print("\nCell 45 - Flights Observations:")
print(get_cell_source(nb['cells'][45]))

# Cell 50 - Flights missing value observations
print("\nCell 50 - Flights Missing Values:")
print(get_cell_source(nb['cells'][50]))

# Cell 66 - Tickets observations
print("\nCell 66 - Tickets Observations:")
print(get_cell_source(nb['cells'][66]))

# Cell 69 - Overall data quality assessment
print("\nCell 69 - Data Quality Assessment:")
print(get_cell_source(nb['cells'][69]))
