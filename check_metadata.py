import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def get_cell_source(cell):
    return ''.join(cell['source'])

print("="*80)
print("CHECKING FOR METADATA/FIELD DOCUMENTATION")
print("="*80)

# Look at cell 85 again which has all the field calculations
print("\n>>> CELL 85 - Cost/Revenue Field Creation")
source = get_cell_source(nb['cells'][85])
print(source)

# Check if there are any comments explaining the fields
print("\n" + "="*80)
print("CHECKING FOR COMMENTS IN CODE CELLS")
print("="*80)

comment_cells = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = get_cell_source(cell)
        # Count comment lines
        lines = source.split('\n')
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        if comment_lines and i >= 75:  # Focus on analysis section
            comment_cells.append(i)
            print(f"\nCell {i}: {len(comment_lines)} comment lines")
            for comment in comment_lines[:10]:  # Show first 10
                print(f"  {comment}")

# Check cell 84 which had the cost assumptions
print("\n" + "="*80)
print("CELL 84 - COST ASSUMPTIONS (Serves as metadata)")
print("="*80)
print(get_cell_source(nb['cells'][84]))

# Check for any data dictionary or glossary
print("\n" + "="*80)
print("SEARCHING FOR DATA DICTIONARY OR GLOSSARY")
print("="*80)
found_dict = False
for i, cell in enumerate(nb['cells']):
    source = get_cell_source(cell).lower()
    if any(kw in source for kw in ['dictionary', 'glossary', 'field definition', 'column description']):
        print(f"\nFound in Cell {i}:")
        print(get_cell_source(nb['cells'][i])[:500])
        found_dict = True

if not found_dict:
    print("No explicit data dictionary found")

# Check cell 91 for route metrics definitions
print("\n" + "="*80)
print("CELL 91 - METRIC DEFINITIONS")
print("="*80)
print(get_cell_source(nb['cells'][91]))
