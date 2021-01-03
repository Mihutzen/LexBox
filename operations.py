from docx import Document
import mysql.connector
import random
import string

def get_connection():
    try:
        con = mysql.connector.connect(
            user='lexboxapp', password='', host='localhost', database='lexbox')
        con.connect()
        return con
    except Exception as e:
        print(e)

def generateToken():
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(15))
    return result

def logout(username):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("delete from lexbox.token where id=ANY(SELECT id FROM lexbox.user where username='{username}')".format(username=username))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return 2


def logoutByToken(token):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("delete from lexbox.token where token = '{t}'".format(t=token))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return 2

def login(username, password):
    try:
        if checkCredentials(username, password):
            logout(username)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("insert into lexbox.token(id, token) select id, '{token}' from lexbox.user where user.username='{username}'".format(username=username, token=generateToken()))
            connection.commit()
            connection.close()
            return True
        else:
            return False
    except Exception as e:
        return 2

def register(username, password1, password2):
    if password1 == password2:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO `lexbox`.`user` (`username`, `password`) VALUES('{username}', '{password}'".format(username=username, password=password1))
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            return 2
    else:
        return False

def checkToken(token):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select count(*) from lexbox.token where token = '{s}'".format(s=str(token)))
        record = cursor.fetchall()
        connection.close()
        if record[0][0] == 0:
            return False
        else:
            return True
    except Exception as e:
        return 2

def getToken(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select token from lexbox.token inner join (select id from lexbox.user where username = '{username}') as x on lexbox.token.id = x.id".format(username=username))
    record = cursor.fetchall()
    connection.close()
    return record[0][0]

def checkCredentials(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute( "select count(*) from lexbox.user where password = '{password}' and username = '{user}' ".format(password=str(password),user=str(username)))
        record = cursor.fetchall()
        connection.close()
        if record[0][0] == 0:
            return False
        else:
            return True
    except Exception as e:
        return 2


def getResultsByName(nume, prenume):
    if len(nume) > 3 and len(prenume) > 3:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select id, nume, prenume, telefon, serieBuletin, numarBuletin, cnp, adresaProceduralaStrada, adresaProceduralaNumar, adresaProceduralaOras, adresaProceduralaJudet, adresaProceduralaBloc, adresaProceduralaScara, adresaProceduralaApartament, adresaProceduralaApartament, adresaProceduralaCodPostal, numeAgent, prenumeAgent, institutieAgent, serieProcesVerbal from lexbox.instance where nume like '%{nume}%' and prenume like '%{prenume}%' limit 15".format(nume=nume, prenume=prenume))
        records = cursor.fetchall()
        connection.close()
        return records
    else:
        return []

def getResultsByCNP(CNP):
    if len(CNP)>4:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select id, nume, prenume, telefon, serieBuletin, numarBuletin, cnp, adresaProceduralaStrada, adresaProceduralaNumar, adresaProceduralaOras, adresaProceduralaJudet, adresaProceduralaBloc, adresaProceduralaScara, adresaProceduralaApartament, adresaProceduralaApartament, adresaProceduralaCodPostal, numeAgent, prenumeAgent, institutieAgent, serieProcesVerbal from lexbox.instance where cnp like '%{CNP}%' limit 15".format(CNP=CNP))
        records = cursor.fetchall()
        connection.close()
        return records
    else:
        return []

def getResultsByAgent(nume, prenume):
    if len(nume) > 3 and len(prenume) > 3:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select id, nume, prenume, telefon, serieBuletin, numarBuletin, cnp, adresaProceduralaStrada, adresaProceduralaNumar, adresaProceduralaOras, adresaProceduralaJudet, adresaProceduralaBloc, adresaProceduralaScara, adresaProceduralaApartament, adresaProceduralaApartament, adresaProceduralaCodPostal, numeAgent, prenumeAgent, institutieAgent, serieProcesVerbal from lexbox.instance where numeAgent like '%{nume}%' and prenumeAgent like '%{prenume}%' limit 15".format(nume=nume, prenume=prenume))
        records = cursor.fetchall()
        connection.close()
        return records
    else:
        return []

def getResultsDataProcesVerbal(date1, date2):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select id from lexbox.instance where dataProcesVerbal > '{date1}' and dataProcesVerbal <'{date2}'".format(date1=date1, date2=date2))
    records = cursor.fetchall()
    connection.close()
    return records

def getResultsDataInmanariiProcesVerbal(date1, date2):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select id from lexbox.instance where dataInmanariiProcesVerbal > '{date1}' and dataInmanariiProcesVerbal < 'date2'".format(date1=date1, date2=date2))
    records = cursor.fetchall()
    connection.close()
    return records

def getResultsDataSavarsireFaptaProcesVerbal(date1, date2):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select id from lexbox.instance where dataSavarsireFaptaProcesVerbal > '{date1}' and dataSavarsireFaptaProcesVerbal < '{date2}'".format(date1=date1, date2=date2))
    records = cursor.fetchall()
    connection.close()
    return records

def getFullResultsById(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select * from lexbox.instance where id={id}".format(id=id))
    records = cursor.fetchall()
    connection.close()
    return records

def setToken(template, usernameORtoken, logged):
    if not logged:
        return template.replace('$TOKEN$', "\""+ getToken(usernameORtoken)+ "\"")
    return template.replace('$TOKEN$', "\"" + usernameORtoken + "\"")
    

def getFiles(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "select plataAmendaFile,adeverintaVenit,adeverintaMedicala,alteDocumente,carteIdentitate,procesVerbalContraventie,chitantaPlata,alteDocumente2,plangere from lexbox.instance where id={id}".format(id=id))
    records = cursor.fetchall()
    connection.close()
    return records[0]


def getExtension(data):
    extension = ''
    for i in range(5):
        extension += chr(data[i])
    if extension.endswith("\r"):
        extension=extension[0:-1]
    return extension

def getFilename(index):
    if index == 0:
        return 'Plata_Amenda'
    elif index == 1:
        return 'Adeverinta_Venit'
    elif index == 2:
        return 'Adeverinta_Medicala'
    elif index == 3:
        return 'Alte_Documente'
    elif index == 4:
        return 'Carte_Identitate'
    elif index == 5:
        return 'Proces_Verbal_Contraventie'
    elif index == 6:
        return 'Chitanta_plata'
    elif index == 7:
        return 'Alte_Documente2'
    elif index == 8:
        return 'Plangere_Contraventionala'

def getNameById(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select nume,prenume from lexbox.instance where id={id}".format(id=id))
    records = cursor.fetchall()
    connection.close()
    return records[0][0]+"_"+records[0][1]

def getDownloadLink(id):
    return "/getFiles?id=" + str(id)

def checkData(data):
    for i in data:
        if i:
            return True
    return False