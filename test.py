# # test.py

# from database.performance_test import PerformanceAnalyzer
# import matplotlib.pyplot as plt

# # Define the dataset sizes to test with
# dataset_sizes = [1000, 2000, 3000, 4000, 5000, 6000]

# # Create analyzer instance
# analyzer = PerformanceAnalyzer(order=5)

# # Run tests and collect results
# print("\n🚀 Running Performance Tests...\n")
# results = analyzer.run_tests(dataset_sizes)

# # Plot time comparison (insert, search)
# analyzer.plot_results(results)

# # Plot memory usage
# def plot_memory_usage(dataset_sizes, btree_memory, brute_memory):
#     plt.figure(figsize=(8, 5))
#     plt.plot(dataset_sizes, btree_memory, label="B+ Tree", color="royalblue", linewidth=2)
#     plt.plot(dataset_sizes, brute_memory, label="Brute Force", color="darkorange", linewidth=2)
#     plt.xlabel("Dataset Size")
#     plt.ylabel("Memory Usage (KB)")
#     plt.title("Memory Usage Comparison")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

# # Call memory plot with extracted values
# plot_memory_usage(
#     results["sizes"],
#     results["bpt_memory"],
#     results["bf_memory"]
# )

# testing of visualisation

# Import the BPlusTree class from the bplustree.py file
from database.bplustree import BPlusTree, BPlusTreeNode

# Create a sample B+ Tree for testing
def create_sample_bplus_tree():
    # Create leaf nodes
    leaf1 = BPlusTreeNode(is_leaf=True)
    leaf1.keys = [1, 2, 3]
    leaf2 = BPlusTreeNode(is_leaf=True)
    leaf2.keys = [4, 5, 6]
    leaf3 = BPlusTreeNode(is_leaf=True)
    leaf3.keys = [7, 8, 9]

    # Link leaf nodes in a linked list style
    leaf1.next = leaf2
    leaf2.next = leaf3

    # Create internal nodes
    internal1 = BPlusTreeNode(is_leaf=False)
    internal1.keys = [3, 6]
    internal1.children = [leaf1, leaf2]
    internal2 = BPlusTreeNode(is_leaf=False)
    internal2.keys = [9]
    internal2.children = [leaf3]

    # Root node
    root = BPlusTreeNode(is_leaf=False)
    root.keys = [6]
    root.children = [internal1, internal2]

    return root

# Test the visualization function
def test_visualization():
    # Create a sample B+ Tree
    root = create_sample_bplus_tree()
    
    # Initialize BPlusTree with the root node
    bptree = BPlusTree(order=4)  # Assuming the default order of 4
    bptree.root = root  # Assign the created root to the tree
    
    # Generate the tree visualization
    tree_visual = bptree.visualize_tree()

    # Render the tree as a PNG image
    tree_visual.render('tree_visualization', format='png')
    print("Tree visualization saved as 'tree_visualization.png'")

# Run the test
if __name__ == '__main__':
    test_visualization()