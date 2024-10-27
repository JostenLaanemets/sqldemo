import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maakonnad 
        (MAAKOND_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MAAKOND TEXT NOT NULL UNIQUE)''')

counties = ['Harju', 'Tartu', 'Võru', 'Põlva', 'Valga', 'Viljandi', 
            'Pärnu', 'Rapla', 'Lääne-Viru', 'Ida-Viru', 'Lääne', 
            'Hiiu', 'Saare', 'Järva', 'Jõgeva']

for county in counties:
    cursor.execute("INSERT OR IGNORE INTO Maakonnad (MAAKOND) VALUES (?)", (county,))


try:
    cursor.execute("ALTER TABLE Soidukid ADD COLUMN MAAKOND_ID INTEGER")
except sqlite3.OperationalError as e:
    print(e)

try:
    cursor.execute("ALTER TABLE Liiklusonnetused ADD COLUMN MAAKOND_ID INTEGER")
except sqlite3.OperationalError as e:
    print(e)


for county in counties:
    cursor.execute("SELECT MAAKOND_ID FROM Maakonnad WHERE MAAKOND = ?", (county,))
    county_id = cursor.fetchone()

    if county_id:
        cursor.execute("UPDATE Soidukid SET MAAKOND_ID = ? WHERE VKOM_MAAKOND = ?", (county_id[0], county))

        county = county + " maakond"
        cursor.execute("UPDATE Liiklusonnetused SET MAAKOND_ID = ? WHERE Maakond = ?", (county_id[0], county))



conn.commit()

conn.close()







