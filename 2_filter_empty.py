import sqlite3
import pandas as pd
import yaml

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Connect to the database
db_path = config['db_name']
conn = sqlite3.connect(db_path)

# SQL query to select the required data
category_id = config['category']
query = f"""
SELECT w.ID, w.WORD, w.RUS, w.Q_REC, w.Q_REP
FROM WORD w
JOIN WORD_CATEGORY wc ON w.ID = wc.WORD_ID
WHERE wc.CATEGORY_ID = '{category_id}'
AND w.EXAMPLES_RUS IS NULL
AND (w.Q_REC <> w.Q_REP OR w.Q_REC IN (0, 2));
"""

# Execute the query and load the data into a DataFrame
df = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Save to a CSV file
csv_filename = "filtered.csv"
df.to_csv(csv_filename, index=False)

print(f"File {csv_filename} created successfully!")
print(f"Number of words: {len(df)}")
