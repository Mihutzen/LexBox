import mysql.connector

def get_connection():
    try:
        con = mysql.connector.connect(
            user='lexboxapp', password='', host='localhost', database='lexbox')
        con.connect()
        return con
    except Exception as e:
        print(e)


data = open("LISTAJDUECATORII.txt", "r", encoding="utf-8")


insertQuery = """INSERT INTO institutie(id,nume,localitate,judet) VALUES (%s,%s,%s,%s)"""

idcounter = 0
isjudet = True
curentJudet = ""
for i in data:
    if i == "\n":
        isjudet = True
        curentJudet = ""
        continue
    if isjudet:
        curentJudet = i
        isjudet=False
        continue
    
    inserBlobTouple = (idcounter,"Judecătoria " + i[:-1], i[:-1], curentJudet[:-1])
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(insertQuery, inserBlobTouple)
    con.commit()
    con.close()
    idcounter=idcounter+1




