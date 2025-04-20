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