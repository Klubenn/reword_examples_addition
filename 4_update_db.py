import sqlite3
import pandas as pd

# Reading data from CSV file
csv_filename = 'filtered.csv'
df = pd.read_csv(csv_filename)

# Connecting to the database
db_path = "reword_de.backup"  # Specify the path to your SQLite file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Updating data in the database
for index, row in df.iterrows():
    cursor.execute("""
        UPDATE WORD
        SET EXAMPLES_RUS = ?
        WHERE ID = ?
    """, (row['EXAMPLES_RUS'], row['ID']))

# Saving changes and closing the connection
conn.commit()
conn.close()

print(f"Database successfully updated with data from {csv_filename}!")