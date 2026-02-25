import json
import sys
import re

# Set UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Load the notebook
with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def get_cell_source(cell):
    """Get cell source as string"""
    return ''.join(cell['source'])

def print_section(title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

# Basic stats
print_section("NOTEBOOK OVERVIEW")
print(f"Total cells: {len(nb['cells'])}")
print(f"Markdown cells: {sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')}")
print(f"Code cells: {sum(1 for c in nb['cells'] if c['cell_type'] == 'code')}")

# Extract structure
print_section("NOTEBOOK STRUCTURE")
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = get_cell_source(cell)
        for line in source.split('\n'):
            if line.strip().startswith('#'):
                # Clean special characters
                cleaned = line.strip().encode('ascii', 'ignore').decode('ascii')
                print(f"Cell {i}: {cleaned}")

# Check Q1: Top 10 busiest routes
print_section("Q1: TOP 10 BUSIEST ROUTES - VERIFICATION")
q1_cells = []
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'question 1' in source or 'busiest' in source:
        if 'route' in source:
            q1_cells.append(i)
            print(f"\nFound in Cell {i} ({cell['cell_type']})")
            preview = get_cell_source(cell)[:400].encode('ascii', 'ignore').decode('ascii')
            print(preview)

print(f"\nQ1 Status: {'FOUND' if q1_cells else 'NOT FOUND'}")

# Check Q2: Top 10 profitable routes
print_section("Q2: TOP 10 PROFITABLE ROUTES - VERIFICATION")
q2_cells = []
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'question 2' in source or ('profitable' in source and 'route' in source):
        q2_cells.append(i)
        print(f"\nFound in Cell {i} ({cell['cell_type']})")
        preview = get_cell_source(cell)[:400].encode('ascii', 'ignore').decode('ascii')
        print(preview)

print(f"\nQ2 Status: {'FOUND' if q2_cells else 'NOT FOUND'}")

# Check Q3: 5 recommended routes
print_section("Q3: 5 RECOMMENDED ROUTES - VERIFICATION")
q3_cells = []
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'question 3' in source or ('recommend' in source and 'route' in source):
        q3_cells.append(i)
        print(f"\nFound in Cell {i} ({cell['cell_type']})")
        preview = get_cell_source(cell)[:400].encode('ascii', 'ignore').decode('ascii')
        print(preview)

print(f"\nQ3 Status: {'FOUND' if q3_cells else 'NOT FOUND'}")

# Check Q4: Breakeven
print_section("Q4: BREAKEVEN ANALYSIS - VERIFICATION")
q4_cells = []
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'question 4' in source or 'breakeven' in source or 'break-even' in source or 'break even' in source:
        q4_cells.append(i)
        print(f"\nFound in Cell {i} ({cell['cell_type']})")
        preview = get_cell_source(cell)[:400].encode('ascii', 'ignore').decode('ascii')
        print(preview)

print(f"\nQ4 Status: {'FOUND' if q4_cells else 'NOT FOUND'}")

# Check Q5: KPIs
print_section("Q5: KPIs - VERIFICATION")
q5_cells = []
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if 'question 5' in source or 'kpi' in source:
        q5_cells.append(i)
        print(f"\nFound in Cell {i} ({cell['cell_type']})")
        preview = get_cell_source(cell)[:400].encode('ascii', 'ignore').decode('ascii')
        print(preview)

print(f"\nQ5 Status: {'FOUND' if q5_cells else 'NOT FOUND'}")

# Data Quality Checks
print_section("DATA QUALITY CHECKS")
dq_keywords = ['null', 'missing', 'duplicat', 'isnull', 'isna', 'quality', 'cleaning']
dq_cells = set()
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if any(kw in source for kw in dq_keywords):
        if cell['cell_type'] == 'code' or 'quality' in source:
            dq_cells.add(i)

print(f"Cells with data quality checks: {len(dq_cells)}")
print(f"Cells: {sorted(list(dq_cells))[:20]}")

# Functions
print_section("REUSABLE FUNCTIONS")
functions = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = get_cell_source(cell)
        matches = re.findall(r'def\s+(\w+)\s*\(', source)
        for func in matches:
            functions.append((i, func))
            print(f"Cell {i}: def {func}()")

print(f"\nTotal functions: {len(functions)}")

# Visualizations
print_section("VISUALIZATIONS")
viz_count = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = get_cell_source(cell)
        if any(kw in source for kw in ['plt.', '.plot(', 'fig', 'chart', 'sns.']):
            viz_count += 1

print(f"Visualization cells found: {viz_count}")

# Cost calculations
print_section("COST/REVENUE CALCULATIONS")
cost_cells = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = get_cell_source(cell)
        # Look for the specific cost constants
        if '8' in source and ('mile' in source.lower() or 'fuel' in source.lower()):
            cost_cells.append(i)
            print(f"\nCell {i}: Fuel/oil/maintenance cost found")
        if '1.18' in source:
            cost_cells.append(i)
            print(f"Cell {i}: Depreciation cost found")
        if '5000' in source or '10000' in source:
            if 'airport' in source.lower() or 'fee' in source.lower():
                cost_cells.append(i)
                print(f"Cell {i}: Airport fees found")
        if '75' in source and 'delay' in source.lower():
            cost_cells.append(i)
            print(f"Cell {i}: Delay cost found")
        if '35' in source and 'bag' in source.lower():
            cost_cells.append(i)
            print(f"Cell {i}: Baggage revenue found")

print(f"\nCells with cost/revenue calculations: {len(set(cost_cells))}")

# Summary
print_section("EVALUATION SUMMARY")
print(f"Q1 (Busiest Routes): {'YES' if q1_cells else 'NO'}")
print(f"Q2 (Profitable Routes): {'YES' if q2_cells else 'NO'}")
print(f"Q3 (Recommendations): {'YES' if q3_cells else 'NO'}")
print(f"Q4 (Breakeven): {'YES' if q4_cells else 'NO'}")
print(f"Q5 (KPIs): {'YES' if q5_cells else 'NO'}")
print(f"Data Quality Checks: {len(dq_cells)} cells")
print(f"Functions Defined: {len(functions)}")
print(f"Visualizations: {viz_count} cells")
print(f"Cost Calculations: {len(set(cost_cells))} cells")
