import sqlite3
import pandas as pd

# Отключить ограничение на количество строк
pd.set_option('display.max_rows', None)

# Отключить ограничение на количество столбцов
pd.set_option('display.max_columns', None)

# Отключить ограничение на ширину вывода (чтобы длинные строки отображались полностью)
pd.set_option('display.max_colwidth', None)

# Подключение к базе данных
db_path = "reword_de.backup"  # Укажите путь к вашему файлу базы данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Запрос списка таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Вывод списка таблиц
if tables:
    print("Список таблиц в базе данных:")
    for table in tables:
        print(table[0])
else:
    print("В базе данных нет таблиц или она пуста.")

table_name = 'WORD'
# Запрос нескольких строк
query = f"SELECT * FROM {table_name} WHERE EXAMPLES_RUS IS NOT NULL LIMIT 10;"
df = pd.read_sql(query, conn)
print(df)


table_name = 'WORD_CATEGORY'
query = f'SELECT DISTINCT CATEGORY_ID FROM {table_name};'
df = pd.read_sql(query, conn)
print(df)

# Закрытие соединения
conn.close()
