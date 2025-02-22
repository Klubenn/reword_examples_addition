import sqlite3
import pandas as pd
import yaml

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Disable row limit
pd.set_option('display.max_rows', None)

# Disable column limit
pd.set_option('display.max_columns', None)

# Disable output width limit (to display long strings fully)
pd.set_option('display.max_colwidth', None)

# Connect to the database
db_path = config['db_name']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# List all column names in the table WORD
print("List of column names:")
table_name = 'WORD'
cursor.execute(f'PRAGMA table_info({table_name});')
columns = cursor.fetchall()
print(f"\nList of columns in the table {table_name}:")
for column in columns:
    print(column[1])

# Find and print categories
print("\nList of categories:")
table_name = 'WORD_CATEGORY'
query = f'SELECT DISTINCT CATEGORY_ID FROM {table_name};'
df = pd.read_sql(query, conn)
for category_id in df['CATEGORY_ID']:
    print(category_id)

# Close the connection
conn.close()
