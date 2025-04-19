# test.py

from database.bplustree import BPlusTree


def print_all(tree, title="All key-value pairs"):
    print(f"\n📄 {title}:")
    for k, v in tree.get_all():
        print(f"{k}: {v}")


def main():
    # Create B+ Tree with order 4
    tree = BPlusTree(order=4)

    # Insert entries
    print("🟢 Inserting values...")
    data = [
        (10, "Alice"),
        (20, "Bob"),
        (15, "Charlie"),
        (5, "David"),
        (25, "Eve"),
        (30, "Frank"),
        (12, "Grace"),
        (18, "Hannah")
    ]

    for k, v in data:
        tree.insert(k, v)

    print_all(tree, "After Insertions")

    # Search
    print("\n🔍 Searching:")
    print("Search 15 ➝", tree.search(15))  # Should be Charlie
    print("Search 100 ➝", tree.search(100))  # Should be None

    # Range Query
    print("\n📊 Range Query 10 to 25:")
    for k, v in tree.range_query(10, 25):
        print(f"{k}: {v}")

    # Delete some keys
    print("\n🗑️ Deleting keys 15, 10, 5...")
    tree.delete(15)
    tree.delete(10)
    tree.delete(5)

    print_all(tree, "After Deletions")

    # Visualize tree (Task 3)
    print("\n🌳 Generating B+ Tree Visualization...")
    dot = tree.visualize_tree()
    dot.render("bptree_visual", format="png", cleanup=True)
    print("✅ Tree visual saved as bptree_visual.png")


if __name__ == "__main__":
    main()
