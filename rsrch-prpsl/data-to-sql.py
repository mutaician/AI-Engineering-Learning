import json
import sqlite3

# Read JSON data
with open('inventory_data.json', 'r') as file:
    inventory_data = json.load(file)

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    unit_cost REAL,
    selling_price REAL,
    supplier TEXT,
    warehouse TEXT,
    location TEXT,
    last_restocked DATE,
    reorder_point INTEGER,
    stock_status TEXT,
    batch_id TEXT,
    expiry_date DATE,
    sales_last_30_days INTEGER
)
''')

# Insert data
for item in inventory_data:
    cursor.execute('''
    INSERT OR REPLACE INTO inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item['sku'],
        item['product_name'],
        item['category'],
        item['quantity'],
        item['unit_cost'],
        item['selling_price'],
        item['supplier'],
        item['warehouse'],
        item['location'],
        item['last_restocked'],
        item['reorder_point'],
        item['stock_status'],
        item['batch_id'],
        item['expiry_date'],
        item['sales_last_30_days']
    ))

# Commit and close
conn.commit()
conn.close()

print("Data successfully imported to SQLite database!")