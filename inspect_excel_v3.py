import shutil
import os
import pandas as pd

src = r'c:\Users\saina\OneDrive\Documents\Bike Theft\MDH-project-Analytical-Application-Team-B\berlin_LOR_hierarchy.xlsx'
dst = r'c:\Users\saina\OneDrive\Documents\Bike Theft\MDH-project-Analytical-Application-Team-B\temp_hierarchy.xlsx'

try:
    shutil.copy(src, dst)
    print(f"Copied {src} to {dst}")
    
    # Now try to read the copy
    df = pd.read_excel(dst)
    print("Columns:", df.columns.tolist())
    print(df.head())
    
    # Look for district names
    districts = set()
    for col in df.columns:
        # Check if column values look like districts
        unique_vals = df[col].dropna().unique()
        for v in unique_vals:
            v_str = str(v)
            if v_str in [
                "Charlottenburg-Wilmersdorf", "Friedrichshain-Kreuzberg", "Lichtenberg", 
                "Marzahn-Hellersdorf", "Mitte", "Neukölln", "Pankow", 
                "Reinickendorf", "Spandau", "Steglitz-Zehlendorf", 
                "Tempelhof-Schöneberg", "Treptow-Köpenick"
            ]:
                districts.add(v_str)
    
    print("\nDistricts found in Excel copy:")
    for d in sorted(list(districts)):
        print(f"- {d}")
        
    # Also check for LOR prefix mapping
    # Assuming there's a column with LOR (ID) and a column with District Name
    lor_col = None
    district_name_col = None
    
    for col in df.columns:
        if 'lor' in col.lower() or 'id' in col.lower() or 'kennzahl' in col.lower():
            lor_col = col
        if 'bezirk' in col.lower() or 'district' in col.lower():
            district_name_col = col
            
    if lor_col and district_name_col:
        print(f"\nFound LOR column '{lor_col}' and District column '{district_name_col}'")
        # Extract the first 2 digits of LOR and the district name
        df['prefix'] = df[lor_col].astype(str).str.zfill(8).str[:2]
        mapping = df.groupby('prefix')[district_name_col].first().to_dict()
        print("Mapping from Excel:")
        for k, v in sorted(mapping.items()):
            print(f"  '{k}': '{v}'")
            
    os.remove(dst)
except Exception as e:
    print(f"Error: {e}")
    if os.path.exists(dst):
        os.remove(dst)
