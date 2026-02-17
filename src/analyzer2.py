import csv
import os

def run_analysis():
    home = os.path.expanduser('~')
    file_path = os.path.join(home, 'cafe_project/data/report-month-2026-01-95286.csv')
    
    if not os.path.exists(file_path):
        print("[-] Error: File not found")
        return

    sales_data = []
    total_revenue = 0.0
    total_quantity = 0

    # Stronger filtering to remove Categories and Payment Methods
    EXCLUDE_KEYWORDS = [
            # Payment Methods
        "visa", "mastercard", "maestro", "bar", "barzahlung", "karte", "amex", "summe",
        # Categories / Subtotals
        "speisen", "sonstiges", "total", "theke", "getränke", "kaffee & chai", 
        "hafer heiss", "milch heiß", "kuchen", "snacks", "abfrage", "gesamt", "umsatz"
    ]

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            
            for row in reader:
                if len(row) < 4:
                    continue
                
                try:
                    name = row[0].strip()
                    qty_str = row[2].strip()
                    rev_str = row[3].strip()

                    if not name:
                        continue
                    
                    lower_name = name.lower()
                    # Skip if the name is in the exclusion list
                    if any(key == lower_name or key in lower_name for key in EXCLUDE_KEYWORDS):
                        continue

                    qty = int(qty_str)
                    rev = float(rev_str)
                    
                    # Additional safety: Skip very high amounts that look like totals
                    if rev > 15000:
                        continue

                    total_revenue += rev
                    total_quantity += qty
                    
                    sales_data.append({
                            "item_name": name,
                        "revenue": rev,
                        "quantity": qty
                    })
                except (ValueError, IndexError):
                    continue

        if not sales_data:
            print("[-] No valid product items found. Please check the exclusion list.")
            return

        # Sort by revenue descending
        top_performers = sorted(sales_data, key=lambda x: x['revenue'], reverse=True)

        print("\n" + "="*50)
        print("   Kiez Kaffee Kraft - Final Product Report")
        print("="*50)
        print(f"[*] Total Quantity Sold    : {total_quantity:,} units")
        print(f"[*] Total Gross Revenue    : €{total_revenue:,.2f}")
        print("-" * 50)
        print("TOP 5 Best Sellers (Actual Menu Items):")
        
        for item in top_performers[:5]:
            share = (item['revenue'] / total_revenue) * 100
            print(f"- {item['item_name']:<25}: €{item['revenue']:>10.2f} ({share:>5.1f}%)")
        print("="*50 + "\n")

    except Exception as e:
        print(f"[-] A critical error occurred: {e}")

if __name__ == "__main__":
    run_analysis()
