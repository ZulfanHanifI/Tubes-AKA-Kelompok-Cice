"""
Benchmark Module
Modul untuk mengukur dan membandingkan performa Quick Sort Rekursif vs Iteratif.
"""

import time
import copy
from product_data import generate_random_products, load_products_from_csv
from quicksort_recursive import quick_sort_recursive, sort_products_recursive
from quicksort_iterative import quick_sort_iterative, sort_products_iterative


def measure_time(func, *args, **kwargs):
    """
    Mengukur waktu eksekusi sebuah fungsi.
    
    Args:
        func: Fungsi yang akan diukur
        *args, **kwargs: Argumen untuk fungsi
    
    Returns:
        Tuple (hasil, waktu_eksekusi_ms)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    
    execution_time_ms = (end_time - start_time) * 1000
    return result, execution_time_ms


def run_single_comparison(products, sort_by='price', reverse=False):
    """
    Menjalankan perbandingan tunggal antara Quick Sort Rekursif dan Iteratif.
    
    Args:
        products: List dictionary produk
        sort_by: Atribut untuk pengurutan
        reverse: True untuk urutan descending
    
    Returns:
        Dictionary dengan hasil perbandingan
    """
    # Buat salinan untuk masing-masing algoritma
    products_recursive = copy.deepcopy(products)
    products_iterative = copy.deepcopy(products)
    
    # Ukur waktu Quick Sort Rekursif
    _, time_recursive = measure_time(
        sort_products_recursive, 
        products_recursive, 
        sort_by=sort_by, 
        reverse=reverse
    )
    
    # Ukur waktu Quick Sort Iteratif
    _, time_iterative = measure_time(
        sort_products_iterative, 
        products_iterative, 
        sort_by=sort_by, 
        reverse=reverse
    )
    
    return {
        'data_size': len(products),
        'sort_by': sort_by,
        'time_recursive_ms': time_recursive,
        'time_iterative_ms': time_iterative,
        'difference_ms': time_recursive - time_iterative,
        'faster': 'Iteratif' if time_iterative < time_recursive else 'Rekursif'
    }


def run_benchmark(data_sizes=None, sort_by='price', iterations=3):
    """
    Menjalankan benchmark lengkap untuk berbagai ukuran data.
    
    Args:
        data_sizes: List ukuran data untuk diuji
        sort_by: Atribut untuk pengurutan
        iterations: Jumlah iterasi untuk rata-rata
    
    Returns:
        List hasil benchmark
    """
    if data_sizes is None:
        data_sizes = [100, 500, 1000, 2500, 5000, 7500, 10000]
    
    results = []
    
    print("\n" + "=" * 70)
    print("BENCHMARK QUICK SORT: REKURSIF vs ITERATIF")
    print("=" * 70)
    print(f"Atribut pengurutan: {sort_by}")
    print(f"Jumlah iterasi per ukuran data: {iterations}")
    print("=" * 70 + "\n")
    
    for size in data_sizes:
        print(f"Testing dengan {size:,} data...", end=" ", flush=True)
        
        recursive_times = []
        iterative_times = []
        
        for i in range(iterations):
            # Generate data baru setiap iterasi
            products = generate_random_products(size)
            
            # Buat salinan untuk masing-masing algoritma
            products_recursive = copy.deepcopy(products)
            products_iterative = copy.deepcopy(products)
            
            # Key function
            if sort_by == 'name':
                key_func = lambda x: x.get(sort_by, '').lower()
            else:
                key_func = lambda x: x.get(sort_by, 0)
            
            # Ukur waktu rekursif
            _, time_rec = measure_time(
                quick_sort_recursive, 
                products_recursive,
                key=key_func
            )
            recursive_times.append(time_rec)
            
            # Ukur waktu iteratif
            _, time_iter = measure_time(
                quick_sort_iterative, 
                products_iterative,
                key=key_func
            )
            iterative_times.append(time_iter)
        
        # Hitung rata-rata
        avg_recursive = sum(recursive_times) / len(recursive_times)
        avg_iterative = sum(iterative_times) / len(iterative_times)
        
        result = {
            'data_size': size,
            'avg_recursive_ms': avg_recursive,
            'avg_iterative_ms': avg_iterative,
            'difference_ms': avg_recursive - avg_iterative,
            'faster': 'Iteratif' if avg_iterative < avg_recursive else 'Rekursif',
            'speedup': max(avg_recursive, avg_iterative) / max(min(avg_recursive, avg_iterative), 0.001)
        }
        results.append(result)
        
        print(f"Rekursif: {avg_recursive:.3f}ms | Iteratif: {avg_iterative:.3f}ms | Lebih cepat: {result['faster']}")
    
    return results


def print_benchmark_table(results):
    """
    Menampilkan hasil benchmark dalam format tabel.
    
    Args:
        results: List hasil benchmark
    """
    print("\n" + "=" * 85)
    print("TABEL HASIL BENCHMARK")
    print("=" * 85)
    print(f"{'Ukuran Data':>12} | {'Rekursif (ms)':>14} | {'Iteratif (ms)':>14} | {'Selisih (ms)':>13} | {'Lebih Cepat':<12}")
    print("-" * 85)
    
    for r in results:
        print(f"{r['data_size']:>12,} | {r['avg_recursive_ms']:>14.3f} | {r['avg_iterative_ms']:>14.3f} | {r['difference_ms']:>+13.3f} | {r['faster']:<12}")
    
    print("=" * 85)


def print_complexity_analysis():
    """
    Menampilkan analisis kompleksitas waktu.
    """
    print("\n" + "=" * 70)
    print("ANALISIS KOMPLEKSITAS WAKTU")
    print("=" * 70)
    
    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │                    QUICK SORT COMPLEXITY                        │
    ├─────────────────┬──────────────────────┬────────────────────────┤
    │     Kasus       │      Rekursif        │       Iteratif         │
    ├─────────────────┼──────────────────────┼────────────────────────┤
    │   Best Case     │     O(n log n)       │      O(n log n)        │
    │   Average Case  │     O(n log n)       │      O(n log n)        │
    │   Worst Case    │     O(n²)            │      O(n²)             │
    ├─────────────────┼──────────────────────┼────────────────────────┤
    │ Space Complexity│   O(log n) stack     │   O(log n) stack       │
    │                 │   (call stack)       │   (explicit stack)     │
    └─────────────────┴──────────────────────┴────────────────────────┘
    
    CATATAN:
    --------
    • Kedua implementasi memiliki kompleksitas waktu yang sama secara teoritis
    • Perbedaan waktu eksekusi disebabkan oleh:
      - Overhead pemanggilan fungsi rekursif
      - Manajemen stack eksplisit vs implicit call stack
      - Optimisasi interpreter Python
    
    • Worst case O(n²) terjadi ketika:
      - Array sudah terurut (ascending atau descending)
      - Semua elemen sama
      - Pivot selalu elemen terkecil/terbesar
    
    • Untuk menghindari worst case, dapat digunakan:
      - Random pivot selection
      - Median of three
      - Introsort (hybrid dengan Heapsort)
    """)
    print("=" * 70)


def analyze_growth_rate(results):
    """
    Menganalisis apakah pertumbuhan waktu sesuai dengan O(n log n).
    
    Args:
        results: List hasil benchmark
    """
    import math
    
    print("\n" + "=" * 70)
    print("ANALISIS PERTUMBUHAN WAKTU (Verifikasi O(n log n))")
    print("=" * 70)
    
    print(f"\n{'Ukuran (n)':>12} | {'n log n':>14} | {'Rasio Rekursif':>16} | {'Rasio Iteratif':>16}")
    print("-" * 70)
    
    base_n = results[0]['data_size']
    base_nlogn = base_n * math.log2(base_n)
    base_rec = results[0]['avg_recursive_ms']
    base_iter = results[0]['avg_iterative_ms']
    
    for r in results:
        n = r['data_size']
        nlogn = n * math.log2(n)
        
        expected_ratio = nlogn / base_nlogn
        actual_rec_ratio = r['avg_recursive_ms'] / base_rec if base_rec > 0 else 0
        actual_iter_ratio = r['avg_iterative_ms'] / base_iter if base_iter > 0 else 0
        
        print(f"{n:>12,} | {nlogn:>14,.0f} | {actual_rec_ratio:>16.2f}x | {actual_iter_ratio:>16.2f}x")
    
    print("-" * 70)
    print("Jika rasio mendekati pertumbuhan n log n, maka kompleksitas terbukti O(n log n)")
    print("=" * 70)


if __name__ == "__main__":
    # Jalankan benchmark
    print("\nMemulai benchmark Quick Sort...\n")
    
    # Benchmark dengan ukuran data berbeda
    results = run_benchmark(
        data_sizes=[100, 500, 1000, 2500, 5000, 7500, 10000],
        sort_by='price',
        iterations=3
    )
    
    # Tampilkan tabel hasil
    print_benchmark_table(results)
    
    # Analisis pertumbuhan
    analyze_growth_rate(results)
    
    # Tampilkan analisis kompleksitas
    print_complexity_analysis()
