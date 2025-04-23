
import time
import tracemalloc
import random
import matplotlib.pyplot as plt
from bplustree import BPlusTree
from bruteforce import BruteForceDB

class PerformanceAnalyzer:
    def __init__(self, n=1000, order=4):
        self.n = n
        self.order = order

    def _benchmark(self, func, *args):
        tracemalloc.start()
        start_time = time.time()
        func(*args)
        elapsed_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return elapsed_time, peak / 1024  # in KB

    def run_tests(self, sizes):
        bpt_insert_times = []
        bf_insert_times = []

        bpt_search_times = []
        bf_search_times = []

        bpt_memory = []
        bf_memory = []

        for size in sizes:
            bptree = BPlusTree(self.order)
            bfdb = BruteForceDB()
            keys = random.sample(range(size * 10), size)

            # Insert
            bpt_time, bpt_mem = self._benchmark(self._insert_bptree, bptree, keys)
            bf_time, bf_mem = self._benchmark(self._insert_bfdb, bfdb, keys)
            bpt_insert_times.append(bpt_time)
            bf_insert_times.append(bf_time)
            bpt_memory.append(bpt_mem)
            bf_memory.append(bf_mem)

            # Search (random subset)
            search_keys = random.sample(keys, min(100, len(keys)))
            bpt_time, _ = self._benchmark(self._search_bptree, bptree, search_keys)
            bf_time, _ = self._benchmark(self._search_bfdb, bfdb, search_keys)
            bpt_search_times.append(bpt_time)
            bf_search_times.append(bf_time)

        return {
            "sizes": sizes,
            "bpt_insert": bpt_insert_times,
            "bf_insert": bf_insert_times,
            "bpt_search": bpt_search_times,
            "bf_search": bf_search_times,
            "bpt_memory": bpt_memory,
            "bf_memory": bf_memory,
        }

    def _insert_bptree(self, bptree, keys):
        for key in keys:
            bptree.insert(key, f"Value {key}")

    def _insert_bfdb(self, bfdb, keys):
        for key in keys:
            bfdb.insert(key, f"Value {key}")

    def _search_bptree(self, bptree, keys):
        for key in keys:
            bptree.search(key)

    def _search_bfdb(self, bfdb, keys):
        for key in keys:
            bfdb.search(key)

    def run_and_plot(self):
        sizes = [int(self.n * scale) for scale in [0.1, 0.2, 0.5, 1]]
        results = self.run_tests(sizes)
        self.plot_results(results)

    def plot_results(self, results):
        sizes = results["sizes"]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(sizes, results["bpt_insert"], label="B+ Tree Insert")
        plt.plot(sizes, results["bf_insert"], label="Brute Force Insert")
        plt.xlabel("Data Size")
        plt.ylabel("Insert Time (s)")
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(sizes, results["bpt_search"], label="B+ Tree Search")
        plt.plot(sizes, results["bf_search"], label="Brute Force Search")
        plt.xlabel("Data Size")
        plt.ylabel("Search Time (s)")
        plt.legend()

        plt.tight_layout()
        plt.show()
