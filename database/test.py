from db_manager import Database

# Initialize database
db = Database()
  
# Updated schema
schema = ['id', 'book_borrowed', 'book_title', 'book_author', 'book_publisher', 'book_year']
primary_key = 'id'

# Create table
db.create_table('library_borrowed_books', schema, primary_key) 

# Insert records
db.insert_into('library_borrowed_books', {
    'id': 101,
    'book_borrowed': 1,
    'book_title': 'Clean Code',
    'book_author': 'Robert C. Martin',
    'book_publisher': 'Prentice Hall',
    'book_year': 2008
})

db.insert_into('library_borrowed_books', {
    'id': 102,
    'book_borrowed': 1,
    'book_title': 'The Pragmatic Programmer',
    'book_author': 'Andy Hunt',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1999
})

# Select a record
record = db.select_from('library_borrowed_books', 101)
print("\nSelected Record:")
print(record)

# List all tables
print("\nAll Tables:")
db.list_tables()

# Delete a record
db.delete_from('library_borrowed_books', 102)
print("\nDeleted record with ID 102")

# Range query
print("\nRange Query (IDs 100 to 200):")
print(db.range_query('library_borrowed_books', 100, 200))

# Drop the table
db.drop_table('library_borrowed_books')



#task 6 
from db_manager import Database

db = Database()

# Load the database if it exists
db.load_from_disk()

# Create tables if not already present
try:
    schema_books = {
        'Book_ID': 'int',
        'Book_Name': 'varchar(100)',
        'Book_Author': 'varchar(100)',
        'Book_Publication_Year': 'year',
        'Total_Reviews': 'int',
        'Quantity': 'int',
        'BOOK_GENRE': 'varchar(1000)'
    }
    db.create_table('BOOKS_DETAILS', schema_books, 'Book_ID')
except Exception as e:
    print(e)

try:
    schema_logs = {
        'Log_ID': 'int',
        'Action': 'varchar(255)',
        'Timestamp': 'timestamp'
    }
    db.create_table('SYS_LOGS', schema_logs, 'Log_ID')
except Exception as e:
    print(e)

# Insert sample data
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

# Save to disk
db.save_to_disk()

# Load again to verify persistence
new_db = Database()
new_db.load_from_disk()

# List all table names and print one record
for table_name in new_db.tables:
    print(f"Table: {table_name}")
    all_records = new_db.tables[table_name].all_records()
    print(f"First record: {all_records[0] if all_records else 'No data'}")