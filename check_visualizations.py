import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\USER\Desktop\Capital One\Abhigyan_ghosh_Capital_One_data_Challenge.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def get_cell_source(cell):
    return ''.join(cell['source'])

print("="*80)
print("VISUALIZATION ANALYSIS")
print("="*80)

viz_cells = [48, 49, 52, 72, 82, 86, 90, 94]

for cell_num in viz_cells:
    print(f"\n>>> CELL {cell_num}")
    source = get_cell_source(nb['cells'][cell_num])
    print(source[:800] if len(source) > 800 else source)
    print("-" * 80)
