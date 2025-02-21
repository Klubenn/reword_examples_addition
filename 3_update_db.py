import sqlite3
import pandas as pd

# Чтение данных из CSV файла
csv_filename = 'filtered.csv'
df = pd.read_csv(csv_filename)

# Подключение к базе данных
db_path = "reword_de.backup"  # Укажите путь к вашему файлу SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Обновление данных в базе данных
for index, row in df.iterrows():
    cursor.execute("""
        UPDATE WORD
        SET EXAMPLES_RUS = ?
        WHERE ID = ?
    """, (row['EXAMPLES_RUS'], row['ID']))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print(f"База данных успешно обновлена данными из {csv_filename}!")