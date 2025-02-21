import sqlite3
import pandas as pd

# Подключение к базе данных
db_path = "reword_de.backup"
conn = sqlite3.connect(db_path)

# SQL-запрос для выборки нужных данных
category_id = 'top4000'
query = f"""
SELECT w.ID, w.WORD, w.RUS, w.Q_REC, w.Q_REP
FROM WORD w
JOIN WORD_CATEGORY wc ON w.ID = wc.WORD_ID
WHERE wc.CATEGORY_ID = '{category_id}'
AND w.EXAMPLES_RUS IS NULL
AND (w.Q_REC <> w.Q_REP OR w.Q_REC IN (0, 2));
"""

# Выполнение запроса и загрузка данных в DataFrame
df = pd.read_sql(query, conn)

# Закрытие соединения
conn.close()

# Сохранение в CSV-файл
csv_filename = "filtered.csv"
df.to_csv(csv_filename, index=False)

print(f"Файл {csv_filename} успешно создан!")
print(f"Количество слов: {len(df)}")
