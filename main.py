import flask
from flask import Flask
from flaskext.mysql import MySQL
import pymysql


app = Flask(__name__, static_url_path="/")
mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "root"
app.config["MYSQL_DATABASE_DB"] = "ucionice"


@app.route("/")
def home():
    return app.send_static_file("index.html")
#-------------------------------------------------------ucionice-------------------------------------------------------------------
#Prikaz svih ucionica iz baze
@app.route("/ucionice")
def ucionice_tabela():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM ucionica")
    ucionice = cursor.fetchall()
    tip = "Ucionice"
    return flask.render_template("prikaz.tpl.html",ucionice = ucionice,tip = tip)

#Prikaz forme za dodavanje ucionice
@app.route("/ucionica/dodaj")
def forma_ucionica_dodavanje():
    return flask.render_template("ucionica.tpl.html", izmena = "false")


#Dodavanje ucionice
@app.route("/ucionica/dodavanje",methods = ["POST"])
def dodavanje_ucionice():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ucionica(naziv, kapacitet) VALUES(%(naziv)s, %(kapacitet)s)",flask.request.form)
    db.commit()
    return flask.redirect("/ucionice")


#Prikaz forme za izmenu ucionice
@app.route("/ucionica/<int:id>/izmena")
def forma_izmena_ucionice(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ucionica WHERE id = %s",(id,))
    ucionica = cursor.fetchone()
    return flask.render_template("/ucionica.tpl.html", ucionica = ucionica, izmena = "true")  

#izmena Ucionice
@app.route("/ucionica/izmeni",methods = ["POST"])
def izmena_ucionice():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE ucionica SET naziv = %(naziv)s, kapacitet =  %(kapacitet)s  WHERE id =%(id)s",flask.request.form)
    db.commit()
    return flask.redirect("/ucionice")

#Prikaz izabrane ucionice
@app.route("/ucionica/<int:id>")
def prikaz_ucionice(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ucionica WHERE id = %s",(id,))
    ucionica = cursor.fetchone()
    return flask.render_template("/ucionica.tpl.html", ucionica = ucionica, prikaz = "true")

#Brisanje izabrane ucionice
@app.route("/ucionica/<int:id>/obrisi")
def obrisi_ucionicu(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ucionica WHERE id = %s",(id,))
    db.commit()
    return flask.redirect("/ucionice")

#-----------------------------------------------------------predavaci-------------------------------------------------------------
#Prikaz svih predavaca iz baze
@app.route("/predavaci")
def predavaci_tabela():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM predavac")
    predavaci = cursor.fetchall()
    tip = "Predavaci"
    return flask.render_template("prikaz.tpl.html",predavaci = predavaci,tip = tip)

#Prikaz forme za dodavanje predavaca
@app.route("/predavac/dodaj")
def forma_predavac_dodavanje():
    return flask.render_template("predavac.tpl.html", izmena = "false")

#Dodavanje predavaca
@app.route("/predavac/dodavanje",methods = ["POST"])
def dodavanje_predavaca():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO predavac(ime, prezime, zvanje) VALUES(%(ime)s, %(prezime)s, %(zvanje)s)",flask.request.form)
    db.commit()
    return flask.redirect("/predavaci")

#Prikaz forme za izmenu predavaca
@app.route("/predavac/<int:id>/izmena")
def forma_izmena_predavaca(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM predavac WHERE id = %s",(id,))
    predavac = cursor.fetchone()
    return flask.render_template("/predavac.tpl.html", predavac = predavac, izmena = "true")  

#izmena predavaca
@app.route("/predavac/izmeni",methods = ["POST"])
def izmena_predavaca():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE predavac SET ime = %(ime)s, prezime =  %(prezime)s , zvanje = %(zvanje)s  WHERE id =%(id)s",flask.request.form)
    db.commit()
    return flask.redirect("/predavaci")

#Prikaz izabranog predavaca
@app.route("/predavac/<int:id>")
def prikaz_predavaca(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM predavac WHERE id = %s",(id,))
    predavac = cursor.fetchone()
    return flask.render_template("/predavac.tpl.html", predavac = predavac, prikaz = "true")  

#Brisanje izabranog predavaca
@app.route("/predavac/<int:id>/obrisi")
def obrisi_predavaca(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM predavac WHERE id = %s",(id,))
    db.commit()
    return flask.redirect("/predavaci")

#-------------------------------------------------------rezervacije-------------------------------------------------      
#Prikaz svih rezervacija iz baze
@app.route("/rezervacije")
def rezervacije_tabela():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM rezervacija INNER JOIN ucionica ON ucionica.id = rezervacija.ucionica_id INNER JOIN predavac ON predavac.id = rezervacija.predavac_id")
    rezervacije = cursor.fetchall()
    for r in rezervacije:
        r["ucionica"] = r["ucionica.naziv"]
        r["predavac"] = r["ime"] + " " + r["prezime"]
    return flask.render_template("prikaz.tpl.html",rezervacije = rezervacije)


#Prikaz forme za dodavanje rezervacija
@app.route("/rezervacija/dodaj")
def forma_rezervacija_dodavanje():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM ucionica")
    ucionice = cursor.fetchall()
    cursor2 = mysql.get_db().cursor()
    cursor2.execute("SELECT * FROM predavac")
    predavaci = cursor2.fetchall()
    return flask.render_template("rezervacija.tpl.html", izmena = "false",ucionice = ucionice, predavaci = predavaci)

#Dodavanje rezervacija
@app.route("/rezervacija/dodavanje",methods = ["POST"])
def dodavanje_rezervacija():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO rezervacija(naziv, pocetak, kraj, brojUcesnika, ucionica_id, predavac_id) VALUES(%(naziv)s, %(pocetak)s, %(kraj)s, %(brojUcesnika)s, %(ucionica_id)s, %(predavac_id)s)",flask.request.form)
    db.commit()
    return flask.redirect("/rezervacije")

#Prikaz forme za izmenu rezervacija
@app.route("/rezervacija/<int:id>/izmena")
def forma_izmena_rezervacija(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rezervacija INNER JOIN ucionica ON rezervacija.ucionica_id = ucionica.id INNER JOIN predavac ON rezervacija.predavac_id = predavac.id WHERE rezervacija.id = %s",(id,))
    rezervacija = cursor.fetchone()
    rezervacija["ucionica"] = rezervacija["ucionica.naziv"]
    rezervacija["predavac"] = rezervacija["ime"] + " " + rezervacija["prezime"]

    cursor2 = mysql.get_db().cursor()
    cursor2.execute("SELECT * FROM ucionica")
    ucionice = cursor2.fetchall()

    cursor3 = mysql.get_db().cursor()
    cursor3.execute("SELECT * FROM predavac")
    predavaci = cursor3.fetchall()
    return flask.render_template("/rezervacija.tpl.html", rezervacija = rezervacija, izmena = "true", ucionice = ucionice, predavaci = predavaci) 

#izmena rezervacije
@app.route("/rezervacija/izmeni",methods = ["POST"])
def izmena_rezervacije():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE rezervacija SET naziv = %(naziv)s, pocetak =  %(pocetak)s , kraj = %(kraj)s, brojUcesnika = %(brojUcesnika)s, ucionica_id = %(ucionica_id)s, predavac_id = %(predavac_id)s  WHERE id =%(id)s",flask.request.form)
    db.commit()
    return flask.redirect("/rezervacije")

#Prikaz izabrane rezervacije
@app.route("/rezervacija/<int:id>")
def prikaz_rezervacije(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rezervacija INNER JOIN ucionica ON rezervacija.ucionica_id = ucionica.id INNER JOIN predavac ON rezervacija.predavac_id = predavac.id WHERE rezervacija.id = %s",(id,) )
    rezervacija = cursor.fetchone()
    rezervacija["ucionica"] = rezervacija["ucionica.naziv"]
    rezervacija["predavac"] = rezervacija["ime"] + " " + rezervacija["prezime"]
    return flask.render_template("/rezervacija.tpl.html", rezervacija = rezervacija, prikaz = "true")      

#Brisanje izabrane rezervacije
@app.route("/rezervacija/<int:id>/obrisi")
def obrisi_rezervaciju(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM rezervacija WHERE id = %s",(id,))
    db.commit()
    return flask.redirect("/rezervacije")

if __name__ == '__main__':
    app.run
