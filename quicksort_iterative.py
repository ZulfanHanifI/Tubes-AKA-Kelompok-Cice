"""
Quick Sort Iteratif
Implementasi algoritma Quick Sort dengan pendekatan iteratif menggunakan stack eksplisit.
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


def quick_sort_iterative(arr, key=None, reverse=False):
    """
    Implementasi Quick Sort Iteratif menggunakan stack eksplisit.
    
    Kompleksitas Waktu:
    - Best Case: O(n log n)
    - Average Case: O(n log n)
    - Worst Case: O(n²)
    
    Kompleksitas Ruang: O(log n) untuk stack eksplisit
    
    Keunggulan dibanding rekursif:
    - Tidak terbatas oleh recursion depth limit Python
    - Lebih aman untuk data berukuran sangat besar
    
    Args:
        arr: List data yang akan diurutkan
        key: Fungsi untuk mengambil nilai kunci dari elemen
        reverse: True untuk urutan descending
    
    Returns:
        List yang sudah diurutkan (in-place)
    """
    if len(arr) <= 1:
        return arr
    
    # Inisialisasi stack dengan range awal
    stack = []
    low = 0
    high = len(arr) - 1
    
    # Push range awal ke stack
    stack.append((low, high))
    
    # Proses selama stack tidak kosong
    while stack:
        # Pop dari stack
        low, high = stack.pop()
        
        if low < high:
            # Partisi dan dapatkan posisi pivot
            pivot_index = partition(arr, low, high, key, reverse)
            
            # Push sub-array kiri ke stack (jika ada elemen)
            if pivot_index - 1 > low:
                stack.append((low, pivot_index - 1))
            
            # Push sub-array kanan ke stack (jika ada elemen)
            if pivot_index + 1 < high:
                stack.append((pivot_index + 1, high))
    
    return arr


def sort_products_iterative(products, sort_by='price', reverse=False):
    """
    Mengurutkan list produk menggunakan Quick Sort Iteratif.
    
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
    
    return quick_sort_iterative(products_copy, key=key_func, reverse=reverse)


if __name__ == "__main__":
    # Contoh penggunaan
    sample_products = [
        {"id": 1, "name": "Laptop", "price": 15000000, "stock": 10},
        {"id": 2, "name": "Mouse", "price": 250000, "stock": 50},
        {"id": 3, "name": "Keyboard", "price": 500000, "stock": 30},
        {"id": 4, "name": "Monitor", "price": 3500000, "stock": 15},
        {"id": 5, "name": "Headset", "price": 750000, "stock": 25},
    ]
    
    print("=== Quick Sort Iteratif Demo ===\n")
    
    print("Data Asli:")
    for p in sample_products:
        print(f"  {p['name']}: Rp {p['price']:,} (Stok: {p['stock']})")
    
    print("\n--- Urut berdasarkan Harga (Ascending) ---")
    sorted_by_price = sort_products_iterative(sample_products, sort_by='price')
    for p in sorted_by_price:
        print(f"  {p['name']}: Rp {p['price']:,}")
    
    print("\n--- Urut berdasarkan Nama (A-Z) ---")
    sorted_by_name = sort_products_iterative(sample_products, sort_by='name')
    for p in sorted_by_name:
        print(f"  {p['name']}")
    
    print("\n--- Urut berdasarkan Stok (Descending) ---")
    sorted_by_stock = sort_products_iterative(sample_products, sort_by='stock', reverse=True)
    for p in sorted_by_stock:
        print(f"  {p['name']}: Stok {p['stock']}")
