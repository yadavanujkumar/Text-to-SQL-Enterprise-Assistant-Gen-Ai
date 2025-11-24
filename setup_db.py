"""
Database Setup Script for Text-to-SQL Assistant
Creates a SQLite database with sample sales data for testing
"""

import sqlite3
from datetime import datetime, timedelta
import random


def create_database():
    """Create and populate the sales.db database with sample data"""
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS transactions')
    cursor.execute('DROP TABLE IF EXISTS products')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Sample product data
    products = [
        (1, 'Laptop Pro 15"', 'Electronics', 1299.99),
        (2, 'Wireless Mouse', 'Electronics', 29.99),
        (3, 'Mechanical Keyboard', 'Electronics', 89.99),
        (4, 'USB-C Hub', 'Electronics', 49.99),
        (5, 'Office Chair', 'Furniture', 299.99),
        (6, 'Standing Desk', 'Furniture', 599.99),
        (7, 'Monitor 27"', 'Electronics', 349.99),
        (8, 'Desk Lamp', 'Furniture', 39.99),
        (9, 'Noise Cancelling Headphones', 'Electronics', 199.99),
        (10, 'Webcam HD', 'Electronics', 79.99),
    ]
    
    # Insert products
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)
    
    # Generate 20 sample transactions
    transactions = []
    start_date = datetime.now() - timedelta(days=60)
    
    for i in range(1, 21):
        product_id = random.randint(1, 10)
        # Get the product price
        cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
        price = cursor.fetchone()[0]
        
        quantity = random.randint(1, 5)
        total_amount = round(price * quantity, 2)
        date = (start_date + timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
        
        transactions.append((i, product_id, date, quantity, total_amount))
    
    # Insert transactions
    cursor.executemany(
        'INSERT INTO transactions VALUES (?, ?, ?, ?, ?)',
        transactions
    )
    
    # Commit and close
    conn.commit()
    
    # Display summary
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM transactions')
    transaction_count = cursor.fetchone()[0]
    
    print(f"✓ Database created successfully!")
    print(f"✓ Created {product_count} products")
    print(f"✓ Created {transaction_count} transactions")
    print(f"✓ Database file: sales.db")
    
    conn.close()


if __name__ == '__main__':
    create_database()
