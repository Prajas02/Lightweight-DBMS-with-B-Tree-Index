from table import Table
import pickle
import os

class Database:
    def __init__(self):
        print("Initializing Database...")
        self.tables = {}


    def create_table(self, name, schema, primary_key):
        """
        Create a new table with a given schema and primary key.
        """
        if name in self.tables:
            raise Exception(f"Table '{name}' already exists.")
        self.tables[name] = Table(name, schema, primary_key)
        print(f"✅ Table '{name}' created successfully.")

    def drop_table(self, name):
        """
        Delete a table by name.
        """
        if name in self.tables:
            del self.tables[name]
            print(f"🗑 Table '{name}' deleted.")
        else:
            print(f"❌ Table '{name}' does not exist.")

    def list_tables(self):
        """
        List all available table names.
        """
        if not self.tables:
            print("📭 No tables found.")
        else:
            print("📋 Available Tables:")
            for name in self.tables:
                print(f" - {name}")
        return list(self.tables.keys())

    def insert_into(self, table_name, record):
        """
        Insert a record into a specified table.
        """
        if table_name in self.tables:
            self.tables[table_name].insert(record)
        else:
            raise Exception(f"Table '{table_name}' not found.")

    def select_from(self, table_name, key):
        """
        Select a record by key from a table.
        """
        if table_name in self.tables:
            return self.tables[table_name].search(key)
        else:
            raise Exception(f"Table '{table_name}' not found.")

    def range_query(self, table_name, start_key, end_key):
        """
        Perform a range query on a specified table.
        """
        if table_name in self.tables:
            return self.tables[table_name].range_query(start_key, end_key)
        else:
            raise Exception(f"Table '{table_name}' not found.")

    def get_table(self, name):
        """
        Get a Table object by name (optional).
        """
        return self.tables.get(name, None)

    def delete_from(self, table_name, key):
        """
        Delete a record by primary key from a table.
        """
        if table_name in self.tables:
            self.tables[table_name].delete(key)
        else:
            raise Exception(f"Table '{table_name}' not found.")
        
    def save_to_disk(self, filename='database_dump.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.tables, f)
        print("💾 Database saved to disk.")

    def load_from_disk(self, filename='database_dump.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.tables = pickle.load(f)
            print("📥 Database loaded from disk.")
        else:
            print("⚠️ No saved database found.")