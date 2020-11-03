import hashlib
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="projekat"
)
mc = mydb.cursor()
password = hashlib.sha256("admin".encode()).hexdigest()
mc.execute("UPDATE korisnici SET lozinka='"+password+"' WHERE korime='admin'")
mydb.commit()