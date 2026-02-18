import pandas as pd
import os

file_path = "3_Bike_Thefts_FINAL_EXCEL.xlsx"

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
else:
    try:
        df = pd.read_excel(file_path, nrows=5)
        print("Columns:")
        print(df.columns.tolist())
        print("\nData Types:")
        print(df.dtypes)
        print("\nFirst 2 rows:")
        print(df.head(2))
    except Exception as e:
        print(f"Error reading Excel file: {e}")
