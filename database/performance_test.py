import matplotlib.pyplot as plt
import time
import random
import tracemalloc
from database.bplustree import BPlusTree
from database.bruteforce import BruteForceDB

dataset_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]

insert_times_btree = []
insert_times_brute = []

search_times_btree = []
search_times_brute = []

delete_times_btree = []
delete_times_brute = []

range_times_btree = []
range_times_brute = []

btree_mem_usage = []
brute_mem_usage = []

# Performance + memory measurement function
def measure_time_operations(dataset_size):
    keys = random.sample(range(1, dataset_size * 10), dataset_size)

    # --- B+ Tree ---
    bptree = BPlusTree(order=5)

    tracemalloc.start()
    # Insert
    start = time.time()
    for key in keys:
        bptree.insert(key, f"value_{key}")
    insert_time_btree = time.time() - start
    current_bptree_mem, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Search
    start = time.time()
    for key in keys:
        bptree.search(key)
    search_time_btree = time.time() - start

    # Delete
    start = time.time()
    for key in keys:
        bptree.delete(key)
    delete_time_btree = time.time() - start

    # Range
    start = time.time()
    _ = len(bptree.range_query(min(keys), max(keys)))
    range_time_btree = time.time() - start

    # --- Brute Force ---
    brute = BruteForceDB()

    tracemalloc.start()
    # Insert
    start = time.time()
    for key in keys:
        brute.insert(key, f"value_{key}")
    insert_time_brute = time.time() - start
    current_brute_mem, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Search
    start = time.time()
    for key in keys:
        brute.search(key)
    search_time_brute = time.time() - start

    # Delete
    start = time.time()
    for key in keys:
        brute.delete(key)
    delete_time_brute = time.time() - start

    # Range
    start = time.time()
    _ = len(brute.range_query(min(keys), max(keys)))
    range_time_brute = time.time() - start

    # Print summary
    print(f"Dataset Size: {dataset_size}")
    print(f"Memory Used - B+ Tree: {current_bptree_mem / 1024:.2f} KB")
    print(f"Memory Used - Brute Force: {current_brute_mem / 1024:.2f} KB")
    print("-" * 50)

    # Append results
    insert_times_btree.append(insert_time_btree)
    insert_times_brute.append(insert_time_brute)

    search_times_btree.append(search_time_btree)
    search_times_brute.append(search_time_brute)

    delete_times_btree.append(delete_time_btree)
    delete_times_brute.append(delete_time_brute)

    range_times_btree.append(range_time_btree)
    range_times_brute.append(range_time_brute)

    btree_mem_usage.append(current_bptree_mem / 1024)
    brute_mem_usage.append(current_brute_mem / 1024)

# Run the benchmarks
print("\n📊 Running Dynamic Performance Tests...\n")
for size in dataset_sizes:
    measure_time_operations(size)

# Plotting Function
def plot_results(dataset_sizes, insert_btree, insert_brute,
                 search_btree, search_brute,
                 delete_btree, delete_brute,
                 range_btree, range_brute):
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Insert Time
    axs[0, 0].plot(dataset_sizes, insert_btree, label="B+ Tree", color='royalblue', linewidth=2)
    axs[0, 0].plot(dataset_sizes, insert_brute, label="Brute Force", color='darkorange', linewidth=2)
    axs[0, 0].set_title("Insert Time Comparison", fontsize=12)
    axs[0, 0].set_xlabel("Dataset Size")
    axs[0, 0].set_ylabel("Time (s)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Search Time
    axs[0, 1].plot(dataset_sizes, search_btree, label="B+ Tree", color='royalblue', linewidth=2)
    axs[0, 1].plot(dataset_sizes, search_brute, label="Brute Force", color='darkorange', linewidth=2)
    axs[0, 1].set_title("Search Time Comparison", fontsize=12)
    axs[0, 1].set_xlabel("Dataset Size")
    axs[0, 1].set_ylabel("Time (s)")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Delete Time
    axs[1, 0].plot(dataset_sizes, delete_btree, label="B+ Tree", color='royalblue', linewidth=2)
    axs[1, 0].plot(dataset_sizes, delete_brute, label="Brute Force", color='darkorange', linewidth=2)
    axs[1, 0].set_title("Delete Time Comparison", fontsize=12)
    axs[1, 0].set_xlabel("Dataset Size")
    axs[1, 0].set_ylabel("Time (s)")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Range Time
    axs[1, 1].plot(dataset_sizes, range_btree, label="B+ Tree", color='royalblue', linewidth=2)
    axs[1, 1].plot(dataset_sizes, range_brute, label="Brute Force", color='darkorange', linewidth=2)
    axs[1, 1].set_title("Range Time Comparison", fontsize=12)
    axs[1, 1].set_xlabel("Dataset Size")
    axs[1, 1].set_ylabel("Time (s)")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.suptitle("Performance Comparison: B+ Tree vs Brute Force", fontsize=15, fontweight='bold')
    plt.show()

# Memory Usage Plot
def plot_memory_usage(dataset_sizes, btree_memory, brute_memory):
    plt.figure(figsize=(8, 5))
    plt.plot(dataset_sizes, btree_memory, label="B+ Tree", color="royalblue", linewidth=2)
    plt.plot(dataset_sizes, brute_memory, label="Brute Force", color="darkorange", linewidth=2)
    plt.xlabel("Dataset Size")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Memory Usage Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Call plotting functions
plot_results(dataset_sizes,
             insert_times_btree, insert_times_brute,
             search_times_btree, search_times_brute,
             delete_times_btree, delete_times_brute,
             range_times_btree, range_times_brute)

plot_memory_usage(dataset_sizes, btree_mem_usage, brute_mem_usage)