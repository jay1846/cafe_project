import pandas as pd
import os
    
def run_analysis():
    # Set the absolute path for the data file
    home = os.path.expanduser('~')
    file_path = os.path.join(home, 'cafe_project/data/report-month-2026-01-95286.csv')

    if not os.path.exists(file_path):
        print(f"[-] Error: File not found at {file_path}")
        return

    try:
        # Step 1: Detect the correct header row dynamically
        # Some CSV files have metadata at the top. We need to find the actual table header.
        header_idx = -1
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # We search for the row containing essential column names
                # Using lowercase comparison to avoid case-sensitivity issues
                lowered_line = line.lower()
                if 'plu' in lowered_line and 'anzahl' in lowered_line and 'total' in lowered_line:
                    header_idx = i
                    break
        if header_idx == -1:
            print("[-] Error: Could not find the data header in the CSV file.")
            return

        print(f"[+] Header detected at row: {header_idx + 1}")
        df = pd.read_csv(file_path, 
                         sep=';', 
                         encoding='utf-8-sig', 
                         skiprows=header_idx,
                         nrows=90,engine='python')

        # Step 2: Load the data starting from the detected header
        # utf-8-sig handles the Byte Order Mark (BOM) often found in Excel-generated CSVs
        df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', skiprows=header_idx)

        # Step 3: Data Cleaning
        # Remove leading/trailing whitespaces from column names
        df.columns = [str(col).strip() for col in df.columns]

        # Convert numeric columns (Handling German format: 1.234,56 -> 1234.56)
        for col in ['Anzahl', 'Total']:
            if col in df.columns:
                # Replace comma with dot and remove thousands separator if exists
                df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows where essential data is missing (e.g., footer or separator rows)
        df = df.dropna(subset=['Anzahl', 'Total'])
        # Filter out rows with zero total to focus on actual sales
        df = df[df['Total'] > 0]

        # Step 4: Display the Analysis Results
        print("\n" + "="*50)
        print("   Kiez Kaffee Kraft - Monthly Sales Report")
        print("="*50)
        print(f"[*] Total Items Sold (Unique): {len(df)}")
        print(f"[*] Total Quantity Sold    : {df['Anzahl'].sum():,.0f} units")
        print(f"[*] Total Gross Revenue    : €{df['Total'].sum():,.2f}")
        print("-" * 50)

        # Step 5: Identify Top 5 Performing Items
        print("TOP 5 Best Sellers by Revenue:")
        # Identify the name column (usually 'Warengruppe' or the first column)
        name_col = 'Warengruppe' if 'Warengruppe' in df.columns else df.columns[0]
        
        top_5 = df.sort_values(by='Total', ascending=False).head(5)
        for _, row in top_5.iterrows():
            revenue_share = (row['Total'] / df['Total'].sum()) * 100
            print(f"- {str(row[name_col]):<25}: €{row['Total']:>8.2f} ({revenue_share:>4.1f}%)")
        print("="*50)

    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_analysis()
