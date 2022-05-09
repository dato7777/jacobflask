import sqlite3
from flask import render_template, request
from sqlite3 import Error

con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()

class Customers:
    
    def __init__(self, customerID, customerName, customerCity, customerAge):
        self.customerID = customerID
        self.customerName = customerName
        self.customerCity = customerCity
        self.customerAge = customerAge
        
    
    def addCustomer(self):
        msg=""
        if request.method=='POST':
            self.customerName = request.form.get('customerName')
            self.customerCity = request.form.get('customerCity')
            self.customerAge = request.form.get('customerAge')
            cur.execute(f'''INSERT INTO Customers VALUES(not null, "{self.customerName}", "{self.customerCity}", {int(self.customerAge )})''')
            con.commit()
            msg="Customer has been added to list!"
        return render_template("/customers/addCustomer.html", msg=msg)
    
    def removeCustomer(self):
        msg=""
        if request.method=='POST':
            self.customerID = request.form.get('customerID')
            cur.execute(f'''select count(customerID) from Customers where customerID={self.customerID}''')
            numberOfID=cur.fetchone()
            if numberOfID[0]==0:
                msg="Please choose a customer from list below and in range"
                return render_template("/customers/removeCustomer.html", msg=msg)
            else:
                cur.execute(f'''select count(customerID) from Loans where customerID={self.customerID} and returnDate=" "''')
                customerCheck=cur.fetchone()
                if customerCheck[0]==0:
                    cur.execute(f'''delete from Customers where customerID="{self.customerID}"''')
                    con.commit()
                    msg="The Customer has been removed!"
                    return render_template("/customers/removeCustomer.html", msg=msg)
                else:
                    # SQL=f'''select customerID, returnDate from Loans where customerID={self.customerID}'''
                    # cur.execute(SQL)
                    # forbiddenCustomer=cur.fetchone()
                    # if forbiddenCustomer[1]==" ":
                    msg="Cannot delete customer with borrowed book"
                    return render_template("/customers/removeCustomer.html", msg=msg)
                    
            # return render_template("/customers/removeCustomer.html", msg=msg)
        return render_template("/customers/removeCustomer.html", msg=msg)

    def displayCustomers(self):
        cur.execute("select distinct * from Customers")
        myCustomers=cur.fetchall()
        return render_template("/customers/customers.html", myCustomers=myCustomers)

    def FindCustomer(self):
        msg=""
        if request.method=='POST':
            self.customerName = request.form.get('customerName')
            cur.execute(f'''select * from Customers where customerName like "%{self.customerName}%"''')
            filteredCustomers=cur.fetchall()
            con.commit()
            if len(filteredCustomers)>0:
                msg="The customer is found!"
                return render_template("/customers/findCustomer.html", filteredCustomers=filteredCustomers,msg=msg)
            else:
                msg="Customer is not in the list"
        return render_template("/customers/findCustomer.html",msg=msg)