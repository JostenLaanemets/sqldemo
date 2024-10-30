import sqlite3

conn = sqlite3.connect('liiklusstatistika.db')
cursor = conn.cursor()




### MITU SOIDUKIT ON REGISTRIS ###

print("#####################################")
cursor.execute('''
    SELECT YLDINE_STAATUS, COUNT(*) AS Arv
    FROM Soidukid
    GROUP BY YLDINE_STAATUS 
''')

tulemused = cursor.fetchall()

for staatus, arv in tulemused:
    print(f"{staatus}: {arv}")


### POPULAARSEMAD MARGID ###
print("#####################################")

cursor.execute('''
    SELECT MARK, MUDEL, COUNT(*) AS kogus
    FROM Soidukid
    GROUP BY MARK, MUDEL
    ORDER BY kogus DESC
    LIMIT 10;
''')

populaarsed_autod = cursor.fetchall()
for mark, mudel, kogus in populaarsed_autod:
    print(f"{mark} {mudel}: {kogus} autot")

print("#####################################")

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

print("#####################################")

### BENSIINI AUTOD ###

cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'BENSIIN'
''')
bensiin = cursor.fetchone()[0]
print(f"Kokku on bensiiniautosid: {bensiin}")

### DIISEL AUTOD ###
cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'DIISEL'
''')
diisel = cursor.fetchone()[0]
print(f"Kokku on diiselautosid: {diisel}")


### LPG AUTOD ###
cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'LPG'
''')
lpg = cursor.fetchone()[0]
print(f"Kokku on lpg-ga autosid: {lpg}")

### CNG AUTOD ###
cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'CNG'
''')
cng = cursor.fetchone()[0]
print(f"Kokku on cng-ga autosid: {cng}")


print("#####################################")

### ELEKTRI AUTOD ###

cursor.execute('''
    SELECT COUNT(*) AS Kokku 
    FROM Soidukid 
    WHERE MOOTORI_TYYP = 'ELEKTER'
''')
elektrilised = cursor.fetchone()[0]
print(f"Kokku on elektriautosid: {elektrilised}")


cursor.execute('''
    SELECT MARK, MUDEL, COUNT(*) AS Arv
    FROM Soidukid
    WHERE MOOTORI_TYYP = 'ELEKTER'
    GROUP BY MARK, MUDEL
    ORDER BY Arv DESC
    LIMIT 3
''')


tulemused = cursor.fetchall()
for mark, mudel, arv in tulemused:
    print(f"{mark} {mudel}: {arv} autot")

print("#####################################")

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

print("#####################################")

cursor.execute('''
    SELECT COUNT(*) AS Registreeritud_Autod
    FROM Soidukid
    WHERE ESMANE_REG > '2024-01-01'
''')

registreeritud_autod = cursor.fetchone()[0]

print(f"Registreeritud autod pärast 2024-01-01: {registreeritud_autod}")


print("#####################################")

cursor.execute('''
    SELECT Maakonnad.MAAKOND, COUNT(Soidukid.SOIDUKI_ID) AS Registreeritud_Soidukid
    FROM Maakonnad
    LEFT JOIN Soidukid ON Maakonnad.MAAKOND_ID = Soidukid.MAAKOND_ID
    GROUP BY Maakonnad.MAAKOND
    ORDER BY Registreeritud_Soidukid DESC
''')


maakonnad_sõidukid = cursor.fetchall()

print("Registreeritud sõidukite arv igas maakonnas:")
for maakond, arv in maakonnad_sõidukid:
    print(f"{maakond}: {arv} sõidukit")

print("#####################################")


cursor.execute('''
    SELECT Maakonnad.MAAKOND, COUNT(Liiklusonnetused.Juhtuminr) AS OnnetusteArv
    FROM Liiklusonnetused
    JOIN Maakonnad ON Liiklusonnetused.MAAKOND_ID = Maakonnad.MAAKOND_ID
    WHERE Liiklusonnetused.Toimumisaeg >= '2024-01-01'
    GROUP BY Maakonnad.MAAKOND
    ORDER BY OnnetusteArv DESC
''')

results = cursor.fetchall()
print("Liiklusõnnetuste arv maakondade kaupa alates 2024. aastast:")
for row in results:
    maakond, onnetuste_arv = row
    print(f"{maakond}: {onnetuste_arv} õnnetust")

print("#####################################")

cursor.execute('''
    SELECT SUM(Joobesmootorsõidukijuhiosalusel) AS JoobesJuhid
    FROM Liiklusonnetused
    WHERE Toimumisaeg >= '2024-01-01'
''')

joobes_juhid = cursor.fetchone()[0]
print(f"Alates 2024. aastast on joobes juhte Eestis olnud: {joobes_juhid}")

print("#####################################")

cursor.execute('''
    SELECT COUNT(*) AS Asulas
    FROM Liiklusonnetused
    WHERE Asula = 'JAH' AND Toimumisaeg >= '2020-01-01'
''')

asulas = cursor.fetchone()[0]

cursor.execute('''
    SELECT COUNT(*) AS valjas
    FROM Liiklusonnetused
    WHERE Asula = 'EI' AND Toimumisaeg >= '2020-01-01'
''')

valjas = cursor.fetchone()[0]
print("Alates 2020")
print(f"Asulas toimus liiklusõnnetusi: {asulas}")
print(f"Välistes piirkondades toimus liiklusõnnetusi: {valjas}")

print("#####################################")


cursor.execute('''
    SELECT COUNT(*) AS Pime_Aeg_Arv
    FROM Liiklusonnetused
    WHERE Valgustus = 'Pimeda aeg'
''')

pime_aeg_arv = cursor.fetchone()[0]
print(f"Liiklusõnnetused pimedas: {pime_aeg_arv}")

cursor.execute('''
    SELECT COUNT(*) AS Valge_Aeg_Arv
    FROM Liiklusonnetused
    WHERE Valgustus = 'Valge aeg'
''')

valge_aeg_arv = cursor.fetchone()[0]
print(f"Liiklusõnnetused valges: {valge_aeg_arv}")


conn.close()
