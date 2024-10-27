import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()


##############
### SELECT ###
##############

### COUNT ####
cursor.execute('''
    SELECT COUNT(*)
    FROM liiklusonnetused
''')
liiklusonnetused = cursor.fetchone()[0]
print(f"Kokku on {liiklusonnetused} liiklusõnnetust.")



### AVERAGE ###
cursor.execute('''
    SELECT AVG(MOOTORI_VOIMSUS)
    FROM Soidukid
''')
voimsus = int(cursor.fetchone()[0])
print(f"Autode keskmine mootori võimsus on {voimsus} kw.")



### SUMMARISE ###
# kasutan AS aliase määramiseks
cursor.execute('''
    SELECT  SUM(Isikuid) as Isikuid_Kokku,
            SUM(Hukkunuid) AS Hukkunuid_Kokku,
            SUM(Vigastatuid) AS Vigastatuid_Kokku,
            SUM(Sõidukeid) AS Sõidukeid_Kokku
    FROM liiklusonnetused
''')
isikuid ,hukkunuid, vigastatud, soidukeid  = cursor.fetchone()
print(f"Liiklusõnnetustes oli kokku {isikuid} isikut, {soidukeid} sõidukit, kellest {vigastatud} said viga ja {hukkunuid} hukkus.")


### MAX ###
cursor.execute('''
    SELECT Max(MOOTORI_VOIMSUS)
    FROM Soidukid
''')
voimsus = int(cursor.fetchone()[0])
print(f"suurima võimsusega on {voimsus} kw.")


### MIN ###
cursor.execute('''
    SELECT Min(SUURIM_KIIRUS)
    FROM Soidukid
''')
kiirus = int(cursor.fetchone()[0])
print(f"Kõige väiksem määratud sõidukiirus on {kiirus} km/h.")




### GROUP BY ###
### ORDER BY ###
### LIMIT    ###
cursor.execute('''
    SELECT omavalitsus, COUNT(*) AS onnetused_kokku
    FROM liiklusonnetused
    GROUP BY omavalitsus
    ORDER BY onnetused_kokku DESC
    LIMIT 1
''')
linn, onnetused  = cursor.fetchone()
print(f"Kõige rohkem õnnetusi toimus linnas {linn}, {onnetused} õnnetust.")


cursor.execute('''
    SELECT MARK, MUDEL, COUNT(*) AS Arv
    FROM Soidukid
    WHERE MAAKOND_ID = (SELECT MAAKOND_ID FROM Maakonnad WHERE MAAKOND = 'Põlva')
    GROUP BY MARK, MUDEL
    ORDER BY Arv DESC
    LIMIT 1;
''')
mark, mudel, kogus  = cursor.fetchone()
print(f"Populaarseim auto Põlvas on: {mark} {mudel} (Arv: {kogus})")



### HAVING ###
cursor.execute('''
    SELECT COUNT(*) 
    FROM Soidukid
    WHERE SOIDUMYRA > 90
''')
arv = cursor.fetchone()[0]
print(f"Autode arv, mille sõidumüra on suurem kui 90 db: {arv}")


################
### DISTINCT ###
################
cursor.execute("""
    SELECT DISTINCT Liiklusõnnetuseliik 
    FROM liiklusonnetused
""")
liigid = cursor.fetchall()
print("Unikaalsed liiklusõnnetuseliigid:", [liik[0] for liik in liigid])



#############
### ALTER ###
#############

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tootjariigid (
        RIIGI_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        RIIGI_NIMI TEXT UNIQUE NOT NULL
    )
''')

### ADD ###
try:
    cursor.execute('''ALTER TABLE Tootjariigid ADD COLUMN TEHASE_NIMI TEXT''')
    conn.commit()
except sqlite3.OperationalError as e:
    cursor.execute('''ALTER TABLE Tootjariigid ADD COLUMN TEHASE_NIMI TEXT''')
    print(e)
### RENAME ###

try:
    cursor.execute(''' ALTER TABLE Tootjariigid RENAME COLUMN RIIGI_NIMI TO RIIK''')
except sqlite3.OperationalError as e:
    cursor.execute(''' ALTER TABLE Tootjariigid RENAME COLUMN RIIK TO RIIGI_NIMI''')
    print(e)

##############
### UPDATE ###
##############

cursor.execute('''
    UPDATE Kategooriad
    SET KATEGOORIA = 'Uus Kategooria'
    WHERE KATEGOORIA_ID = 3
''')

conn.commit()



############
### JOIN ###
############

### INNER JOIN ###
cursor.execute('''
    SELECT Soidukid.MARK, Soidukid.MUDEL, Kategooriad.KATEGOORIA
    FROM Soidukid
    INNER JOIN Kategooriad ON Soidukid.KATEGOORIA_ID = Kategooriad.KATEGOORIA_ID
    LIMIT 3
''')
results = cursor.fetchall()
for row in results:
    print(row)

print("--------------------------")

### LEFT JOIN ###
cursor.execute('''
    SELECT Soidukid.MARK, Soidukid.MUDEL, Kategooriad.KATEGOORIA
    FROM Soidukid
    LEFT JOIN Kategooriad ON Soidukid.KATEGOORIA_ID = Kategooriad.KATEGOORIA_ID
    LIMIT 3
''')
results = cursor.fetchall()
for row in results:
    print(row)

print("--------------------------")

### CROSS JOIN ###
cursor.execute('''
    SELECT Soidukid.MARK, Kategooriad.KATEGOORIA
    FROM Soidukid
    CROSS JOIN Kategooriad
    LIMIT 6
''')
results = cursor.fetchall()
for row in results:
    print(row)


# Andmebaasiga ühenduse katkestamine
conn.close()

