import sqlite3
from flask import render_template, request
from sqlite3 import Error


con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()

class Books:
    
    def __init__(self, bookID, bookName, author, yearPublished, bookType):
        self.bookID = bookID
        self.bookName = bookName
        self.author = author
        self.yearPublished = yearPublished
        self.bookType = bookType
    
    def addBook(self):
        msg=""
        if request.method=='POST':
            self.bookName = request.form.get('bookName')
            self.author = request.form.get('author')
            self.yearPublished = request.form.get('yearPublished')
            self.bookType = request.form.get('bookType')
            cur.execute(f'''INSERT INTO Books VALUES(not null, "{self.bookName}", "{self.author}", {int(self.yearPublished )}, {int(self.bookType)})''')
            con.commit()
            msg="The book is added!"
        return render_template("/books/addBook.html", msg=msg)

    def removeBook(self):
        msg=""
        if request.method=='POST':
            self.bookID = request.form.get('bookID')
            cur.execute(f'''select count(bookID) from Books where bookID={self.bookID}''')
            numberOfID=cur.fetchone()
            if numberOfID[0]==0:
                msg="Please choose book ID which is not loaned and in range"
                return render_template("/books/removeBook.html", msg=msg)
            else:
                SQL2=f'''delete from Books where bookID={int(self.bookID)}'''
                cur.execute(SQL2)
                con.commit()
                msg="The book is removed!"
            return render_template("/books/removeBook.html", msg=msg)   
        return render_template("/books/removeBook.html", msg=msg)

    def displayBooks(self):
        cur.execute("select distinct * from Books")
        myBooks=cur.fetchall()
        return render_template("/books/books.html", myBooks=myBooks)
    
    def FindBook(self):
        msg=""
        if request.method=='POST':
            self.bookName = request.form.get('bookName')
            cur.execute(f'''select * from books where bookName like "%{self.bookName}%"''')
            filteredBooks=cur.fetchall()
            con.commit()
            if len(filteredBooks)>0:
                msg="The book is found!"
                return render_template("/books/findBook.html", msg=msg, filteredBooks=filteredBooks)
            else:
                msg='The Book is not in the list'
        return render_template("/books/findBook.html",msg=msg)
        

    
        

    

    





    
