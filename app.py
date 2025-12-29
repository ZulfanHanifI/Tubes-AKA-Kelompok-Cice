"""
Flask Web Application for Quick Sort Comparison
Aplikasi web sederhana untuk membandingkan Quick Sort Rekursif vs Iteratif
"""

from flask import Flask, render_template, request, jsonify
import time
import copy
import csv
import random
import sys

# Increase recursion limit for large datasets
sys.setrecursionlimit(50000)

app = Flask(__name__)

# ============ Quick Sort Implementations ============

def partition(arr, low, high, key=None, reverse=False):
    """Fungsi partisi untuk Quick Sort."""
    if key is None:
        key = lambda x: x
    
    pivot_raw = key(arr[high])
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
    """Quick Sort Rekursif"""
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_index = partition(arr, low, high, key, reverse)
        quick_sort_recursive(arr, low, pivot_index - 1, key, reverse)
        quick_sort_recursive(arr, pivot_index + 1, high, key, reverse)
    
    return arr


def quick_sort_iterative(arr, key=None, reverse=False):
    """Quick Sort Iteratif dengan stack eksplisit"""
    if len(arr) <= 1:
        return arr
    
    stack = []
    low = 0
    high = len(arr) - 1
    
    stack.append((low, high))
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            pivot_index = partition(arr, low, high, key, reverse)
            
            if pivot_index - 1 > low:
                stack.append((low, pivot_index - 1))
            
            if pivot_index + 1 < high:
                stack.append((pivot_index + 1, high))
    
    return arr


# ============ Data Functions ============

def load_products_from_csv(filepath):
    """Membaca data produk dari file CSV."""
    products = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = {}
                for key, value in row.items():
                    clean_key = key.strip().lower()
                    try:
                        if '.' in str(value):
                            product[clean_key] = float(value)
                        else:
                            product[clean_key] = int(value)
                    except (ValueError, TypeError):
                        product[clean_key] = value.strip() if value else ''
                products.append(product)
    except Exception as e:
        print(f"Error: {e}")
    return products


def generate_random_products(n):
    """Menghasilkan n produk random."""
    product_names = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset",
                     "Speaker", "Webcam", "SSD", "RAM", "Processor"]
    brands = ["Tech", "Pro", "Max", "Ultra", "Elite", "Premium"]
    
    products = []
    for i in range(1, n + 1):
        products.append({
            "id": i,
            "name": f"{random.choice(product_names)} {random.choice(brands)} {random.randint(1, 999)}",
            "price": random.randint(50000, 20000000),
            "stock": random.randint(0, 100)
        })
    return products


# ============ Global Data Storage ============
current_products = []


# ============ Routes ============

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/load-csv', methods=['POST'])
def load_csv():
    global current_products
    try:
        current_products = load_products_from_csv('data.csv')
        
        if current_products:
            columns = list(current_products[0].keys())
            return jsonify({
                'success': True,
                'count': len(current_products),
                'columns': columns,
                'sample': current_products[:10]
            })
        return jsonify({'success': False, 'message': 'Gagal memuat data atau file kosong'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/generate', methods=['POST'])
def generate():
    global current_products
    try:
        data = request.get_json() or {}
        count = int(data.get('count', 1000))
        
        current_products = generate_random_products(count)
        columns = list(current_products[0].keys())
        
        return jsonify({
            'success': True,
            'count': len(current_products),
            'columns': columns,
            'sample': current_products[:10]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/sort', methods=['POST'])
def sort_data():
    global current_products
    
    try:
        if not current_products:
            return jsonify({'success': False, 'message': 'Tidak ada data. Muat data terlebih dahulu.'})
        
        data = request.get_json() or {}
        algorithm = data.get('algorithm', 'recursive')
        sort_by = data.get('sort_by', 'price')
        reverse = data.get('reverse', False)
        
        # Prepare key function - always convert to string for safe comparison
        key_func = lambda x: str(x.get(sort_by, '')).lower()
        
        # Make a copy
        products_copy = copy.deepcopy(current_products)
        
        # Measure time
        start_time = time.perf_counter()
        
        if algorithm == 'recursive':
            sorted_products = quick_sort_recursive(products_copy, key=key_func, reverse=reverse)
        else:
            sorted_products = quick_sort_iterative(products_copy, key=key_func, reverse=reverse)
        
        end_time = time.perf_counter()
        exec_time_ms = (end_time - start_time) * 1000
        
        return jsonify({
            'success': True,
            'algorithm': 'Rekursif' if algorithm == 'recursive' else 'Iteratif',
            'sort_by': sort_by,
            'order': 'Descending' if reverse else 'Ascending',
            'time_ms': round(exec_time_ms, 3),
            'count': len(sorted_products),
            'sample': sorted_products[:50]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/benchmark', methods=['POST'])
def benchmark():
    try:
        data = request.get_json() or {}
        sizes = data.get('sizes', [100, 500, 1000, 2500, 5000])
        iterations = data.get('iterations', 3)
        
        results = []
        
        for size in sizes:
            rec_times = []
            iter_times = []
            
            for _ in range(iterations):
                products = generate_random_products(size)
                key_func = lambda x: str(x.get('price', 0))
                
                # Recursive
                products_rec = copy.deepcopy(products)
                start = time.perf_counter()
                quick_sort_recursive(products_rec, key=key_func)
                rec_times.append((time.perf_counter() - start) * 1000)
                
                # Iterative
                products_iter = copy.deepcopy(products)
                start = time.perf_counter()
                quick_sort_iterative(products_iter, key=key_func)
                iter_times.append((time.perf_counter() - start) * 1000)
            
            avg_rec = sum(rec_times) / len(rec_times)
            avg_iter = sum(iter_times) / len(iter_times)
            
            results.append({
                'size': size,
                'recursive_ms': round(avg_rec, 3),
                'iterative_ms': round(avg_iter, 3),
                'faster': 'Iteratif' if avg_iter < avg_rec else 'Rekursif'
            })
        
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Error handlers to always return JSON
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'message': 'Endpoint tidak ditemukan'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Quick Sort Comparison Web App...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
