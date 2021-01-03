from flask import Flask, request, Response, render_template, redirect
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from flask.helpers import send_file, send_from_directory, url_for
from classes import *
import operations
from jinja2.environment import Template
import time
import threading
from werkzeug.datastructures import Headers
import zipfile
from _io import StringIO
import io

acceptedFormats = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
acceptedFormatsAmenda = ['pdf','jpg']

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

app = Flask(__name__, static_url_path='/static/')

@app.route('/Plangere', methods=['GET','POST'])
def api_record():
    if request.method == 'POST':
        try:
            getInstance(request).save()
        except Exception as e:
            print(e)
            if e.args[0] == "Articolul de lege nu exista!":
                return render_template("FailLaw.html")
            return render_template("Fail.html")
        return render_template("success.html")
    else:
        return getInstitutions()


@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.form['username'] != "" and request.form['password'] != "":
            if operations.login(request.form['username'], request.form['password']):
                template = env.get_template('Dashboard.html')

                connection = operations.get_connection()
                cursor = connection.cursor()
                cursor.execute("select id,nume,prenume,adresaProceduralaJudet,adresaProceduralaOras,cnp from lexbox.instance order by instance.dataProcesVerbal desc limit 15")
                records = cursor.fetchall()
                connection.close()

                results = []
                for i in records:
                    results.append(Record(i[1], i[2], i[3], i[4], i[5], operations.getDownloadLink(i[0])))
                template.records = results

                return operations.setToken(template.render(records=results), request.form['username'],False)
            return render_template("loginFailed.html")
        else:
            return render_template("login.html")


@app.route('/search', methods=['GET'])
def search():
    if operations.checkToken(request.args.get('token')):
        template = env.get_template('Dashboard.html')

        connection = operations.get_connection()
        cursor = connection.cursor()
        cursor.execute("select id,nume, prenume, adresaProceduralaJudet, adresaProceduralaOras, cnp from lexbox.instance where '{query}' like {criteria} limit 15".format(
            criteria=request.args.get('criteria'),
            query=request.args.get('keyword')))
        records = cursor.fetchall()
        connection.close()

        results = []
        
        for i in records:
            results.append(Record(i[1], i[2], i[3], i[4], i[5], operations.getDownloadLink(i[0])))
        template.records = results
        return operations.setToken(template.render(records=results), request.args.get('token'),True)
    else:
        return render_template("loginFailed.html")




@app.route('/getFiles', methods=['GET'])
def getFiles():
    data = operations.getFiles(request.args.get('id'))
    if operations.checkData(data):
        files = []
        mf = io.BytesIO()
        zip_file = zipfile.ZipFile(mf, "a", zipfile.ZIP_DEFLATED, True)
        for i in range(len(data)):
            try:
                if data[i]:
                    filename = operations.getFilename(i)
                    extension = operations.getExtension(data[i]).lower()
                    if extension == '%pdf-': # pdf
                        filename+='.pdf'
                    elif extension == 'ÿøÿà\x00': # jpg
                        filename += '.jpg'
                    elif extension == '\x89png': # png
                        filename += '.png'
                    elif extension == 'ðï\x11à¡':  # doc
                        filename += '.doc'
                    elif extension == 'pk\x03\x04\x14':  # docx
                        filename += '.docx'
                    zip_file.writestr(filename, data[i])
            except Exception as e:
                print(e)
        zip_file.close()
        header = Headers()
        header.add('Content-Disposition', 'attachment',filename=operations.getNameById(request.args.get('id'))+".zip")
        return Response(mf.getvalue(), mimetype='image/zip', headers=header)
    else:
        return render_template("NotFound.html")


@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == "GET":
        if operations.logoutByToken(request.args.get('token')) != 2:
            return redirect(url_for('login'))
        else:
            return render_template('ServerError.html')
    else:
        return redirect(url_for('login'))


def tokenCleaner():
    while True:
        time.sleep(5)
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM lexbox.token WHERE expire < (curdate() - 1)")
        connection.commit()
        connection.close()
       
        


if __name__ == '__main__':
    t1 = threading.Thread(target=tokenCleaner)
    t1.start()
    app.run(debug=True)
