from operations import get_connection
from docx import Document
from django.core.files.storage import FileSystemStorage
import io
from io import BytesIO, StringIO


def getLaw(articol, aliniat, litera):
    litera = litera.lower()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select textlege from lexbox.lege where articol='{articol}' and aliniat='{aliniat}' and litera='{litera}'".format(articol=articol, aliniat=aliniat, litera=litera))
    records = cursor.fetchall()
    connection.close()
    try:
        return records[0][0]
    except:
        return ""

class Instance:
    
    def __init__(self, nume, prenume, telefon, serieBuletin, numarBuletin, cnp, adresaProceduralaStrada, adresaProceduralaNumar, adresaProceduralaOras, adresaProceduralaJudet, adresaProceduralaBloc, adresaProceduralaScara, adresaProceduralaApartament, adresaProceduralaCodPostal, numeAgent, prenumeAgent, calitateAgent, institutieAgent, locSavarsireContraventie, posesieProcesVerbalContraventie, serieProcesVerbal, numarProcesVerbal, dataProcesVerbal, posesieProcesVerbal, dataInmanariiProcesVerbal, dataSavarsireFaptaProcesVerbal, plataAmenda, plataAmendaFile, solicitareInstanta, prezentareSituatieProcesVerbal, prezentareSituatieDPDVPropriu, articolFapta, aliniatFapta, normaLegalaFapta, articolSanctiune, aliniatSanctiune, normaLegalaSanctiune, martori, adeverintaVenit, adeverintaMedicala, alteDocumente, carteIdentitate, procesVerbalContraventie, chitantaPlata, alteDocumente2, prezentaJudecata,asistareJudecata):
        self.nume = nume                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        self.prenume = prenume
        self.telefon = telefon
        self.serieBuletin = serieBuletin
        self.numarBuletin = numarBuletin
        self.cnp = cnp
        self.adresaProceduralaStrada = adresaProceduralaStrada
        self.adresaProceduralaNumar = adresaProceduralaNumar                                                                                                                                                                                                                                                                    
        self.adresaProceduralaOras = adresaProceduralaOras                                                                                                                                                                                                                                                                                                                                                                                                                                
        self.adresaProceduralaJudet = adresaProceduralaJudet
        self.adresaProceduralaBloc = adresaProceduralaBloc
        self.adresaProceduralaScara = adresaProceduralaScara
        self.adresaProceduralaApartament = adresaProceduralaApartament
        self.adresaProceduralaCodPostal = adresaProceduralaCodPostal
        self.numeAgent = numeAgent
        self.prenumeAgent = numeAgent
        self.calitateAgent = calitateAgent
        self.institutieAgent = institutieAgent
        self.locSavarsireContraventie = locSavarsireContraventie
        self.posesieProcesVerbalContraventie = posesieProcesVerbalContraventie
        self.serieProcesVerbal = serieProcesVerbal
        self.numarProcesVerbal = numarProcesVerbal
        self.dataProcesVerbal = dataProcesVerbal
        self.posesieProcesVerbal = posesieProcesVerbal
        self.dataInmanariiProcesVerbal = dataInmanariiProcesVerbal
        self.dataSavarsireFaptaProcesVerbal = dataSavarsireFaptaProcesVerbal
        self.plataAmenda = plataAmenda
        self.plataAmendaFile = plataAmendaFile
        self.solicitareInstanta = solicitareInstanta
        self.prezentareSituatieProcesVerbal = prezentareSituatieProcesVerbal
        self.prezentareSituatieDPDVPropriu = prezentareSituatieDPDVPropriu
        self.articolFapta = articolFapta
        self.aliniatFapta = aliniatFapta
        self.normaLegalaFapta = normaLegalaFapta
        self.articolSanctiune = articolSanctiune
        self.aliniatSanctiune = aliniatSanctiune
        self.normaLegalaSanctiune = normaLegalaSanctiune
        self.martori = martori
        self.adeverintaVenit = adeverintaVenit
        self.adeverintaMedicala=adeverintaMedicala
        self.alteDocumente = alteDocumente
        self.carteIdentitate = carteIdentitate
        self.procesVerbalContraventie = procesVerbalContraventie
        self.chitantaPlata = chitantaPlata
        self.alteDocumente2 = alteDocumente2
        self.prezentaJudecata = prezentaJudecata
        self.asistareJudecata = asistareJudecata
        self.plangere = None

    def getCompletedForm(self,uploadedFiles):
        WordsInPlace = {}

        if self.asistareJudecata.upper()=="DA":
            WordsInPlace["$if$"] = """cu domiciliul procedural ales la sediul avocatului MARCU MIHAELA LUMINIŢA situat în Timişoara, strada Take Ionescu nr. 46B sc. C ap. 06, jud. Timiş, CP: 300124, avocatmihaela@gmail.com, telefon: 0721885855"""
        else:
            WordsInPlace["$if$"] = "."

        WordsInPlace["$A$"] = self.nume + " " + self.prenume
        WordsInPlace["$B$"] = self.adresaProceduralaOras
        WordsInPlace["$C$"] = self.adresaProceduralaStrada
        WordsInPlace["$D$"] = self.adresaProceduralaBloc
        WordsInPlace["$E$"] = self.adresaProceduralaScara
        WordsInPlace["$F$"] = self.adresaProceduralaApartament
        WordsInPlace["$G$"] = self.adresaProceduralaJudet
        WordsInPlace["$H$"] = self.serieBuletin + " "
        WordsInPlace["$I$"] = self.numarBuletin
        WordsInPlace["$J$"] = self.cnp
        institutie = getInstitution(self.institutieAgent)
        WordsInPlace["$K$"] = institutie.nume
        WordsInPlace["$L$"] = "UM 0805 " + institutie.localitate
        WordsInPlace["$M$"] = institutie.localitate
        WordsInPlace["$N$"] = institutie.adresa
        WordsInPlace["$O$"] = institutie.localitate
        WordsInPlace["$P$"] = institutie.cod_postal
        WordsInPlace["$Q$"] = institutie.telefon
        WordsInPlace["$S$"] = institutie.fax
        WordsInPlace["$T$"] = institutie.email
        WordsInPlace["$U$"] = institutie.judet
        WordsInPlace["$V$"] = self.serieProcesVerbal 
        WordsInPlace["$W$"] = self.numarProcesVerbal
        WordsInPlace["$X$"] = self.dataProcesVerbal
        WordsInPlace["$Y$"] = self.dataInmanariiProcesVerbal
        WordsInPlace["$Z$"] = self.plataAmenda

        # if self.plataAmenda.upper() == "DA":
        #     WordsInPlace["$Z$"] = "am fost de acord"
        # else:
        #     WordsInPlace["$Z$"] = "nu am fost de acord"

        WordsInPlace["$AA$"] = self.nume + " " + self.prenume 
        WordsInPlace["$AB$"] = self.serieProcesVerbal
        WordsInPlace["$AC$"] = self.numarProcesVerbal

        WordsInPlace["$AD$"] = self.prezentareSituatieDPDVPropriu
        # WordsInPlace["$AD$"] = self.articolSanctiune

        WordsInPlace["$AE$"] = "nu am fost de acord"
        # WordsInPlace["$AE$"] = self.prezentareSituatieProcesVerbal

        WordsInPlace["$AF$"] = self.plataAmenda

        WordsInPlace["$AG$"] = self.articolSanctiune
        WordsInPlace["$AH$"] = self.aliniatSanctiune
        WordsInPlace["$AI$"] = self.normaLegalaSanctiune
        law = getLaw(self.articolSanctiune, self.aliniatSanctiune,
                     self.normaLegalaSanctiune)
        if law == "":
            raise Exception("Articolul de lege nu exista!")
        
        WordsInPlace["$R$"] = law

        if self.martori == "":
            self.martori = "Nu are martori"

        WordsInPlace["$AJ$"] = self.martori
        WordsInPlace["$FILES$"] = uploadedFiles

        
        def inParagraph(paragraph):
            for i in WordsInPlace:
                if i in paragraph.text:
                    return True
            return False


        def inInline(inline):
            for i in WordsInPlace:
                if i in inline.text:
                    return True
            return False

        doc = Document("resources/test.docx")
        for paragraph in doc.paragraphs:
            if inParagraph(paragraph):
                inline = paragraph.runs
                for i in range(len(inline)):
                    if inInline(inline[i]):
                        try:
                            text = inline[i].text.replace(inline[i].text, WordsInPlace[inline[i].text.rstrip()])
                            inline[i].text = text
                        except Exception as e:
                            for key in WordsInPlace:
                                text = inline[i].text.replace(key, WordsInPlace[key])
                                inline[i].text = text
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        return file_stream.read()
    def save(self):
            uploadedFiles = ""
            insertQuery = """INSERT INTO instance(
            nume,
            prenume,
            telefon,
            serieBuletin,
            numarBuletin,
            cnp,
            adresaProceduralaStrada,
            adresaProceduralaNumar,
            adresaProceduralaOras,
            adresaProceduralaJudet,
            adresaProceduralaBloc,
            adresaProceduralaScara,
            adresaProceduralaApartament,
            adresaProceduralaCodPostal,
            numeAgent,
            prenumeAgent,
            calitateAgent,
            institutieAgent,
            locSavarsireContraventie,
            posesieProcesVerbalContraventie,
            serieProcesVerbal,
            numarProcesVerbal,
            dataProcesVerbal,
            posesieProcesVerbal,
            dataInmanariiProcesVerbal,
            dataSavarsireFaptaProcesVerbal,
            plataAmenda,
            plataAmendaFile,
            solicitareInstanta,
            prezentareSituatieProcesVerbal,
            prezentareSituatieDPDVPropriu,
            articolFapta,
            aliniatFapta,
            normaLegalaFapta,
            articolSanctiune,
            aliniatSanctiune,
            normaLegalaSanctiune,
            martori,
            adeverintaVenit,
            adeverintaMedicala,
            alteDocumente,
            carteIdentitate,
            procesVerbalContraventie,
            chitantaPlata,
            alteDocumente2,
            prezentaJudecata,
            asistareJudecata,
            plangere
            ) VALUES (""" + "%s," * 48
            insertQuery = insertQuery[:-1] + ")"
            if self.plataAmendaFile == b'':
                self.plataAmendaFile = None
            else:
                uploadedFiles += "- Poza plata amenda\n"
            if self.adeverintaVenit == b'':
                self.adeverintaVenit = None
            else:
                uploadedFiles += "- Adeverinta Venit/Pensie\n"
            if self.adeverintaMedicala == b'':
                self.adeverintaMedicala = None
            else:
                uploadedFiles += "- Adeverinta Medicala\n"
            if self.alteDocumente == b'':
                self.alteDocumente = None
            else:
                uploadedFiles += "- Alte Documente\n"
            if self.carteIdentitate == b'':
                self.carteIdentitate = None
            else:
                uploadedFiles += "- Carte de identitate\n"
            if self.procesVerbalContraventie == b'':
                self.procesVerbalContraventie = None
            else:
                uploadedFiles += "- Proces verbal de contraventie\n"
            if self.chitantaPlata == b'':
                self.chitantaPlata = None
            else:
                uploadedFiles += "- Chitanta plata\n"
            if self.alteDocumente2 == b'':
                self.alteDocumente2 = None
            else:
                uploadedFiles += "- Alte Documente2"
                
            insertBlobTouple = (self.nume,
                                self.prenume,
                                self.telefon,
                                self.serieBuletin,
                                self.numarBuletin,
                                self.cnp,
                                self.adresaProceduralaStrada,
                                self.adresaProceduralaNumar,
                                self.adresaProceduralaOras,
                                self.adresaProceduralaJudet,
                                self.adresaProceduralaBloc,
                                self.adresaProceduralaScara,
                                self.adresaProceduralaApartament,
                                self.adresaProceduralaCodPostal,
                                self.numeAgent,
                                self.prenumeAgent,
                                self.calitateAgent,
                                self.institutieAgent,
                                self.locSavarsireContraventie,
                                self.posesieProcesVerbalContraventie,
                                self.serieProcesVerbal,
                                self.numarProcesVerbal,
                                self.dataProcesVerbal,
                                self.posesieProcesVerbal,
                                self.dataInmanariiProcesVerbal,
                                self.dataSavarsireFaptaProcesVerbal,
                                self.plataAmenda,
                                self.plataAmendaFile,
                                self.solicitareInstanta,
                                self.prezentareSituatieProcesVerbal,
                                self.prezentareSituatieDPDVPropriu,
                                self.articolFapta,
                                self.aliniatFapta,
                                self.normaLegalaFapta,
                                self.articolSanctiune,
                                self.aliniatSanctiune,
                                self.normaLegalaSanctiune,
                                self.martori,
                                self.adeverintaVenit,
                                self.adeverintaMedicala,
                                self.alteDocumente,
                                self.carteIdentitate,
                                self.procesVerbalContraventie,
                                self.chitantaPlata,
                                self.alteDocumente2,
                                self.prezentaJudecata,
                                self.asistareJudecata,
                                self.getCompletedForm(uploadedFiles)
                                )
            con = get_connection()
            cursor = con.cursor()
            result = cursor.execute(insertQuery, insertBlobTouple)
            con.commit()
            con.close()


def getInstance(request):
    # Client
    nume = request.form["q17_nume"]
    prenume = request.form["q25_prenume25"]
    telefon = request.form["q20_telefon[full]"]
    serieBuletin = request.form["q33_seriaa"]
    numarBuletin = request.form["q34_numarul"]
    cnp = request.form["q34_CNP"]
    adresaProceduralaStrada = request.form["q21_adresaProcedurala[addr_line1]"]
    adresaProceduralaNumar = request.form["q21_adresaProcedurala[addr_line2]"]
    adresaProceduralaOras = request.form["q21_adresaProcedurala[city]"]
    adresaProceduralaJudet = request.form["q21_adresaProcedurala[state]"]
    adresaProceduralaBloc = request.form["q21_adresaProcedurala[bloc]"]
    adresaProceduralaScara = request.form["q21_adresaProcedurala[scara]"]
    adresaProceduralaApartament = request.form["q21_adresaProcedurala[apartament]"]
    adresaProceduralaCodPostal = request.form["q21_adresaProcedurala[postal]"]

    # politist
    numeAgent = request.form["q24_nume24"]
    prenumeAgent = request.form["q18_prenume"]
    calitateAgent = request.form["q26_calitate"]
    institutieAgent = request.form["q73_institutie73"]

    # contraventie
    locSavarsireContraventie = request.form["q28_loculSavarsirii"]
    posesieProcesVerbalContraventie = request.form["q30_suntetiIn"]
    serieProcesVerbal = request.form["q33_seria"]
    numarProcesVerbal = request.form["q34_numarul"]
    dataProcesVerbal = request.form["data1"]
    posesieProcesVerbal = request.form["q39_cumAti"]
    dataInmanariiProcesVerbal = request.form["data2"]
    dataSavarsireFaptaProcesVerbal = request.form["data3"]
    plataAmenda = request.form["q42_atiPlatit"]
    plataAmendaFile = request.files["q43_dacaAti43[]"].read()

    # prezentare contraventie
    solicitareInstanta = request.form["q44_careDintre"]
    prezentareSituatieProcesVerbal = request.form["q45_vaRugam"]
    prezentareSituatieDPDVPropriu = request.form["q46_vaRugam46"]
    articolFapta = request.form["q49_articolul"]
    aliniatFapta = request.form["q50_aliniatul"]
    normaLegalaFapta = request.form["q51_normaLegala51"]
    articolSanctiune = request.form["q54_articolul54"]
    aliniatSanctiune = request.form["q55_aliniatul55"]
    normaLegalaSanctiune = request.form["q56_normaLegala56"]
    martori = request.form["q57_avetiMartori"]
    prezentaJudecata = request.form["q70_doritiSa"]
    asistareJudecata = request.form["q71_doritiSa71"]
    termeniConditii = request.form["q72_mentionezCa"]
    adeverintaVenit = request.files["q60_adeverintaDe[]"].read()
    adeverintaMedicala = request.files["q61_adeverintaMedicala[]"].read()
    alteDocumente = request.files["q62_alteDocumente[]"].read()
    carteIdentitate = request.files["q65_carteDe[]"].read()
    procesVerbalContraventie = request.files["q66_procesVerbal[]"].read()
    chitantaPlata = request.files["q67_chitantaPlata[]"].read()
    alteDocumente2 = request.files["q68_oriceAlt68[]"].read()

    instance = Instance(
        nume,
        prenume,
        telefon,
        serieBuletin,
        numarBuletin,
        cnp,
        adresaProceduralaStrada,
        adresaProceduralaNumar,
        adresaProceduralaOras,
        adresaProceduralaJudet,
        adresaProceduralaBloc,
        adresaProceduralaScara,
        adresaProceduralaApartament,
        adresaProceduralaCodPostal,
        numeAgent,
        prenumeAgent,
        calitateAgent,
        institutieAgent,
        locSavarsireContraventie,
        posesieProcesVerbalContraventie,
        serieProcesVerbal,
        numarProcesVerbal,
        dataProcesVerbal,
        posesieProcesVerbal,
        dataInmanariiProcesVerbal,
        dataSavarsireFaptaProcesVerbal,
        plataAmenda,
        plataAmendaFile,
        solicitareInstanta,
        prezentareSituatieProcesVerbal,
        prezentareSituatieDPDVPropriu,
        articolFapta,
        aliniatFapta,
        normaLegalaFapta,
        articolSanctiune,
        aliniatSanctiune,
        normaLegalaSanctiune,
        martori,
        adeverintaVenit,
        adeverintaMedicala,
        alteDocumente,
        carteIdentitate,
        procesVerbalContraventie,
        chitantaPlata,
        alteDocumente2,
        prezentaJudecata,
        asistareJudecata
    )
    return instance


class Institutie:
    
    def __init__(self, id, nume, localitate, judet,adresa,cod_postal,telefon,fax,email):
        self.id = id
        self.nume = nume
        self.localitate = localitate
        self.judet = judet
        self.adresa = adresa
        self.cod_postal = cod_postal
        self.telefon = telefon
        self.fax = fax
        self.email = email
        
        
    
    def __repr__(self):
        return self.judet +" - "+ self.nume
    
def sort(arr):
    sorted = False
    size = len(arr)
    while not sorted:
        sorted = True
        for i in range(0, size-1):
            if arr[i].judet > arr[i + 1].judet:
                arr[i],arr[i+1] = arr[i+1],arr[i]
                sorted = False
            elif arr[i].judet == arr[i + 1].judet:
                if arr[i].localitate > arr[i + 1].localitate:
                    arr[i],arr[i+1] = arr[i+1],arr[i]
                    sorted = False
    return arr

def getInstitutions():
    

    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM lexbox.institutie")
    records = cursor.fetchall()
    con.close()

    toReplace = ""
    institutions = []

    for row in records:
        institutions.append(Institutie(row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7],row[8]))
    institutions = sort(institutions)


    for i in institutions:
        toReplace += "<option value = \"{id}\" > {name} </option>".format(name=i.__repr__(), id=i.id) + " \n "

    res = ""
    HTMLresult = open("templates/Plangere.html", "r",encoding="utf-8")
    for line in HTMLresult:
        line = line.replace("              $$$A$$$", toReplace)
        res+=line
    HTMLresult.close()

    
    return res
    
def getInstitution(id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM lexbox.institutie where id={id}".format(id=str(id)))
    records = cursor.fetchall()
    con.close()
    return Institutie(records[0][0], records[0][1], records[0][2], records[0][3], records[0][4], records[0][5], records[0][6], records[0][7], records[0][8])

class Record:
    def __init__(self, nume, prenume, judet, oras, cnp, download):
        self.nume = nume
        self.prenume = prenume
        self.judet = judet
        self.oras = oras
        self.cnp = cnp
        self.download = download
    
