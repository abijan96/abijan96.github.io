import json
import re

# Load the notebook
with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("CAPITAL ONE DATA CHALLENGE - NOTEBOOK ANALYSIS")
print("="*80)
print(f"\nTotal cells: {len(nb['cells'])}")
print(f"Markdown cells: {sum(1 for cell in nb['cells'] if cell['cell_type'] == 'markdown')}")
print(f"Code cells: {sum(1 for cell in nb['cells'] if cell['cell_type'] == 'code')}")

# Extract all markdown headers to understand structure
print("\n" + "="*80)
print("NOTEBOOK STRUCTURE (Headers)")
print("="*80)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        # Find headers
        for line in source.split('\n'):
            if line.strip().startswith('#'):
                print(f"Cell {i}: {line.strip()}")

# Search for key requirements
print("\n" + "="*80)
print("REQUIREMENT 1: TOP 10 BUSIEST ROUTES")
print("="*80)
found = False
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'busiest' in source.lower() or 'top 10' in source.lower():
        if 'route' in source.lower() or 'flight count' in source.lower():
            print(f"\nCell {i} ({cell['cell_type']}):")
            print(source[:500] if len(source) > 500 else source)
            found = True
if not found:
    print("NOT FOUND")

print("\n" + "="*80)
print("REQUIREMENT 2: TOP 10 MOST PROFITABLE ROUTES")
print("="*80)
found = False
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'profitable' in source.lower() or 'profit' in source.lower():
        if 'top' in source.lower() or 'revenue' in source.lower() or 'cost' in source.lower():
            print(f"\nCell {i} ({cell['cell_type']}):")
            print(source[:500] if len(source) > 500 else source)
            found = True
if not found:
    print("NOT FOUND")

print("\n" + "="*80)
print("REQUIREMENT 3: 5 RECOMMENDED ROUTES")
print("="*80)
found = False
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'recommend' in source.lower():
        if 'route' in source.lower() or 'invest' in source.lower():
            print(f"\nCell {i} ({cell['cell_type']}):")
            print(source[:500] if len(source) > 500 else source)
            found = True
if not found:
    print("NOT FOUND")

print("\n" + "="*80)
print("REQUIREMENT 4: BREAKEVEN ANALYSIS")
print("="*80)
found = False
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'breakeven' in source.lower() or 'break-even' in source.lower() or 'break even' in source.lower():
        print(f"\nCell {i} ({cell['cell_type']}):")
        print(source[:500] if len(source) > 500 else source)
        found = True
    elif '90' in source and ('million' in source.lower() or 'm' in source.lower()):
        if 'airplane' in source.lower() or 'aircraft' in source.lower() or 'cost' in source.lower():
            print(f"\nCell {i} ({cell['cell_type']}):")
            print(source[:500] if len(source) > 500 else source)
            found = True
if not found:
    print("NOT FOUND")

print("\n" + "="*80)
print("REQUIREMENT 5: KPIs")
print("="*80)
found = False
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'kpi' in source.lower() or 'key performance indicator' in source.lower():
        print(f"\nCell {i} ({cell['cell_type']}):")
        print(source[:500] if len(source) > 500 else source)
        found = True
    elif 'metric' in source.lower() and 'track' in source.lower():
        print(f"\nCell {i} ({cell['cell_type']}):")
        print(source[:500] if len(source) > 500 else source)
        found = True
if not found:
    print("NOT FOUND")

print("\n" + "="*80)
print("DATA QUALITY CHECKS")
print("="*80)
quality_checks = 0
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'null' in source.lower() or 'missing' in source.lower() or 'duplicat' in source.lower():
        if cell['cell_type'] == 'code':
            print(f"\nCell {i}:")
            print(source[:300] if len(source) > 300 else source)
            quality_checks += 1
    elif 'data quality' in source.lower() or 'data cleaning' in source.lower():
        print(f"\nCell {i} ({cell['cell_type']}):")
        print(source[:300] if len(source) > 300 else source)
        quality_checks += 1
    elif 'isnull' in source.lower() or 'isna' in source.lower():
        print(f"\nCell {i}:")
        print(source[:300] if len(source) > 300 else source)
        quality_checks += 1

print(f"\nTotal cells with quality checks: {quality_checks}")

print("\n" + "="*80)
print("FUNCTIONS (Reusability)")
print("="*80)
functions_found = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        # Find function definitions
        matches = re.findall(r'def\s+(\w+)\s*\(', source)
        if matches:
            for func in matches:
                print(f"\nCell {i}: Function '{func}'")
                print(source[:400] if len(source) > 400 else source)
                functions_found.append(func)

print(f"\nTotal functions defined: {len(functions_found)}")

print("\n" + "="*80)
print("VISUALIZATIONS")
print("="*80)
viz_count = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'plt.' in source or 'plot' in source or 'chart' in source.lower() or 'fig' in source:
            if 'import' not in source or 'matplotlib' in source or 'seaborn' in source or 'plotly' in source:
                print(f"\nCell {i}:")
                print(source[:300] if len(source) > 300 else source)
                viz_count += 1

print(f"\nTotal visualization cells: {viz_count}")

print("\n" + "="*80)
print("METADATA DOCUMENTATION")
print("="*80)
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'metadata' in source.lower() or 'data dictionary' in source.lower():
        print(f"\nCell {i} ({cell['cell_type']}):")
        print(source[:500] if len(source) > 500 else source)

print("\n" + "="*80)
print("COST CALCULATIONS")
print("="*80)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if any(keyword in source for keyword in ['8', '1.18', '5000', '10000', '75', '35']):
            if 'cost' in source.lower() or 'fee' in source.lower() or 'revenue' in source.lower():
                print(f"\nCell {i}:")
                print(source[:400] if len(source) > 400 else source)

print("\n" + "="*80)
print("END OF ANALYSIS")
print("="*80)
