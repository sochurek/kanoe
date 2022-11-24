# importy
import re
from flask import Flask, render_template, request
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# list pro ukládání dat
storage = []

# definice web serveru
app = Flask(__name__, static_url_path='/static',
            static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = '43845eab2bbba1dce738c8446ad12f8fc03dd86ad88f7716'

#route pro RestAPI
@app.route('/api/check-name/<name>',methods=['GET', 'POST'])
def api(name):

    #nemá smysl když může být člověk se stejným jménem 
    # není implementovaná, byla vytvořena pro nickname

    #temp list pro všechen obsah data.csv
    temp = []

    #načtení dat z data.csv (https://docs.python.org/3/library/csv.html)
    data = open('data.csv', 'r')
    with data:
        reader = csv.reader(data, delimiter=',')
        for typek in reader:
            temp.append(typek)

    # checkne jestli je nickname uz v data.csv
    for uzivatel in temp:
        if(name == uzivatel[0]):
            return {
                'avalible' : False
                }

    return {
        'avalible' : True
    }

# route pro domovskou stránku
@app.route('/', methods=['GET', 'POST'])
def index():

    #temp list pro všechen obsah data.csv
    temp = []


    #načtení dat z data.csv (https://docs.python.org/3/library/csv.html)
    data = open('data.csv', 'r', encoding='utf-8')
    with data:
        reader = csv.reader(data, delimiter=',')
        for typek in reader:
            temp.append(typek)

    # Render stránky
    return render_template('prvni_stranka.html', ucastnici=temp), 200

#route pro check
@app.route('/check', methods=['GET', 'POST'])
def check():

    # Hodnoty
    jmeno = request.form['jmeno']
    prijmeni = request.form['prijmeni']
    trida = request.form['trida']
    je_plavec = request.form['je_plavec']
    kanoe_kamarad_jm = request.form['kanoe_kamarad_jm']
    kanoe_kamarad_pr = request.form['kanoe_kamarad_pr']

    # Kontroly
    if ((je_plavec == "1") or (je_plavec == 1)):
        je_plavec = "Ano"
    else:
        je_plavec = "Ne"

    if not re.search("^[a-zA-Z0-9áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", jmeno):
        return render_template("neprovedeno.html"), 400

    if not re.search("^[a-zA-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", prijmeni):
        return render_template("neprovedeno.html"), 400

    if (not(re.search("^[a-zA-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", kanoe_kamarad_jm)) or not(re.search("^[a-zA-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", kanoe_kamarad_pr))):
        storage.append([jmeno, prijmeni, trida, je_plavec, "Nemá", " "])

    if ((re.search("^[a-zA-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", kanoe_kamarad_jm) and (re.search("^[a-zA-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]{2,20}$", kanoe_kamarad_pr)))):
        storage.append([jmeno, prijmeni, trida, je_plavec, kanoe_kamarad_jm, kanoe_kamarad_pr])

    # Převedení storage do stringu    
    temp = ""

    for x in storage:
        temp += str(x) + ", "

    #kód pro posílání emailů je inspirován stránkou https://realpython.com/python-send-email/ a pomoc od https://stackoverflow.com/questions/17759860/python-2-smtpserverdisconnected-connection-unexpectedly-closed
    cas = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    port = 465
    password = "tajne_heslo_pro_kanoe" # opravdu velice tajné heslo
    smtp_server = "smtp.seznam.cz"
    sender_email = "kanoe@kevizb.cz"  
    receiver_email = "kanoe@kevizb.cz"  

    # vytvoření zprávy emailu
    message = MIMEMultipart("alternative")
    message["Subject"] = "Nová registrace"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # přidání html části emailu
    html = "<html><head><meta charset='utf-8'></head><body><h1>Proběhla nová registrace</h1><br><p>Hodnoty: " + str(temp) + " Čas odeslání: " + str(cas) + "</p></body></html>"
    part2 = MIMEText(html, 'html')

    # připojení k message
    message.attach(part2)

    # poslání emailu
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email,receiver_email,message.as_string())

    # Zápis do data.csv
    with open('data.csv', 'a', newline='', encoding='utf-8') as data:
        write = csv.writer(data)
        write.writerows(storage)

    # vyprázdnění storage aby nedošklo k zápisu stejného obsahu listu několikrát
    storage.clear()

    # Render stránky
    return render_template('provedeno.html'), 200

# route pro ýpis podle ročníků
@app.route('/vypis/<rocnik>', methods=['GET', 'POST'])
def vypis_rocniky(rocnik):

    #temp list pro všechen obsah data.csv
    temp = []

    #načtení dat z data.csv (https://docs.python.org/3/library/csv.html)
    data = open('data.csv', 'r', encoding='utf-8')
    with data:
        reader = csv.reader(data, delimiter=',')
        for typek in reader:
            if(typek[2] == rocnik):
                temp.append(typek)

    # Render stránky
    return render_template('vypis.html', rocnik=rocnik, ucastnici=temp), 200

# route pro registraci
@app.route('/registrace', methods=['GET', 'POST'])
def registrace():

    # Render stránky
    return render_template('registrace.html'), 200

# spuštění scriptu
if __name__ == '__main__':

    #nadefinování IP a portu pro web server
    app.run(host='0.0.0.0', port=80)
