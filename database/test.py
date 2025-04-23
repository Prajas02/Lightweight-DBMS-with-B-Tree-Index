#task 5
from db_manager import Database

# Initialize database
db = Database()
  
# Updated schema
schema = ['id', 'book_borrowed', 'book_title', 'book_author', 'book_publisher', 'book_year']
primary_key = 'id'

# Create table
db.create_table('library_db', 'library_borrowed_books', schema)

db.insert_into('library_db', 'library_borrowed_books', {
    'id': 103,
    'book_borrowed': 1,
    'book_title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
    'book_author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1994
})

db.insert_into('library_db', 'library_borrowed_books', {
    'id': 104,
    'book_borrowed': 1,
    'book_title': 'Refactoring: Improving the Design of Existing Code',
    'book_author': 'Martin Fowler',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1999
})


# Insert records into 'library_borrowed_books'
db.insert_into('library_db', 'library_borrowed_books', {
    'id': 101,
    'book_borrowed': 1,
    'book_title': 'Clean Code',
    'book_author': 'Robert C. Martin',
    'book_publisher': 'Prentice Hall',
    'book_year': 2008
})

db.insert_into('library_db', 'library_borrowed_books', {
    'id': 102,
    'book_borrowed': 1,
    'book_title': 'The Pragmatic Programmer',
    'book_author': 'Andy Hunt',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1999
})

db.insert_into('library_db', 'library_borrowed_books', {
    'id': 103,
    'book_borrowed': 1,
    'book_title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
    'book_author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1994
})

db.insert_into('library_db', 'library_borrowed_books', {
    'id': 104,
    'book_borrowed': 1,
    'book_title': 'Refactoring: Improving the Design of Existing Code',
    'book_author': 'Martin Fowler',
    'book_publisher': 'Addison-Wesley',
    'book_year': 1999
})

# Delete record with ID 102
db.delete_from('library_db', 'library_borrowed_books', 102)
print("\nDeleted record with ID 102")

# Range query (IDs 100 to 200)
print("\nRange Query (IDs 100 to 200):")
print(db.range_query('library_db', 'library_borrowed_books', 100, 200))

# Drop the table
db.drop_table('library_db', 'library_borrowed_books')
print("\nTable 'library_borrowed_books' dropped successfully.")