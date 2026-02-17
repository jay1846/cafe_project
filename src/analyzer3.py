import csv
import os
import matplotlib.pyplot as plt

def run_analysis():
    home = os.path.expanduser('~')
    file_path = os.path.join(home, 'cafe_project/data/report-month-2026-01-95286.csv')
    output_image = os.path.join(home, 'cafe_project/sales_chart.png')
    
    if not os.path.exists(file_path):
        print("[-] Error: File not found")
        return

    sales_data = []
    EXCLUDE_KEYWORDS = ["visa", "mastercard", "maestro", "bar", "speisen", "sonstiges", "total", "theke", "getränke"]

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) < 4: continue
                try:
                    name = row[0].strip()
                    if not name or any(key in name.lower() for key in EXCLUDE_KEYWORDS): continue
                    
                    rev = float(row[3].strip())
                    if rev > 15000: continue
                    
                    sales_data.append({"name": name, "revenue": rev})
                except: continue

        # Sort and take top 10 for the chart
        top_10 = sorted(sales_data, key=lambda x: x['revenue'], reverse=True)[:10]
        
        # --- Visualization Section ---
        names = [item['name'] for item in top_10]
        revenues = [item['revenue'] for item in top_10]

        plt.figure(figsize=(12, 8))
        bars = plt.barh(names, revenues, color='skyblue')
        plt.xlabel('Revenue (€)')
        plt.title('Top 10 Menu Items by Revenue - Jan 2026')
        plt.gca().invert_yaxis()  # Highest revenue at the top

        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 5, bar.get_y() + bar.get_height()/2, f'€{width:,.0f}', va='center')

        plt.tight_layout()
        plt.savefig(output_image) # Save as image
        print(f"[+] Success! Chart saved to: {output_image}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    run_analysis()
