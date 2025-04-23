import json
import os

class Database:
    def __init__(self):
        self.data = {}  # key = table name, value = { schema, primary_key, records }

    def create_table(self, table_name, schema, primary_key):
        if table_name in self.data:
            raise Exception(f"Table '{table_name}' already exists in database.")
        self.data[table_name] = {
            'schema': schema,
            'primary_key': primary_key,
            'records': []
        }

    def delete_table(self, table_name):
        if table_name not in self.data:
            raise Exception(f"Table '{table_name}' does not exist.")
        del self.data[table_name]

    def list_tables(self):
        return list(self.data.keys())

    def insert_into(self, table_name, record):
        if table_name not in self.data:
            raise Exception(f"Table '{table_name}' does not exist.")
        schema_keys = self.data[table_name]['schema'].keys()
        for key in schema_keys:
            if key not in record:
                raise Exception(f"Missing column '{key}' in the record.")
        self.data[table_name]['records'].append(record)

    def save_to_disk(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def load_from_disk(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError("No persistent file found.")
        with open(filename, 'r') as f:
            self.data = json.load(f)


db = Database()
filename = 'library_db.json'

# Load or initialize
try:
    db.load_from_disk(filename)
    print("Database loaded from disk.")
except FileNotFoundError:
    print("No persistent file found.")
    db.save_to_disk(filename)

# Schemas
schema_books = {
    'Book_ID': 'int',
    'Book_Name': 'varchar(100)',
    'Book_Author': 'varchar(100)',
    'Book_Publication_Year': 'year',
    'Total_Reviews': 'int',
    'Quantity': 'int',
    'BOOK_GENRE': 'varchar(1000)'
}

schema_logs = {
    'Log_ID': 'int',
    'Action': 'varchar(255)',
    'Timestamp': 'timestamp'
}

# Create Tables
if 'BOOKS_DETAILS' not in db.list_tables():
    db.create_table('BOOKS_DETAILS', schema_books, 'Book_ID')

if 'SYS_LOGS' not in db.list_tables():
    db.create_table('SYS_LOGS', schema_logs, 'Log_ID')

# Insert Records
try:
    db.insert_into('BOOKS_DETAILS', {
        'Book_ID': 1,
        'Book_Name': '1984',
        'Book_Author': 'George Orwell',
        'Book_Publication_Year': 1949,
        'Total_Reviews': 8945,
        'Quantity': 10,
        'BOOK_GENRE': 'Dystopian Fiction'
    })

    db.insert_into('SYS_LOGS', {
        'Log_ID': 1,
        'Action': 'Insert Book',
        'Timestamp': '2025-04-20 14:00:00'
    })

    db.save_to_disk(filename)
    print("Data inserted and saved.")
except Exception as e:
    print("Insert Error:", e)

# Verify
try:
    verify = Database()
    verify.load_from_disk(filename)
    for table, content in verify.data.items():
        print(f"\nTable: {table}")
        print("First record:", content['records'][0] if content['records'] else "No data")
except Exception as e:
    print("Load Error:", e)