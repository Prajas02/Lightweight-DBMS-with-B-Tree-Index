from bplustree import BPlusTree

class Table:
    
    def __init__(self, name, schema, primary_key, tree_order=3):
        self.name = name
        self.schema = schema
        self.primary_key = primary_key
        self.tree = BPlusTree(order=tree_order)  


    def insert(self, record):
        key = record[self.primary_key]
        self.tree.insert(key, record)

    def delete(self, key):
        self.tree.delete(key)

    def search(self, key):
        return self.tree.search(key)

    def range_query(self, start_key, end_key):
        return self.tree.range_query(start_key, end_key)

    def all_records(self):
        return list(self.tree.get_all())