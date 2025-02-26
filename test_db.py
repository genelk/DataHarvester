import sqlite3
import os

# Print the absolute path to help find the file
db_path = 'movie_data.db'
abs_path = os.path.abspath(db_path)
print(f"Looking for database at: {abs_path}")
print(f"File exists: {os.path.exists(abs_path)}")

# Try to open and read from the database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")
    
    # Try to read from movies table
    if ('movies',) in tables:
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        print(f"Number of movies in database: {count}")
    
    conn.close()
    print("Database connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")
