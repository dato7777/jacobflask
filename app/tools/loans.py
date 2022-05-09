import sqlite3
from flask import render_template, request
from sqlite3 import Error
from datetime import datetime, date

con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()
# import tools.books as b
loanedBooks=[]
lateBooks=[]

class Loans:
    
    def __init__(self, customerID, bookID, loanDate, returnDate):
        
        self.customerID = customerID
        self.bookID = bookID
        self.loanDate = loanDate
        self.returnDate = returnDate

    def addLoan(self):
        res=" "
        if request.method=='POST':
            self.customerID = request.form.get('customerID')
            self.bookID = request.form.get('bookID')
            self.loanDate = request.form.get('loanDate')
            SQL=f'''select Loans.bookID, returnDate from LoanedBooksList inner join Loans on Loans.bookID=LoanedBooksList.bookID where LoanedBooksList.bookID={self.bookID}'''
            cur.execute(SQL)
            loanedBook=cur.fetchall()
            if len(loanedBook)==0:
                cur.execute(f'''select count(bookID) from Books where bookID={self.bookID}''')
                numberOfID=cur.fetchone()
                cur.execute(f'''select count(customerID) from Customers where customerID={self.customerID}''')
                custCheck=cur.fetchone()
                if numberOfID[0]==0 or custCheck[0]==0:
                    res="Please choose an existing book or existing customer"
                    return render_template("/loans/addLoan.html", res=res)
                else:
                    cur.execute(f'''INSERT INTO Loans VALUES(NOT NULL, {int(self.customerID)}, {int(self.bookID)}, "{self.loanDate}", "{" "}")''')
                    cur.execute(f'''insert into LoanedBooksList select * from Books where bookID={self.bookID} ''')
                    cur.execute(f'''delete from Books where bookID={self.bookID}''')
                    con.commit()
                    res="You've successfully loaned a book! "
                    return render_template("/loans/addLoan.html", res=res)
            else:
                cur.execute(SQL)
                loanedBook=cur.fetchone()
                for row in loanedBook:
                    if loanedBook[0]==int(self.bookID) and loanedBook[1]==" ":
                        res="book is already loaned, choose another"
                    else:
                        cur.execute(f'''INSERT INTO Loans VALUES(NOT NULL, {int(self.customerID)}, {int(self.bookID)}, "{self.loanDate}", "{" "}")''')
                        cur.execute(f'''insert into LoanedBooksList select * from Books where bookID={self.bookID} ''')
                        cur.execute(f'''delete from Books where bookID={self.bookID}''')
                        con.commit()
                        res="You've successfully loaned a book!"
                        return render_template("/loans/addLoan.html", res=res)
                return render_template("/loans/addLoan.html",res=res)
        return render_template("/loans/addLoan.html")

    def loansDisplay(self):
        cur.execute("select * from Loans")
        myLoans=cur.fetchall()
        return render_template("/loans/loans.html", myLoans=myLoans)

    def returnLoan(self):
        msg=""
        if request.method=='POST':
            self.loanID = request.form.get('loanID')
            self.customerID = request.form.get('customerID')
            self.bookID = request.form.get('bookID')
            self.returnDate = request.form.get('returnDate')
            cur.execute("select count(loanID) from Loans")
            numberOfID=cur.fetchone()
            if int(self.loanID)>numberOfID[0]:
                msg="Please choose loan ID within range"
            else:
                SQL=f'''select loanID, returnDate, bookID from Loans where loanID={int(self.loanID)}'''
                cur.execute(SQL)
                ignorePastLoans=cur.fetchone()
                # for row in ignorePastLoans:
                if ignorePastLoans[0]==int(self.loanID) and ignorePastLoans[1]==" " and ignorePastLoans[2]==int(self.bookID):
                    cur.execute(f'''update Loans SET returnDate="{self.returnDate}" where bookID={int(self.bookID)} and customerID={int(self.customerID)} and loanID={int(self.loanID)}''')
                    # cur.execute(f'''insert OR IGNORE INTO Books select * from LoanedBooksList where bookID={self.bookID}''')
                    # cur.execute(f'''delete from LoanedBooksList where bookID={int(self.bookID)}''')
                    con.commit()
                    SQL2=f'''select loanDate, returnDate from Loans where loanID={self.loanID}'''
                    cur.execute(SQL2)
                    compar=cur.fetchone()
                    if compar[0]>compar[1]:
                        cur.execute(f'''update Loans SET returnDate="{" "}" where loanID={self.loanID}''')
                        msg="enter valid return date"
                        con.commit()
                        return render_template("/loans/returnBook.html", msg=msg)
                    else:
                        cur.execute(f'''update Loans SET returnDate="{self.returnDate}" where bookID={int(self.bookID)} and customerID={int(self.customerID)} and loanID={int(self.loanID)}''')
                        cur.execute(f'''insert OR IGNORE INTO Books select * from LoanedBooksList where bookID={self.bookID}''')
                        cur.execute(f'''delete from LoanedBooksList where bookID={int(self.bookID)}''')
                        con.commit()
                        msg="You've returned a book. Loan table is updated!"
                    return render_template("/loans/returnBook.html", msg=msg)
                else:
                    msg="Please choose an active loan."
                    return render_template("/loans/returnBook.html", msg=msg)
            return render_template("/loans/returnBook.html", msg=msg)
        return render_template("/loans/returnBook.html")

    def lateLoans(self):
        cur.execute("select Books.bookType, loanDate, returnDate, loanID from Books inner join Loans on Loans.bookID=Books.bookID")
        allTypes=cur.fetchall()
        for bType in allTypes:
            if bType[0]==1:
                date_format = "%Y-%m-%d"
                a = datetime.strptime(bType[1], date_format)
                b = datetime.strptime(bType[2], date_format)
                delta = b-a
                myDif=delta.days
                if myDif>10:
                    overDays1=myDif-10
                    SQL=f'''select distinct Customers.customerName, Customers.customerAge, Books.bookName, Books.author, bookType, Loans.loanDate, Loans.returnDate from Loans inner join Books on Books.bookID=Loans.bookID inner join Customers on Customers.customerID=Loans.customerID  where bookType={bType[0]} and loanID={bType[3]} '''
                    cur.execute(SQL)
                    displayAll1=cur.fetchall()
                    cur.executemany(f"insert into Late ('customerName', 'customerAge', 'bookName', 'author', 'bookType', 'loanDate', 'returnDate', 'lateBy' ) values (?,?,?,?,?,?,?,{overDays1})", (displayAll1)) 
                    con.commit()
            if bType[0]==2:
                date_format = "%Y-%m-%d"
                a = datetime.strptime(bType[1], date_format)
                b = datetime.strptime(bType[2], date_format)
                delta = b-a
                myDif=delta.days
                if myDif>5:
                    overDays2=myDif-5
                    SQL=f'''select distinct Customers.customerName, Customers.customerAge, Books.bookName, Books.author, bookType, Loans.loanDate, Loans.returnDate from Loans inner join Books on Books.bookID=Loans.bookID inner join Customers on Customers.customerID=Loans.customerID  where bookType={bType[0]} and loanID={bType[3]} '''
                    cur.execute(SQL)
                    displayAll2=cur.fetchall()
                    cur.executemany(f"insert into Late ('customerName', 'customerAge', 'bookName', 'author', 'bookType', 'loanDate', 'returnDate', 'lateBy' ) values (?,?,?,?,?,?,?,{overDays2})", (displayAll2)) 
                    con.commit()
            if bType[0]==3:
                date_format = "%Y-%m-%d"
                a = datetime.strptime(bType[1], date_format)
                b = datetime.strptime(bType[2], date_format)
                delta = b-a
                myDif=delta.days
                if myDif>2:
                    overDays3=myDif-2
                    SQL=f'''select distinct Customers.customerName, Customers.customerAge, Books.bookName, Books.author, bookType, Loans.loanDate, Loans.returnDate from Loans inner join Books on Books.bookID=Loans.bookID inner join Customers on Customers.customerID=Loans.customerID  where bookType={bType[0]} and loanID={bType[3]} '''
                    cur.execute(SQL)
                    displayAll3=cur.fetchall()
                    cur.executemany(f"insert into Late ('customerName', 'customerAge', 'bookName', 'author', 'bookType', 'loanDate', 'returnDate', 'lateBy' ) values (?,?,?,?,?,?,?,{overDays3})", (displayAll3)) 
                    con.commit()
        cur.execute("select distinct * from Late")
        allLateLoans=cur.fetchall()
        return render_template("/loans/lateLoans.html",allLateLoans=allLateLoans)



    
                


        
