from database.table import Table
import pickle
import os

# database/db_manager.py

import os
import json

class Database:
    def __init__(self):
        self.databases_dir = "data"
        os.makedirs(self.databases_dir, exist_ok=True)

    def list_databases(self):
        return [f.replace('.json', '') for f in os.listdir(self.databases_dir) if f.endswith('.json')]

    def create_database(self, name):
        db_path = os.path.join(self.databases_dir, f"{name}.json")
        with open(db_path, 'w') as f:
            json.dump({}, f)

    def delete_database(self, name):
        os.remove(os.path.join(self.databases_dir, f"{name}.json"))

    def list_tables(self, db_name):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")
        with open(db_path, 'r') as f:
            db = json.load(f)
        return list(db.keys())

    def create_table(self, db_name, table_name, columns):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")
        with open(db_path, 'r') as f:
            db = json.load(f)
        db[table_name] = {"columns": columns, "records": []}
        with open(db_path, 'w') as f:
            json.dump(db, f)

    def delete_table(self, db_name, table_name):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")
        with open(db_path, 'r') as f:
            db = json.load(f)
        db.pop(table_name, None)
        with open(db_path, 'w') as f:
            json.dump(db, f)

    def get_table(self, db_name, table_name):
        return TableHandler(db_name, table_name, self.databases_dir)


class TableHandler:
    def __init__(self, db_name, table_name, dir_path):
        self.db_path = os.path.join(dir_path, f"{db_name}.json")
        self.table_name = table_name

    def all_records(self):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        return db[self.table_name]["records"]

    def insert(self, record):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        db[self.table_name]["records"].append(record)
        with open(self.db_path, 'w') as f:
            json.dump(db, f)

    def delete(self, record_id):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        db[self.table_name]["records"].pop(int(record_id))
        with open(self.db_path, 'w') as f:
            json.dump(db, f)

    def update(self, record_id, new_data):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        db[self.table_name]["records"][int(record_id)] = new_data
        with open(self.db_path, 'w') as f:
            json.dump(db, f)

    def search(self, query):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        return [r for r in db[self.table_name]["records"] if all(r.get(k) == v for k, v in query.items())]

    def range_query(self, field, min_val, max_val):
        with open(self.db_path, 'r') as f:
            db = json.load(f)
        return [r for r in db[self.table_name]["records"] if min_val <= r.get(field, 0) <= max_val]