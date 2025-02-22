import sqlite3
import pandas as pd

# Disable row limit
pd.set_option('display.max_rows', None)

# Disable column limit
pd.set_option('display.max_columns', None)

# Disable output width limit (to display long strings fully)
pd.set_option('display.max_colwidth', None)

# Connect to the database
db_path = "reword_de.backup"  # Specify the path to your database file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the list of tables
if tables:
    print("List of tables in the database:")
    for table in tables:
        print(table[0])
else:
    print("There are no tables in the database or it is empty.")


# Find and print categories
print("\nList of categories:")
table_name = 'WORD_CATEGORY'
query = f'SELECT DISTINCT CATEGORY_ID FROM {table_name};'
df = pd.read_sql(query, conn)
for category_id in df['CATEGORY_ID']:
    print(category_id)

# Close the connection
conn.close()
