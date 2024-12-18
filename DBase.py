import sqlite3
from PIL import Image
import io

class DB():
    def __init__(self):
        self.con = sqlite3.connect('Dbase.db')
        self.cur = self.con.cursor()

    def createTableUsers(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Users (id_user INTEGER PRIMARY KEY autoincrement, login TEXT, password TEXT, access_status INTEGER)")
        self.con.commit()

    def getAllUsers(self):
        users = self.cur.execute("SELECT * FROM Users").fetchall()
        return users

    def addUser(self,login,password,status=0):
        trigger=True
        users=DB().getAllUsers()
        for i in users:
            if login==i[1]:
                trigger=False
                return 0
        if trigger:
            self.cur.execute("INSERT INTO Users (login,password,access_status) VALUES (?,?,?)",(login,password,status))
            self.con.commit()
            return 1

    def getUserID(self, id_user):
        user = self.cur.execute("SELECT * FROM Users WHERE id_user = ?", (id_user,)).fetchone()
        return user

    def getUserByLogin(self,login):
        user = self.cur.execute("SELECT * FROM Users WHERE login = ?", (login,)).fetchone()
        return user

    def getUser(self, login,password):
        user=self.cur.execute("SELECT * FROM Users WHERE login=? and password=?", (login,password)).fetchone()
        return user


    #Группа к которой будут относиться продукты
    def createTableTypes(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Types (id_type INTEGER PRIMARY KEY autoincrement, name TEXT)")
        self.con.commit()

    def getAllTypes(self):
        types = self.cur.execute("SELECT * FROM Types").fetchall()
        return types

    def addType(self,name):
        trigger = True
        types = DB().getAllTypes()
        for i in types:
            if name == i[1]:
                trigger = False
                return 0
        if trigger:
            self.cur.execute("INSERT INTO Types (name) VALUES (?)", (name,))
            self.con.commit()
            return 1

    def getTypeIdByName(self,name):
        type = self.cur.execute("SELECT id_type FROM Types WHERE name=?", (name,)).fetchone()
        if type==None:
            return False
        return type[0]





    def createTableProducts(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Products (id_product INTEGER PRIMARY KEY autoincrement, id_type INTEGER, name TEXT, about TEXT, price FLOAT, picture BLOB)")
        self.con.commit()

    def addProduct(self, type, name, about, price, picture):
        id_type = DB().getTypeIdByName(type)
        if id_type != False:
            self.cur.execute("INSERT INTO Products (id_type, name, about, price, picture) VALUES (?, ?, ?, ?, ?)",(id_type, name, about, price, sqlite3.Binary(picture)))
            self.con.commit()
            return 1
        else:
            return 0

    def changeProduct(self,id_product, new_price):
        self.cur.execute("UPDATE Products SET price=? WHERE id_product=?", (new_price,id_product))
        self.con.commit()

    def getAllProducts(self):
        products = self.cur.execute("SELECT * FROM Products").fetchall()
        return products




    def createTableReviews(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Reviews (id_review INTEGER PRIMARY KEY autoincrement, id_user INTEGER, text TEXT)")
        self.con.commit()

    def addReview(self, id_user, text):
        self.cur.execute("INSERT INTO Reviews (id_user, text) VALUES (?, ?)",(id_user, text))
        self.con.commit()

    def deleteReview(self,id_review):
        self.cur.execute("DELETE FROM Reviews WHERE id_review=?",(id_review,))
        self.con.commit()

    def getAllReviews(self):
        reviews = self.cur.execute("SELECT * FROM Reviews").fetchall()
        return reviews




    def createTableCarts(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Carts (id_tracking INTEGER PRIMARY KEY autoincrement, id_user TEXT, product TEXT)")
        self.con.commit()

    def addProductToCart(self,id_user,product):
        self.cur.execute("INSERT INTO Carts (id_user, product) VALUES (?,?)", (id_user,product))
        self.con.commit()

    def deleteFromCart(self,id_tracking, id_user):
        self.cur.execute("DELETE FROM Carts WHERE id_tracking=? and id_user=?", (id_tracking,id_user))
        self.con.commit()

    def deleteUsersCart(self, id_user):
        self.cur.execute("DELETE FROM Carts WHERE id_user=?", (id_user,))
        self.con.commit()

if __name__ == "__main__":
    DB().createTableReviews()
    DB().createTableCarts()
    DB().createTableTypes()
    DB().createTableUsers()
    DB().createTableProducts()