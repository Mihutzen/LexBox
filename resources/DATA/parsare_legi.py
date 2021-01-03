import mysql.connector

def get_connection():
    try:
        con = mysql.connector.connect(
            user='lexboxapp', password='', host='localhost', database='lexbox')
        con.connect()
        return con
    except Exception as e:
        print(e)

def isArtNumber(string):
    if string[0] == "A":
        if "Art. " in string:
            return True
    return False

def getArtNumber(string):
    number = ""
    for i in string:
        try:
            int(i)
            number += i
        except:
            pass
    return number

def isParagraphNumber(string):
    if string[0] == "(":
        return True
    return False

def getParagraphNumber(string):
    result = ""
    brackets = 0
    for i in string:
        if i == "(":
            brackets += 1
        elif i == ")":
            brackets -= 1
        elif i != "(" and i != ")":
            result += i
        if brackets == 0:
            return result

def getRuleOfNumber(string):
    result = ""
    read = False
    for i in string:
        if not read:
            if i == ")":
                read = True
                continue
        else:
            result += i
    return result

def isCharRule(string):
    if string[1] == ")":
        return True
    return False

def getCharRule(string):
    result = ""
    for i in string:
        if i == ")":
            return result
        else:
            result += i

def getRuleOfChar(string):
    return string[2:]



data = open("legi.txt", "r", encoding="utf-8")


insertQuery = """INSERT INTO lege(articol,aliniat,litera,textlege) VALUES (%s,%s,%s,%s)"""

firstinsert = False
articol = ""
aliniat = ""
litera = ""
textlege = ""

temptextlegeA = ""
temptextlegeB = ""


for i in data:
    if i == "\n":
        if temptextlegeB != "":
            pass
        elif temptextlegeA != "":
            inserBlobTouple = (articol, aliniat, litera, temptextlegeA)
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(insertQuery, inserBlobTouple)
            con.commit()
            con.close()
        else:
            inserBlobTouple = (articol, aliniat, litera, textlege)
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(insertQuery, inserBlobTouple)
            con.commit()
            con.close()
           
        articol = ""
        aliniat = ""
        litera = ""
        textlege = ""
        temptextlegeA = ""
        temptextlegeB = ""
    elif not isArtNumber(i) and not isCharRule(i) and not isParagraphNumber(i):
        textlege += i
    
    elif isArtNumber(i):
        articol = getArtNumber(i)
        continue

    elif isParagraphNumber(i):
        if aliniat == "":
            aliniat = getParagraphNumber(i)
            temptextlegeA = getRuleOfNumber(i)
        elif litera == "" and aliniat != "":
            if textlege != "":
                inserBlobTouple = (articol, aliniat, litera, textlege + temptextlegeA)
            else:
                inserBlobTouple = (articol, aliniat, litera,temptextlegeA)
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(insertQuery, inserBlobTouple)
            con.commit()
            con.close()

            temptextlegeA = textlege + getRuleOfNumber(i)
            aliniat = getParagraphNumber(i)
            litera = ""

    elif isCharRule(i):
        if textlege != "":
            temptextlegeB = textlege + " " + temptextlegeA + " " + getRuleOfChar(i)
        else:
            temptextlegeB = temptextlegeA + " " + getRuleOfChar(i)
        inserBlobTouple = (articol, aliniat, getCharRule(i), temptextlegeB)
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(insertQuery, inserBlobTouple)
        con.commit()
        con.close()


        
    
    




