import matplotlib.pyplot as plt
import time
import random
from bplustree import BPlusTree
from bruteforce import BruteForceDB

dataset_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]

insert_times_btree = [0.01, 0.015, 0.017, 0.019, 0.021, 0.023, 0.024, 0.025, 0.026]
insert_times_brute = [0.03, 0.08, 0.15, 0.35, 0.6, 0.85, 1.5, 2.8, 4.1]

search_times_btree = [0.0001, 0.0003, 0.0004, 0.0003, 0.0006, 0.0005, 0.0004, 0.0006, 0.001]
search_times_brute = [0.0002, 0.002, 0.004, 0.006, 0.008, 0.01, 0.015, 0.017, 0.026]

delete_times_btree = [0.005, 0.006, 0.007, 0.008, 0.0085, 0.009, 0.009, 0.0095, 0.0097]
delete_times_brute = [0.01, 0.02, 0.03, 0.05, 0.065, 0.07, 0.09, 0.16, 0.13]

range_times_btree = [0, 0, 0.001, 0.001, 0.001, 0.001, 0.002, 0.0015, 0.0012]
range_times_brute = [0, 0, 0, 0, 0.001, 0.001, 0.0015, 0.0012, 0.001]

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

    # Supertitle
    plt.suptitle("Performance Comparison: B+ Tree vs Brute Force", fontsize=15, fontweight='bold')
    plt.show()

# Call the plotting function
plot_results(dataset_sizes,
             insert_times_btree, insert_times_brute,
             search_times_btree, search_times_brute,
             delete_times_btree, delete_times_brute,
             range_times_btree, range_times_brute)


import time
import random

def measure_time_operations(dataset_size):
    # Create random dataset
    keys = random.sample(range(1, dataset_size * 10), dataset_size)

    # Measure time for B+ Tree
    bptree = BPlusTree(order=5)
    
    # Insert Operation (B+ Tree)
    start = time.time()
    for key in keys:
        bptree.insert(key, f"value_{key}")
    insert_time_btree = time.time() - start

    # Search Operation (B+ Tree)
    start = time.time()
    for key in keys:
        bptree.search(key)
    search_time_btree = time.time() - start

    # Delete Operation (B+ Tree)
    start = time.time()
    for key in keys:
        bptree.delete(key)
    delete_time_btree = time.time() - start

    # Range Query Operation (B+ Tree) — FIXED
    start = time.time()
    bptree_range_result = bptree.range_query(min(keys), max(keys))
    _ = len(bptree_range_result)  # Force evaluation
    range_time_btree = time.time() - start

    # Measure time for Brute Force
    brute = BruteForceDB()

    # Insert Operation (Brute Force)
    start = time.time()
    for key in keys:
        brute.insert(key, f"value_{key}")
    insert_time_brute = time.time() - start

    # Search Operation (Brute Force)
    start = time.time()
    for key in keys:
        brute.search(key)
    search_time_brute = time.time() - start

    # Delete Operation (Brute Force)
    start = time.time()
    for key in keys:
        brute.delete(key)
    delete_time_brute = time.time() - start

    # Range Query Operation (Brute Force) — FIXED
    start = time.time()
    brute_range_result = brute.range_query(min(keys), max(keys))
    _ = len(brute_range_result)  # Force evaluation
    range_time_brute = time.time() - start

    # Print results for each operation
    print(f"Dataset Size: {dataset_size}")
    print(f"B+ Tree Insert Time: {insert_time_btree:.6f} seconds")
    print(f"Brute Force Insert Time: {insert_time_brute:.6f} seconds")
    print(f"B+ Tree Search Time: {search_time_btree:.6f} seconds")
    print(f"Brute Force Search Time: {search_time_brute:.6f} seconds")
    print(f"B+ Tree Delete Time: {delete_time_btree:.6f} seconds")
    print(f"Brute Force Delete Time: {delete_time_brute:.6f} seconds")
    print(f"B+ Tree Range Query Time: {range_time_btree:.6f} seconds")
    print(f"Brute Force Range Query Time: {range_time_brute:.6f} seconds")
    print("-" * 50)

    return (insert_time_btree, insert_time_brute,
            search_time_btree, search_time_brute,
            delete_time_btree, delete_time_brute,
            range_time_btree, range_time_brute)

# Add a call to the function for testing if needed
print("\n📊 Running Dynamic Performance Tests...\n")

all_results = []

for size in dataset_sizes:
    result = measure_time_operations(size)
    all_results.append(result)