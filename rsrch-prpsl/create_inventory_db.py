import json
import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    category TEXT,
    supplier TEXT,
    cost_price REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_channels (
    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_name TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    channel_id INTEGER,
    quantity INTEGER NOT NULL,
    reorder_level INTEGER DEFAULT 10,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (channel_id) REFERENCES sales_channels(channel_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    channel_id INTEGER,
    quantity_sold INTEGER NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (channel_id) REFERENCES sales_channels(channel_id)
)
''')

# Read JSON data for products
with open('inventory_data.json', 'r') as file:
    inventory_data = json.load(file)

# Insert products
for item in inventory_data:
    cursor.execute('''
    INSERT INTO products (name, sku, category, supplier, cost_price)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        item['product_name'],
        item['sku'],
        item['category'],
        item['supplier'],
        item['unit_cost']
    ))

# Insert sales channels
channels = ['Website', 'Shopify', 'Amazon', 'WhatsApp', 'Facebook']
for channel in channels:
    cursor.execute('''
    INSERT INTO sales_channels (channel_name) VALUES (?)
    ''', (channel,))

# Get product ids
cursor.execute('SELECT product_id, sku FROM products')
products = cursor.fetchall()
product_dict = {sku: pid for pid, sku in products}

# Get channel ids
cursor.execute('SELECT channel_id, channel_name FROM sales_channels')
channels_db = cursor.fetchall()
channel_dict = {name: cid for cid, name in channels_db}

# Populate inventory: distribute quantities across channels
for item in inventory_data:
    sku = item['sku']
    total_quantity = item['quantity']
    reorder_level = item['reorder_point']
    pid = product_dict[sku]
    # Distribute quantity randomly among channels
    quantities = []
    remaining = total_quantity
    for i, channel in enumerate(channels):
        if i == len(channels) - 1:
            qty = remaining
        else:
            qty = random.randint(0, remaining // 2)
            remaining -= qty
        quantities.append(qty)
    for channel_name, qty in zip(channels, quantities):
        cid = channel_dict[channel_name]
        cursor.execute('''
        INSERT INTO inventory (product_id, channel_id, quantity, reorder_level)
        VALUES (?, ?, ?, ?)
        ''', (pid, cid, qty, reorder_level))

# Populate sales_orders: generate some sales data
# For each product, generate sales based on sales_last_30_days
for item in inventory_data:
    sku = item['sku']
    sales_30 = item['sales_last_30_days']
    pid = product_dict[sku]
    # Generate sales over last 30 days
    for _ in range(sales_30 // 10):  # Roughly 10 sales per day average
        channel_name = random.choice(channels)
        cid = channel_dict[channel_name]
        qty_sold = random.randint(1, 5)
        # Random date in last 30 days
        days_ago = random.randint(0, 29)
        sale_date = datetime.now() - timedelta(days=days_ago)
        cursor.execute('''
        INSERT INTO sales_orders (product_id, channel_id, quantity_sold, sale_date)
        VALUES (?, ?, ?, ?)
        ''', (pid, cid, qty_sold, sale_date.strftime('%Y-%m-%d %H:%M:%S')))

# Commit and close
conn.commit()
conn.close()

print("Inventory database created and populated successfully!")