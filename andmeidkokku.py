import sqlite3
conn = sqlite3.connect('liiklusstatistika.db')

cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
total_records = 0

for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    total_records += count
    print(f"Tabel '{table_name}' on andmeid: {count} ")


print(f"Kokku on andmeid {total_records} ")

conn.close()
