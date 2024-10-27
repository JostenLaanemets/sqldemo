import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Kategooriad 
        (KATEGOORIA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        KATEGOORIA TEXT NOT NULL UNIQUE)''')


cursor.execute("INSERT OR IGNORE INTO Kategooriad (KATEGOORIA) VALUES ('M1')")
cursor.execute("INSERT OR IGNORE INTO Kategooriad (KATEGOORIA) VALUES ('M1G')")
 

try:
    cursor.execute("ALTER TABLE Soidukid ADD COLUMN KATEGORIA_ID INTEGER")
     
except sqlite3.OperationalError as e:
    print(e)


cursor.execute("SELECT KATEGOORIA_ID FROM Kategooriad WHERE KATEGOORIA = 'M1'")
m1_id = cursor.fetchone()

cursor.execute("SELECT KATEGOORIA_ID FROM Kategooriad WHERE KATEGOORIA = 'M1G'")
m1g_id = cursor.fetchone()

if m1_id:
    cursor.execute("UPDATE Soidukid SET KATEGORIA_ID = ? WHERE KATEGOORIA = 'M1'", (m1_id[0],))
if m1g_id:
    cursor.execute("UPDATE Soidukid SET KATEGORIA_ID = ? WHERE KATEGOORIA = 'M1G'", (m1g_id[0],))


conn.commit()
conn.close()

#
