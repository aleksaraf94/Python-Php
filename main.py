from flask import Flask, render_template, sessions, session, request,redirect,url_for
from datetime import datetime
import hashlib
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="projekat"
)

app = Flask(__name__)

app.secret_key = "nesto"  # kada se radi sa sesijama

@app.route("/")
def index():

    #admin(vidi,menja i brise sve proizvode)

    #prodavac(vidi,menja i brise svoje proizvode)

    #korisnik(vidi sve proizvode)
    if "korime" in session:
        ulogovan=1
        if session["podaci"][4]=="admin":
            mc = mydb.cursor()
            mc.execute("SELECT * FROM proizvodi")  # prolazimo kroz sve korisnike
            res = mc.fetchall()
            return render_template("index.html", proizvodi=res)
        elif session["podaci"][4]=="prodavac":
            mc = mydb.cursor()
            mc.execute("SELECT * FROM proizvodi WHERE id_osobe="+str(session["podaci"][0]))  # prolazimo kroz sve korisnike
            res = mc.fetchall()
            return render_template("index.html", proizvodi=res)
        else:
            mc = mydb.cursor()
            mc.execute("SELECT * FROM proizvodi")  # prolazimo kroz sve korisnike
            res = mc.fetchall()
            return render_template("korisnik.html", proizvodi=res)
    else:

        mc = mydb.cursor()
        mc.execute("SELECT * FROM proizvodi")  # prolazimo kroz sve korisnike
        res = mc.fetchall()
        return render_template("korisnik.html",proizvodi=res)

@app.route("/registracija")
def registracija():
    if "korime" in session:
        return render_template("index.html",odg="ulogovani ste")
    return render_template("registracija.html")

@app.route("/registruj",methods=["POST"])
def registruj():
    # provera da li je korisnik ulogovan
    ime = request.form["ime"]
    lozinka = request.form["lozinka"]
    potvrda = request.form["potvrda"]
    prezime = request.form["prezime"]
    email = request.form["email"]
    telefon = request.form["telefon"]
    status = request.form["status"]
    kasa = request.form["kasa"]
    korime = request.form["korime"]

    if korime == "":
        return render_template("registracija.html", odg="unesite korisnicko ime")

    if ime == "":
        return render_template("registracija.html", odg="unesite ime")

    if prezime=="":
        return render_template("registracija.html",odg="unesite prezime")

    if lozinka=="":
        return render_template("registracija.html",odg="unesite lozinku")

    if lozinka!=potvrda:
        return render_template("registracija.html",odg="lozinka i potvrda se ne slazu")

    if email=="":
        return render_template("registracija.html",odg="unesite email")

    if telefon=="":
        return render_template("registracija.html",odg="unesite telefon")

    if kasa=="":
        return render_template("registracija.html",odg="unesite kasu")

    mc = mydb.cursor()
    mc.execute("SELECT * FROM korisnici WHERE korime='" + korime + "'")  # prolazimo kroz sve korisnike
    res = mc.fetchall()


    if mc.rowcount == 0:

        try:
            #ovo stavljamo u try catch blok iz razloga ako se nesto desi pa ne moze doci do upisa u bazu obavestimo korisnika o tome
            password = hashlib.sha256(lozinka.encode()).hexdigest()
            mc.execute("INSERT INTO korisnici VALUES(null,'" + korime + "','" + password + "','" + email + "','" + status + "','" + telefon + "','" + ime + "','" + prezime + "',"+kasa+")")
            mydb.commit()
            return render_template("logovanje.html", odg="Uspesna registracija!")
            print(res)
        except Exception as e:
            return render_template("registracija.html", odg=str(e))



    else:
        return render_template("registracija.html", odg="korisnicko ime zauzeto")

@app.route("/logovanja")
def logovanje():
    if "korime" in session:
        return render_template("index.html",odg="ulogovani ste")
    return render_template("logovanje.html")

@app.route("/uloguj",methods=["POST"])
def uloguj():
    korime = request.form["korime"]
    lozinka = request.form["lozinka"]
    print(korime+" "+lozinka)
    password = hashlib.sha256(lozinka.encode()).hexdigest()

    mc = mydb.cursor()
    mc.execute("SELECT * FROM korisnici WHERE korime='" + korime + "' AND lozinka='"+password+"'")  # prolazimo kroz sve korisnike
    res = mc.fetchall()
    print(res)

    if mc.rowcount == 0:
        return render_template("logovanje.html", odg="korisnik ne postoji")
    else:
        session["korime"] = korime
        session["podaci"] = res[0]
        return render_template("index.html", odg="ulogovani ste")

@app.route("/logout")
def logout():
    session.pop("korime", None)
    session.pop("podaci", None)
    return render_template("index.html")

@app.route("/profil")
def profil():
    if "korime" in session:  # proveravamo sesiju
        print(session["podaci"])
        return render_template("profil.html",podaci=session["podaci"])
    else:
        return "niste ulogovani <a href='/logovanja'>Ulogujte se</a>"

@app.route("/izmenaKorisnik",methods=["POST"])
def izmenaKorisnik():
    id = request.form["id"]
    korime = request.form["korime"]
    lozinka = request.form["lozinka"]
    potvrda = request.form["potvrda"]
    email = request.form["email"]
    ime = request.form["ime"]
    prezime = request.form["prezime"]
    telefon = request.form["telefon"]

    if korime == "":
        return render_template("profil.html", odg="unesite korisnicko ime",podaci=session["podaci"])

    if ime == "":
        return render_template("profil.html", odg="unesite ime",podaci=session["podaci"])

    if prezime=="":
        return render_template("profil.html",odg="unesite prezime",podaci=session["podaci"])

    if lozinka=="":
        return render_template("profil.html",odg="unesite lozinku",podaci=session["podaci"])

    if lozinka!=potvrda:
        return render_template("profil.html",odg="lozinka i potvrda se ne slazu",podaci=session["podaci"])

    if email=="":
        return render_template("profil.html",odg="unesite email",podaci=session["podaci"])

    if telefon=="":
        return render_template("profil.html",odg="unesite telefon",podaci=session["podaci"])

    mc = mydb.cursor()
    mc.execute("SELECT * FROM korisnici WHERE korime='" + korime + "'")  # prolazimo kroz sve korisnike
    res = mc.fetchall()

    if mc.rowcount == 0:
        password = hashlib.sha256(lozinka.encode()).hexdigest()
        mc.execute("UPDATE korisnici SET korime='"+korime+"',lozinka='"+password+"',email='"+email+"',ime='"+ime+"',prezime='"+prezime+"',telefon='"+telefon+"' WHERE id="+str(id))
        mydb.commit()

        mc.execute("SELECT * FROM korisnici WHERE korime='" + korime + "' AND lozinka='" + password + "'")  # prolazimo kroz sve korisnike
        res = mc.fetchall()

        session["korime"] = korime
        session["podaci"] = res[0]

        return render_template("profil.html", odg="Podaci promenjeni",podaci=session["podaci"])
    else:
        return render_template("profil.html", odg="Korisnicko ime zauzeto",podaci=session["podaci"])

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

@app.route("/poruka",methods=["post"])
def poruka():
    naslov = request.form["naslov"]
    poruka = request.form["poruka"]
    email = request.form["email"]


    if naslov=="":
        return render_template("kontakt.html",odg="unesite naslov")

    if poruka=="":
        return render_template("kontakt.html",odg="unesite poruku")

    if email=="":
        return render_template("kontakt.html",odg="unesite email")



    mc = mydb.cursor()
    mc.execute("INSERT INTO kontakt VALUES(null,'" + naslov + "','" + poruka + "','" + email + "')")
    mydb.commit()

    return render_template("kontakt.html",odg="poruka poslata")

@app.route("/o nama")
def o_nama():
    return render_template("o nama.html")

@app.route("/administracija")
def administracija():
    if "korime" in session:  # proveravamo sesiju

        res=""
        if session["korime"]=="admin":
            mc = mydb.cursor()
            mc.execute("SELECT * FROM kontakt")  # prolazimo kroz sve korisnike
            res = mc.fetchall()


        return render_template("administracija.html",idd=session["podaci"][0],poruke=res)
    else:
        return "niste ulogovani <a href='/logovanja'>Ulogujte se!</a>"

@app.route("/dodaj",methods=["post"])
def dodaj():
    #ime	opis	cena	proizvodjac
    id_osobe = request.form["id_osobe"]
    ime = request.form["ime"]
    opis = request.form["opis"]
    cena = request.form["cena"]
    proizvodjac = request.form["proizvodjac"]

    mc = mydb.cursor()
    mc.execute("INSERT INTO proizvodi VALUES(null,'" + ime + "','" + opis + "'," + cena + ",'"+proizvodjac+"',"+id_osobe+")")
    mydb.commit()

    return render_template("administracija.html",idd=session["podaci"][0],odg="proizvod dodat")

@app.route("/obrisi",methods=["post"])
def obrisi():
    id = request.form["id"]

    mc = mydb.cursor()
    mc.execute("DELETE FROM proizvodi WHERE id="+str(id))
    mydb.commit()
    return redirect("http://127.0.0.1:5000")

@app.route("/izmeni",methods=["post"])
def izmeni():
    id = request.form["id"]
    ime = request.form["ime"]
    opis = request.form["opis"]
    cena = request.form["cena"]
    proizvodjac = request.form["proizvodjac"]

    mc = mydb.cursor()
    mc.execute("UPDATE proizvodi SET ime='"+ime+"',opis='"+opis+"',cena="+str(cena)+",proizvodjac='"+proizvodjac+"' WHERE id=" + str(id))
    mydb.commit()

    return redirect("http://127.0.0.1:5000")

@app.route("/dodajkorpa",methods=["post"])
def dodaj2():
    id_proizvoda = request.form["id"]
    id_korisnika = session["podaci"][0]

    mc = mydb.cursor()
    mc.execute("INSERT INTO korpa VALUES(null,"+str(id_proizvoda)+","+str(id_korisnika)+")")
    mydb.commit()

    return redirect("http://127.0.0.1:5000")

@app.route("/korpa")
def korpa():
    if "korime" in session:  # proveravamo sesiju

        mc = mydb.cursor()
        mc.execute("SELECT * FROM korpa WHERE id_korisnika='" + str(session["podaci"][0]) + "'")  # prolazimo kroz sve korisnike
        res = mc.fetchall()

        if mc.rowcount == 0:
            return render_template("korpa.html",proizvodi=[],odg="prazna korpa")

        #ispod moramo kreirati zagrade koje sadrze sve ideve proizvoda za prikaz (1,4,14)
        asd="("#otvaramo zagrade
        j=0#brojac je bitan posto ispred prvog broja ne ide zarez (1
        for i in res:
            if j==0:
                asd+=str(i[1])#ovde dodajemo prvi id (1
                j=5
            else:
                asd += ","+str(i[1])#ovde doadajemo sve ostale (1 => (1,4 => (1,4,14...
        asd +=")"#zatvaramo zagrade (...)


        mc = mydb.cursor()
        mc.execute("SELECT * FROM proizvodi WHERE id IN "+asd)  # prolazimo kroz sve korisnike
        res = mc.fetchall()

        return render_template("korpa.html",proizvodi=res)

    else:
        return "Niste ulogovani <a href='/logovanja'>Ulogujte se</a>"

@app.route("/izbaci",methods=["post"])
def izbaci():
    id = request.form["id"]

    mc = mydb.cursor()
    mc.execute("DELETE FROM korpa WHERE id_proizvoda=" + str(id)+" AND id_korisnika="+str(session["podaci"][0]))
    mydb.commit()

    return redirect(url_for("korpa"))

@app.route("/komentarisi",methods=["post"])
def komentarisi():
    #id_proizvoda,naslov,komentar
    id_proizvoda=request.form["id_proizvoda"]
    naslov = request.form["naslov"]
    komentar = request.form["komentar"]
    id_korisnika = session["podaci"][0]

    mc = mydb.cursor()
    mc.execute("INSERT INTO komentari VALUES(null,"+str(id_proizvoda)+",'"+naslov+"','"+komentar+"',"+str(id_korisnika)+")")
    mydb.commit()

    return redirect("http://127.0.0.1:5000")

@app.route("/jedanProizvod/<id>")
def prikazi(id):
    mc = mydb.cursor()
    mc.execute("SELECT * FROM proizvodi WHERE id=" + str(id))  # prolazimo kroz sve korisnike
    res = mc.fetchall()

    id_proizvoda=res[0][0]

    mc.execute("SELECT * FROM komentari WHERE id_proizvoda=" + str(id_proizvoda))  # prolazimo kroz sve korisnike
    res2 = mc.fetchall()

    mc = mydb.cursor()
    mc.execute("SELECT COUNT(*) FROM lajkovi WHERE id_proizvoda=" + str(id_proizvoda))  # prolazimo kroz sve korisnike
    lajkovi = mc.fetchall()

    mc = mydb.cursor()
    mc.execute("SELECT COUNT(*) FROM dislajkovi WHERE id_proizvoda=" + str(id_proizvoda))  # prolazimo kroz sve korisnike
    dislajkovi = mc.fetchall()

    return render_template("jedanProizvod.html",proizvod=res[0],komentari=res2,lajkovi=lajkovi,dislajkovi=dislajkovi)

@app.route("/lajkuj",methods=["post"])
def lajkuj():

    if not "korime" in session:
        return redirect("http://127.0.0.1:5000/logovanja")

    id_proizvoda = request.form["id_proizvoda"]
    id_korisnika = session["podaci"][0]

    mc = mydb.cursor()
    mc.execute(
        "SELECT * FROM lajkovi WHERE id_korisnika=" + str(id_korisnika) + " AND id_proizvoda="+str(id_proizvoda))  # prolazimo kroz sve korisnike
    res = mc.fetchall()

    if mc.rowcount == 0:

        mc = mydb.cursor()
        mc.execute(
            "SELECT * FROM dislajkovi WHERE id_korisnika=" + str(id_korisnika) + " AND id_proizvoda=" + str(
                id_proizvoda))  # prolazimo kroz sve korisnike
        res = mc.fetchall()

        if mc.rowcount == 0:

            mc = mydb.cursor()
            mc.execute("INSERT INTO lajkovi VALUES(null," + str(id_proizvoda) + "," + str(id_korisnika) + ")")
            mydb.commit()

    return redirect("http://127.0.0.1:5000/jedanProizvod/" + str(id_proizvoda))

@app.route("/dislajkuj", methods=["post"])
def dislajkuj():

    if not "korime" in session:
        return redirect("http://127.0.0.1:5000/logovanja")

    id_proizvoda = request.form["id_proizvoda"]
    id_korisnika = session["podaci"][0]

    mc = mydb.cursor()
    mc.execute(
            "SELECT * FROM lajkovi WHERE id_korisnika=" + str(id_korisnika) + " AND id_proizvoda=" + str(
                id_proizvoda))  # prolazimo kroz sve korisnike
    res = mc.fetchall()

    if mc.rowcount == 0:

        mc = mydb.cursor()
        mc.execute(
                "SELECT * FROM dislajkovi WHERE id_korisnika=" + str(id_korisnika) + " AND id_proizvoda=" + str(
                    id_proizvoda))  # prolazimo kroz sve korisnike
        res = mc.fetchall()

        if mc.rowcount == 0:
            mc = mydb.cursor()
            mc.execute("INSERT INTO dislajkovi VALUES(null," + str(id_proizvoda) + "," + str(id_korisnika) + ")")
            mydb.commit()




    return redirect("http://127.0.0.1:5000/jedanProizvod/"+str(id_proizvoda))





@app.route("/prodavac/<id>")
def prodavac(id):
    mc = mydb.cursor()
    mc.execute("SELECT * FROM proizvodi WHERE id_osobe=" + str(id))
    res = mc.fetchall()


    return str(res[0])




app.run()
