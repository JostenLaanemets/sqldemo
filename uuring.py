import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()

### LUKSUSAUTOD ###

cursor.execute('''
    SELECT COUNT(*) AS Arv, MARK 
    FROM Soidukid 
    WHERE MARK IN ('LAMBORGHINI', 'FERRARI') 
    GROUP BY MARK
''')
Autod = cursor.fetchall()
for i in Autod:
    print(f"{i[1]} marke on Eestis: {i[0]}")


### ELEKTRI AUTOD ###

cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'ELEKTER'
''')
elektrilised = cursor.fetchone()[0]
print(f"Kokku on elektriautosid: {elektrilised}")


cursor.execute('''
    SELECT COUNT(*) AS Teslad 
    FROM Soidukid 
    WHERE MARK = 'TESLA'
''')
teslad = cursor.fetchone()[0]

print(f"Tesla marke: {teslad}")


### PIKIM SÕIDUK ###
cursor.execute('''
    SELECT MARK, MUDEL, PIKKUS
    FROM Soidukid
    WHERE PIKKUS = (SELECT MAX(PIKKUS) FROM Soidukid)
''')

pikim_auto = cursor.fetchone()

if pikim_auto:
    mark, mudel, pikkus = pikim_auto
    print(f"Pikim auto on: {mark} {mudel} (Pikkus: {pikkus} mm)")


#

conn.close()
