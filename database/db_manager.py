import json
import os

class Database:
    def __init__(self):
        self.databases_dir = "data"
        os.makedirs(self.databases_dir, exist_ok=True)

    def list_databases(self):
        return [f.replace('.json', '') for f in os.listdir(self.databases_dir) if f.endswith('.json')]

    def create_database(self, name):
        db_path = os.path.join(self.databases_dir, f"{name}.json")
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                json.dump({}, f)
        else:
            raise Exception(f"Database '{name}' already exists.")

    def delete_database(self, name):
        db_path = os.path.join(self.databases_dir, f"{name}.json")
        if os.path.exists(db_path):
            os.remove(db_path)
        else:
            raise Exception(f"Database '{name}' does not exist.")

    def list_tables(self, db_name):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)
        return list(db.keys())

    def create_table(self, db_name, table_name, columns):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")
        
        # Ensure the databases directory exists
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        
        # Now it's safe to read
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if table already exists
        if table_name in db:
            raise Exception(f"Table '{table_name}' already exists in '{db_name}'.")

        # Add the new table
        db[table_name] = {"columns": columns, "records": []}

        # Write back to the file
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=4)

    def insert_into(self, db_name, table_name, record):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")

        # Load the database
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if the table exists
        if table_name not in db:
            raise Exception(f"Table '{table_name}' does not exist in database '{db_name}'.")

        # Get table schema and records
        table = db[table_name]
        expected_columns = table['columns']

        # Ensure record matches schema
        for column in expected_columns:
            if column not in record:
                raise Exception(f"Missing column '{column}' in the record.")
        
        # Optional: Check for extra columns in the record
        for column in record:
            if column not in expected_columns:
                raise Exception(f"Unexpected column '{column}' in the record.")

        # Append the record
        table['records'].append(record)

        # Write back the updated database
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=4)

    def delete_from(self, db_name, table_name, key_value):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")

        # Load the database
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if the table exists
        if table_name not in db:
            raise Exception(f"Table '{table_name}' does not exist in database '{db_name}'.")

        table = db[table_name]
        primary_key = 'id'  # Adjust this to your actual primary key if it's not 'id'

        # Find and remove the record
        table['records'] = [record for record in table['records'] if record.get(primary_key) != key_value]

        # Save the changes back to the file
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=4)

    def select_from(self, db_name, table_name, key_value):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")

        # Load the database
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if the table exists
        if table_name not in db:
            raise Exception(f"Table '{table_name}' does not exist in database '{db_name}'.")

        table = db[table_name]
        primary_key = 'id'  # Adjust this to your actual primary key if it's not 'id'

        for record in table['records']:
            if str(record.get(primary_key)) == str(key_value):
                return record

        return None  # If no matching record found
    
    def range_query(self, db_name, table_name, start_id, end_id):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")

        # Load the database
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if the table exists
        if table_name not in db:
            raise Exception(f"Table '{table_name}' does not exist in database '{db_name}'.")

        table = db[table_name]

        # Find and return records within the range
        result = [record for record in table['records'] if start_id <= record.get('id', 0) <= end_id]

        return result

    def drop_table(self, db_name, table_name):
        db_path = os.path.join(self.databases_dir, f"{db_name}.json")

        # Load the database
        if not os.path.exists(db_path):
            raise Exception(f"Database '{db_name}' does not exist.")
        with open(db_path, 'r') as f:
            db = json.load(f)

        # Check if the table exists
        if table_name not in db:
            raise Exception(f"Table '{table_name}' does not exist in database '{db_name}'.")

        # Remove the table
        del db[table_name]

        # Save the changes back to the file
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=4)

    def save_to_disk(self, filename="persistent_db.json"):
        # Save only BOOKS_DETAILS and SYS_LOGS from all databases
        to_save = {}
        for db_name, tables in self.databases.items():
            filtered_tables = {
                tbl_name: tbl_data
                for tbl_name, tbl_data in tables.items()
                if tbl_name in ["BOOKS_DETAILS", "SYS_LOGS"]
            }
            if filtered_tables:
                to_save[db_name] = filtered_tables

        with open(filename, "w") as f:
            json.dump(to_save, f, indent=4)
        print("Database saved to disk.")

    def load_from_disk(self, filename="persistent_db.json"):
        if not os.path.exists(filename):
            print("No persistent file found.")
            return

        with open(filename, "r") as f:
            self.databases = json.load(f)
        print("Database loaded from disk.")


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


import json
import os
from datetime import datetime

# class Database:
#     def __init__(self):
#         self.databases_dir = "data"
#         os.makedirs(self.databases_dir, exist_ok=True)

#     def _get_path(self, db_name):
#         return os.path.join(self.databases_dir, f"{db_name}.json")

#     def create_table(self, db_name, table_name, schema, primary_key='id'):
#         path = self._get_path(db_name)
#         db = {}
#         if os.path.exists(path):
#             with open(path, 'r') as f:
#                 db = json.load(f)
#         else:
#             self.save_to_disk(db_name, db)

#         if table_name in db:
#             raise Exception(f"Table '{table_name}' already exists.")
#         db[table_name] = {
#             "schema": schema,
#             "primary_key": primary_key,
#             "records": []
#         }
#         self.save_to_disk(db_name, db)

#     def insert_into(self, db_name, table_name, record):
#         db = self.load_from_disk(db_name)

#         if table_name not in db:
#             raise Exception(f"Table '{table_name}' doesn't exist.")

#         table = db[table_name]
#         primary_key = table["primary_key"]
#         if any(r[primary_key] == record[primary_key] for r in table["records"]):
#             print(f"Duplicate primary key '{record[primary_key]}' found. Skipping insert.")
#             return

#         table["records"].append(record)
#         self.save_to_disk(db_name, db)

#     def delete_from(self, db_name, table_name, key_value):
#         db = self.load_from_disk(db_name)
#         table = db[table_name]
#         pk = table["primary_key"]
#         table["records"] = [r for r in table["records"] if r[pk] != key_value]
#         self.save_to_disk(db_name, db)

#     def range_query(self, db_name, table_name, start, end):
#         db = self.load_from_disk(db_name)
#         table = db[table_name]
#         pk = table["primary_key"]
#         return [r for r in table["records"] if start <= r[pk] <= end]

#     def drop_table(self, db_name, table_name):
#         db = self.load_from_disk(db_name)
#         del db[table_name]
#         self.save_to_disk(db_name, db)

#     def save_to_disk(self, db_name=None, db=None):
#         if db_name and db is not None:
#             with open(self._get_path(db_name), 'w') as f:
#                 json.dump(db, f, indent=4)

#     def load_from_disk(self, db_name):
#         path = self._get_path(db_name)
#         if not os.path.exists(path):
#             raise Exception(f"Database '{db_name}' does not exist.")
#         with open(path, 'r') as f:
#             return json.load(f)