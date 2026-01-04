import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def get_cell_source(cell):
    return ''.join(cell['source'])

def print_section(title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

# Detailed look at specific cells
print_section("DETAILED ANALYSIS")

# Cell 8 - Functions
print("\n>>> CELL 8: REUSABLE FUNCTIONS")
print(get_cell_source(nb['cells'][8]))

# Cell 11 - Data Quality overview
print("\n>>> CELL 11: DATA QUALITY HEADER")
print(get_cell_source(nb['cells'][11]))

# Cell 74 - Data Quality Summary
print("\n>>> CELL 74: DATA QUALITY SUMMARY")
print(get_cell_source(nb['cells'][74]))

# Cell 85 - Cost/Revenue calculations
print("\n>>> CELL 85: COST/REVENUE CALCULATIONS")
print(get_cell_source(nb['cells'][85]))

# Cell 81 - Q1 Answer
print("\n>>> CELL 81: Q1 CODE")
print(get_cell_source(nb['cells'][81]))

# Cell 84 - Q2 Setup
print("\n>>> CELL 84: Q2 ROUTE AGGREGATION")
print(get_cell_source(nb['cells'][84]))

# Cell 89 - Q3 Recommendations
print("\n>>> CELL 89: Q3 ROUTE METRICS")
print(get_cell_source(nb['cells'][89]))

# Cell 93 - Q4 Breakeven
print("\n>>> CELL 93: Q4 BREAKEVEN CALCULATION")
print(get_cell_source(nb['cells'][93]))

# Cell 97 - Q5 KPIs
print("\n>>> CELL 97: Q5 KPI RECOMMENDATIONS")
print(get_cell_source(nb['cells'][97]))

# Check metadata documentation
print_section("METADATA/DATA DICTIONARY CHECK")
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'metadata' in source or 'data dictionary' in source or 'field description' in source:
        print(f"\nCell {i}:")
        print(get_cell_source(nb['cells'][i]))

# Check for join function
print_section("JOIN FUNCTION CHECK")
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell)
    if 'def' in source and 'merge' in source.lower() or 'join' in source.lower():
        print(f"\nCell {i}:")
        print(source)

# Check cell 76 - merge strategy
print("\n>>> CELL 76: MERGE STRATEGY")
print(get_cell_source(nb['cells'][76]))

# Check cell 77 - actual merge code
print("\n>>> CELL 77: MERGE CODE")
print(get_cell_source(nb['cells'][77]))
