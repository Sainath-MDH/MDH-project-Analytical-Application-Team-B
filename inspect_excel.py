import pandas as pd

try:
    xl = pd.ExcelFile(r'c:\Users\saina\OneDrive\Documents\Bike Theft\MDH-project-Analytical-Application-Team-B\berlin_LOR_hierarchy.xlsx')
    print("Sheet names:", xl.sheet_names)
    df = xl.parse(xl.sheet_names[0])
    print("Columns:", df.columns.tolist())
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
