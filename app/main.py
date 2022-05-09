from flask import Flask,json, request, render_template
import sqlite3
from sqlite3 import Error
from .tools.books import Books
from .tools.customers import Customers
from .tools.generateData import genBooksData,genCustomersData,genTables
from .tools.loans import Loans
app = Flask(__name__)

con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()

               # Here You can generate initial Data: 
               # Instructions: 1) Run the app first while generation modules below are in hashtag
                             # 2) Release the hashtags from modules BELOW and save (ctrl+s)
                             # 3) Hashtag the modules again to avoid multiplications in database table 
# genTables()
# genBooksData()
# genCustomersData()


@app.route("/", methods=['GET'])
def home():
        return render_template("home.html")


@app.route("/books", methods=['GET'])
def displayBooks():
        return Books.displayBooks(Books)

@app.route("/booksNoNav", methods=['GET'])
def BooksNoNav():
        cur.execute("select * from Books")
        myBooks=cur.fetchall()
        return render_template("/books/booksNoNav.html", myBooks=myBooks)

@app.route("/addBook", methods=['GET', 'POST'])
def bookAdd():
    #print(request.form.get("author"))
    return Books.addBook(Books)

@app.route("/removeBook", methods=['GET', 'POST'])
def bookRemove():
    return Books.removeBook(Books)+ BooksNoNav()

@app.route("/findBook", methods=['GET', 'POST'])
def bookFind():
    return Books.FindBook(Books)

@app.route("/addCustomer", methods=['GET', 'POST'])
def customerAdd():
    return Customers.addCustomer(Customers)

@app.route("/removeCustomer", methods=['GET', 'POST'])
def customerRemove():
    return Customers.removeCustomer(Customers)+CustomersNoNav()

@app.route("/findCustomer", methods=['GET', 'POST'])
def CustomerFind():
    return Customers.FindCustomer(Customers)

@app.route("/customers", methods=['GET'])
def displayCustomers():
        return Customers.displayCustomers(Customers)

@app.route("/customersNoNav", methods=['GET'])
def CustomersNoNav():
        cur.execute("select * from Customers")
        myCustomers=cur.fetchall()
        return render_template("/customers/customersNoNav.html", myCustomers=myCustomers)

@app.route("/addLoan", methods=['GET', 'POST'])
def loanAdd():
    return Loans.addLoan(Loans)+CustomersNoNav() + BooksNoNav()

@app.route("/loans", methods=['GET'])
def loansDisplay():
        
        return Loans.loansDisplay(Loans)

@app.route("/returnBook", methods=['GET', 'POST'])
def bookReturn():
    return Loans.returnLoan(Loans)+LoansNoNav()

@app.route("/loansNoNav", methods=['GET'])
def LoansNoNav():
    cur.execute("select * from Loans")
    myLoans=cur.fetchall()
    return render_template("/loans/loansNoNav.html", myLoans=myLoans)

@app.route("/lateLoans", methods=['GET'])
def displayLate():
    return Loans.lateLoans(Loans)

if __name__ == '__main__':
    app.run(debug=True)