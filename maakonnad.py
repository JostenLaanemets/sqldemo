import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maakonnad 
        (MAAKOND_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MAAKOND TEXT NOT NULL UNIQUE)''')

maakonnad = ['Harju', 'Tartu', 'Võru', 'Põlva', 'Valga', 'Viljandi', 
            'Pärnu', 'Rapla', 'Lääne-Viru', 'Ida-Viru', 'Lääne', 
            'Hiiu', 'Saare', 'Järva', 'Jõgeva']

for c in maakonnad:
    cursor.execute("INSERT OR IGNORE INTO Maakonnad (MAAKOND) VALUES (?)", (c,))

try:
    cursor.execute("ALTER TABLE Soidukid ADD COLUMN MAAKOND_ID INTEGER")
except sqlite3.OperationalError as e:
    print(e)

try:
    cursor.execute("ALTER TABLE Liiklusonnetused ADD COLUMN MAAKOND_ID INTEGER")
except sqlite3.OperationalError as e:
    print(e)

for c in maakonnad:
    cursor.execute("SELECT MAAKOND_ID FROM Maakonnad WHERE MAAKOND = ?", (c,))
    maakonna_id = cursor.fetchone()
    if maakonna_id:
        cursor.execute("UPDATE Soidukid SET MAAKOND_ID = ? WHERE VKOM_MAAKOND = ?", (maakonna_id[0], c))
        county = county + " maakond"
        cursor.execute("UPDATE Liiklusonnetused SET MAAKOND_ID = ? WHERE Maakond = ?", (maakonna_id[0], c))

conn.commit()
conn.close()



