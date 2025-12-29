"""
Product Data Handler
Modul untuk membaca dan mengelola data produk dari file CSV.
"""

import csv
import random
import string


def load_products_from_csv(filepath):
    """
    Membaca data produk dari file CSV.
    
    Args:
        filepath: Path ke file CSV
    
    Returns:
        List dictionary produk
    """
    products = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = {}
                for key, value in row.items():
                    # Clean key name
                    clean_key = key.strip().lower()
                    
                    # Coba konversi ke numerik jika memungkinkan
                    try:
                        if '.' in value:
                            product[clean_key] = float(value)
                        else:
                            product[clean_key] = int(value)
                    except (ValueError, TypeError):
                        product[clean_key] = value.strip() if value else ''
                
                products.append(product)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan.")
    except Exception as e:
        print(f"Error membaca file: {e}")
    
    return products


def save_products_to_csv(products, filepath):
    """
    Menyimpan data produk ke file CSV.
    
    Args:
        products: List dictionary produk
        filepath: Path ke file CSV
    """
    if not products:
        print("Tidak ada data untuk disimpan.")
        return
    
    try:
        fieldnames = products[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
        print(f"Data berhasil disimpan ke '{filepath}'")
    except Exception as e:
        print(f"Error menyimpan file: {e}")


def generate_random_products(n):
    """
    Menghasilkan n produk random untuk testing.
    
    Args:
        n: Jumlah produk yang akan dibuat
    
    Returns:
        List dictionary produk
    """
    product_names = [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Headset",
        "Speaker", "Webcam", "SSD", "RAM", "Processor",
        "Motherboard", "VGA Card", "Power Supply", "Casing", "Cooler",
        "Router", "Switch Hub", "UPS", "External HDD", "Flash Drive",
        "Printer", "Scanner", "Projector", "Tablet", "Smartphone"
    ]
    
    brands = ["Tech", "Pro", "Max", "Ultra", "Elite", "Premium", "Basic", "Advanced"]
    
    products = []
    for i in range(1, n + 1):
        name_base = random.choice(product_names)
        brand = random.choice(brands)
        
        product = {
            "id": i,
            "name": f"{name_base} {brand} {random.randint(1, 999)}",
            "price": random.randint(50000, 20000000),
            "stock": random.randint(0, 100)
        }
        products.append(product)
    
    return products


def display_products(products, limit=None):
    """
    Menampilkan daftar produk dalam format tabel.
    
    Args:
        products: List dictionary produk
        limit: Batasan jumlah produk yang ditampilkan
    """
    if not products:
        print("Tidak ada produk untuk ditampilkan.")
        return
    
    display_list = products[:limit] if limit else products
    
    # Dapatkan header dari keys
    headers = list(display_list[0].keys())
    
    # Hitung lebar kolom
    col_widths = {h: len(str(h)) for h in headers}
    for product in display_list:
        for key, value in product.items():
            col_widths[key] = max(col_widths.get(key, 0), len(str(value)))
    
    # Print header
    header_line = " | ".join(h.upper().ljust(col_widths[h]) for h in headers)
    separator = "-+-".join("-" * col_widths[h] for h in headers)
    
    print(header_line)
    print(separator)
    
    # Print data
    for product in display_list:
        row = " | ".join(str(product.get(h, '')).ljust(col_widths[h]) for h in headers)
        print(row)
    
    if limit and len(products) > limit:
        print(f"\n... dan {len(products) - limit} produk lainnya")


def get_column_names(products):
    """
    Mendapatkan nama kolom dari data produk.
    
    Args:
        products: List dictionary produk
    
    Returns:
        List nama kolom
    """
    if not products:
        return []
    return list(products[0].keys())


if __name__ == "__main__":
    # Demo
    print("=== Product Data Handler Demo ===\n")
    
    # Generate sampel data
    print("Generating 10 random products...")
    products = generate_random_products(10)
    display_products(products)
    
    # Coba baca dari file jika ada
    print("\n\nMembaca dari data.csv...")
    csv_products = load_products_from_csv('data.csv')
    if csv_products:
        print(f"Ditemukan {len(csv_products)} produk dari file CSV")
        display_products(csv_products, limit=5)
