import pandas as pd
import sys

xl = pd.ExcelFile(r'C:\Users\USER\Downloads\Cake Pricing - Karthika Sravanthi.xlsx')
print('Sheet names:', xl.sheet_names)
print('\n')

for sheet in xl.sheet_names:
    print(f'\n=== Sheet: {sheet} ===\n')
    df = pd.read_excel(xl, sheet)
    print(df.to_string())
    print('\n')
