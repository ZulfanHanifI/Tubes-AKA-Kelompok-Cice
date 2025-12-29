"""
Quick Sort Comparison Application
Aplikasi utama untuk membandingkan Quick Sort Rekursif vs Iteratif pada data produk.
"""

import sys
import copy
from product_data import (
    load_products_from_csv, 
    generate_random_products, 
    display_products,
    get_column_names,
    save_products_to_csv
)
from quicksort_recursive import sort_products_recursive
from quicksort_iterative import sort_products_iterative
from benchmark import (
    run_benchmark, 
    print_benchmark_table, 
    print_complexity_analysis,
    analyze_growth_rate,
    run_single_comparison, 
    measure_time
)


def clear_screen():
    """Membersihkan layar terminal."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Menampilkan header aplikasi."""
    print("\n" + "=" * 60)
    print("   APLIKASI PERBANDINGAN QUICK SORT")
    print("   Rekursif vs Iteratif - Data Produk")
    print("=" * 60)


def print_menu():
    """Menampilkan menu utama."""
    print("\n[MENU UTAMA]")
    print("-" * 40)
    print("1. Muat data dari file CSV")
    print("2. Generate data produk random")
    print("3. Lihat data produk")
    print("4. Sorting dengan Quick Sort Rekursif")
    print("5. Sorting dengan Quick Sort Iteratif")
    print("6. Bandingkan kedua algoritma (data saat ini)")
    print("7. Jalankan Benchmark Lengkap")
    print("8. Tampilkan Analisis Kompleksitas")
    print("9. Simpan data hasil sorting ke CSV")
    print("0. Keluar")
    print("-" * 40)


def get_sort_options(products):
    """
    Meminta user memilih atribut sorting.
    
    Returns:
        Tuple (sort_by, reverse)
    """
    columns = get_column_names(products)
    
    print("\nPilih atribut untuk pengurutan:")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")
    
    while True:
        try:
            choice = int(input("Pilihan: "))
            if 1 <= choice <= len(columns):
                sort_by = columns[choice - 1]
                break
            print("Pilihan tidak valid!")
        except ValueError:
            print("Masukkan angka yang valid!")
    
    order = input("Urutan (A)scending / (D)escending [A]: ").strip().upper()
    reverse = order == 'D'
    
    return sort_by, reverse


def run_sorting(products, algorithm='recursive'):
    """
    Menjalankan sorting dan menampilkan hasil.
    
    Args:
        products: List produk
        algorithm: 'recursive' atau 'iterative'
    
    Returns:
        List produk yang sudah diurutkan
    """
    if not products:
        print("Tidak ada data produk. Muat data terlebih dahulu.")
        return products
    
    sort_by, reverse = get_sort_options(products)
    
    order_text = "Descending" if reverse else "Ascending"
    algo_name = "Rekursif" if algorithm == 'recursive' else "Iteratif"
    
    print(f"\nMenjalankan Quick Sort {algo_name}...")
    print(f"Sorting berdasarkan: {sort_by} ({order_text})")
    print(f"Jumlah data: {len(products):,}")
    
    # Pilih fungsi sorting
    if algorithm == 'recursive':
        sorted_products, exec_time = measure_time(
            sort_products_recursive, 
            products, 
            sort_by=sort_by, 
            reverse=reverse
        )
    else:
        sorted_products, exec_time = measure_time(
            sort_products_iterative, 
            products, 
            sort_by=sort_by, 
            reverse=reverse
        )
    
    print(f"\n✓ Sorting selesai dalam {exec_time:.3f} ms")
    
    print(f"\nHasil sorting (10 data pertama):")
    display_products(sorted_products, limit=50)
    
    return sorted_products


def compare_algorithms(products):
    """
    Membandingkan kedua algoritma dengan data saat ini.
    """
    if not products:
        print("Tidak ada data produk. Muat data terlebih dahulu.")
        return
    
    sort_by, reverse = get_sort_options(products)
    
    print(f"\nMembandingkan Quick Sort Rekursif vs Iteratif...")
    print(f"Jumlah data: {len(products):,}")
    print(f"Sorting berdasarkan: {sort_by}")
    
    result = run_single_comparison(products, sort_by=sort_by, reverse=reverse)
    
    print("\n" + "=" * 50)
    print("HASIL PERBANDINGAN")
    print("=" * 50)
    print(f"Ukuran data      : {result['data_size']:,}")
    print(f"Quick Sort Rekursif : {result['time_recursive_ms']:.3f} ms")
    print(f"Quick Sort Iteratif : {result['time_iterative_ms']:.3f} ms")
    print(f"Selisih           : {abs(result['difference_ms']):.3f} ms")
    print(f"Lebih cepat       : {result['faster']}")
    print("=" * 50)


def main():
    """Fungsi utama aplikasi."""
    products = []
    sorted_products = []
    
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Pilih menu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nTerima kasih telah menggunakan aplikasi ini!")
            sys.exit(0)
        
        if choice == '1':
            # Muat data dari CSV
            filepath = input("Masukkan path file CSV [data.csv]: ").strip()
            if not filepath:
                filepath = 'data.csv'
            products = load_products_from_csv(filepath)
            if products:
                print(f"\n✓ Berhasil memuat {len(products):,} produk dari '{filepath}'")
                display_products(products, limit=5)
            
        elif choice == '2':
            # Generate data random
            while True:
                try:
                    n = int(input("Jumlah data yang ingin di-generate: "))
                    if n > 0:
                        break
                    print("Masukkan angka positif!")
                except ValueError:
                    print("Masukkan angka yang valid!")
            
            products = generate_random_products(n)
            print(f"\n✓ Berhasil generate {n:,} produk random")
            display_products(products, limit=5)
            
        elif choice == '3':
            # Lihat data produk
            if not products:
                print("Tidak ada data. Muat data terlebih dahulu.")
            else:
                limit_input = input(f"Tampilkan berapa data? (max={len(products)}, Enter=semua): ").strip()
                limit = int(limit_input) if limit_input else None
                display_products(products, limit=limit)
            
        elif choice == '4':
            # Quick Sort Rekursif
            sorted_products = run_sorting(products, algorithm='recursive')
            
        elif choice == '5':
            # Quick Sort Iteratif
            sorted_products = run_sorting(products, algorithm='iterative')
            
        elif choice == '6':
            # Bandingkan kedua algoritma
            compare_algorithms(products)
            
        elif choice == '7':
            # Benchmark lengkap
            print("\n[BENCHMARK LENGKAP]")
            print("Ini akan menguji kedua algoritma dengan berbagai ukuran data.")
            
            # Pilih ukuran data
            print("\nPilih preset ukuran data:")
            print("1. Kecil (100, 500, 1000)")
            print("2. Sedang (100, 500, 1000, 2500, 5000)")
            print("3. Besar (100, 500, 1000, 2500, 5000, 7500, 10000)")
            print("4. Custom")
            
            preset = input("Pilihan [2]: ").strip() or '2'
            
            if preset == '1':
                data_sizes = [100, 500, 1000]
            elif preset == '2':
                data_sizes = [100, 500, 1000, 2500, 5000]
            elif preset == '3':
                data_sizes = [100, 500, 1000, 2500, 5000, 7500, 10000]
            else:
                sizes_input = input("Masukkan ukuran data (pisahkan dengan koma): ")
                data_sizes = [int(x.strip()) for x in sizes_input.split(',')]
            
            # Pilih jumlah iterasi
            iterations = input("Jumlah iterasi untuk rata-rata [3]: ").strip()
            iterations = int(iterations) if iterations else 3
            
            # Jalankan benchmark
            results = run_benchmark(data_sizes=data_sizes, iterations=iterations)
            print_benchmark_table(results)
            analyze_growth_rate(results)
            
        elif choice == '8':
            # Analisis kompleksitas
            print_complexity_analysis()
            
        elif choice == '9':
            # Simpan hasil sorting
            if not sorted_products:
                print("Belum ada data hasil sorting. Jalankan sorting terlebih dahulu.")
            else:
                filepath = input("Masukkan nama file output [sorted_data.csv]: ").strip()
                if not filepath:
                    filepath = 'sorted_data.csv'
                save_products_to_csv(sorted_products, filepath)
            
        elif choice == '0':
            print("\nTerima kasih telah menggunakan aplikasi ini!")
            print("Sampai jumpa!")
            break
            
        else:
            print("Pilihan tidak valid. Silakan pilih 0-9.")
        
        input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    main()
