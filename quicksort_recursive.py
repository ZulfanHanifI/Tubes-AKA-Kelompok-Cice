"""
Quick Sort Rekursif
Implementasi algoritma Quick Sort dengan pendekatan rekursif untuk pengurutan data produk.
"""

def partition(arr, low, high, key=None, reverse=False):
    """
    Fungsi partisi untuk Quick Sort.
    Memilih pivot (elemen terakhir) dan mempartisi array.
    
    Args:
        arr: List data yang akan dipartisi
        low: Indeks awal
        high: Indeks akhir
        key: Fungsi untuk mengambil nilai kunci dari elemen (opsional)
        reverse: True untuk urutan descending
    
    Returns:
        Indeks posisi pivot setelah partisi
    """
    if key is None:
        key = lambda x: x
    
    pivot_raw = key(arr[high])
    # Convert to string for consistent comparison when types are mixed
    pivot = str(pivot_raw) if pivot_raw is not None else ''
    i = low - 1
    
    for j in range(low, high):
        current_raw = key(arr[j])
        current_val = str(current_raw) if current_raw is not None else ''
        
        if reverse:
            condition = current_val >= pivot
        else:
            condition = current_val <= pivot
            
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_recursive(arr, low=None, high=None, key=None, reverse=False):
    """
    Implementasi Quick Sort Rekursif.
    
    Kompleksitas Waktu:
    - Best Case: O(n log n)
    - Average Case: O(n log n)
    - Worst Case: O(n²)
    
    Kompleksitas Ruang: O(log n) untuk call stack
    
    Args:
        arr: List data yang akan diurutkan
        low: Indeks awal (default: 0)
        high: Indeks akhir (default: len(arr) - 1)
        key: Fungsi untuk mengambil nilai kunci dari elemen
        reverse: True untuk urutan descending
    
    Returns:
        List yang sudah diurutkan (in-place)
    """
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partisi array dan dapatkan posisi pivot
        pivot_index = partition(arr, low, high, key, reverse)
        
        # Rekursif untuk sub-array kiri dan kanan
        quick_sort_recursive(arr, low, pivot_index - 1, key, reverse)
        quick_sort_recursive(arr, pivot_index + 1, high, key, reverse)
    
    return arr


def sort_products_recursive(products, sort_by='price', reverse=False):
    """
    Mengurutkan list produk menggunakan Quick Sort Rekursif.
    
    Args:
        products: List dictionary produk
        sort_by: Atribut untuk pengurutan ('price', 'name', 'stock', dll)
        reverse: True untuk urutan descending
    
    Returns:
        List produk yang sudah diurutkan
    """
    if not products:
        return products
    
    # Buat salinan agar tidak mengubah data asli
    products_copy = products.copy()
    
    # Tentukan key function berdasarkan atribut
    if sort_by == 'name':
        key_func = lambda x: x.get(sort_by, '').lower()
    else:
        key_func = lambda x: x.get(sort_by, 0)
    
    return quick_sort_recursive(products_copy, key=key_func, reverse=reverse)


if __name__ == "__main__":
    # Contoh penggunaan
    sample_products = [
        {"id": 1, "name": "Laptop", "price": 15000000, "stock": 10},
        {"id": 2, "name": "Mouse", "price": 250000, "stock": 50},
        {"id": 3, "name": "Keyboard", "price": 500000, "stock": 30},
        {"id": 4, "name": "Monitor", "price": 3500000, "stock": 15},
        {"id": 5, "name": "Headset", "price": 750000, "stock": 25},
    ]
    
    print("=== Quick Sort Rekursif Demo ===\n")
    
    print("Data Asli:")
    for p in sample_products:
        print(f"  {p['name']}: Rp {p['price']:,} (Stok: {p['stock']})")
    
    print("\n--- Urut berdasarkan Harga (Ascending) ---")
    sorted_by_price = sort_products_recursive(sample_products, sort_by='price')
    for p in sorted_by_price:
        print(f"  {p['name']}: Rp {p['price']:,}")
    
    print("\n--- Urut berdasarkan Nama (A-Z) ---")
    sorted_by_name = sort_products_recursive(sample_products, sort_by='name')
    for p in sorted_by_name:
        print(f"  {p['name']}")
    
    print("\n--- Urut berdasarkan Stok (Descending) ---")
    sorted_by_stock = sort_products_recursive(sample_products, sort_by='stock', reverse=True)
    for p in sorted_by_stock:
        print(f"  {p['name']}: Stok {p['stock']}")
