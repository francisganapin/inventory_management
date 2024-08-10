import os
import sqlite3

# Define the current directory and the database file path
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'database.db')

# Connect to the SQLite database
conn = sqlite3.connect(file_path)
cursor = conn.cursor()

# Create the products table if it doesn't exist
#cursor.execute('''
#CREATE TABLE "products" (
#	"id"	INTEGER UNIQUE,
#	"name"	TEXT,
#	"brand"	TEXT,
#	"color"	TEXT,
#	"date"	DATE,
#	"category"	TEXT,
#	"quantity"	INTEGER,
##	PRIMARY KEY("id" AUTOINCREMENT)
#);
#''')

# Function to insert a product into the database

# Sample data to insert
products = [
    ('Product2', 'BrandB', 'Blue', '2024-08-02', 'Category2', 20),
    ('Product3', 'BrandC', 'Green', '2024-08-03', 'Category3', 30),
]


def insert_product(name, brand, color, date, category, quantity):
    try:
        cursor.execute('''INSERT INTO products
                        (name, brand, color, date, category, quantity)
                        VALUES (?, ?, ?, ?, ?, ?)''', 
                        (name, brand, color, date, category, quantity))
        conn.commit()
        print('ok na po na insert na')
    except sqlite3.IntegrityError:
        print('Integrity error occurred.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # Insert sample data into the database
        for product in products:
            insert_product(*product)
        conn.close()

# Sample data to insert
