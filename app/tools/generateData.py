import sqlite3
from sqlite3 import Error
con = sqlite3.connect('Library.db', check_same_thread=False)

cur = con.cursor()

def genTables():
    try:
    # Generates 3 tables 
        cur.execute('''CREATE TABLE Books
                            (bookID INTEGER PRIMARY KEY AUTOINCREMENT, bookName text, author text, yearPublished int, bookType int)''')
        cur.execute('''CREATE TABLE Customers
                            (customerID INTEGER PRIMARY KEY AUTOINCREMENT, customerName text, customerCity text, customerAge int)''')
        cur.execute('''CREATE TABLE Loans
                            (loanID INTEGER PRIMARY KEY AUTOINCREMENT, customerID int, bookID int, loanDate int, returnDate int)''')
        cur.execute('''CREATE TABLE LoanedBooksList
                            (bookID int, bookName text, author text, yearPublished int, bookType int)''')
        cur.execute('''CREATE TABLE Late
                            (customerName text, customerAge int, bookName text, author text, bookType int, loanDate int NOT NULL, returnDate int NOT NULL, lateBy int)''')
    except:
        print("table already exist")
    else:
        print("Tables created successfully")
    con.commit()

def genBooksData(): #inputs initial data 
    book_list = [
        (('Carrie'),('Stephen King'),(1974),(1)),
        (('The Godfather'),('Mario Puzo'),(1969),(3)),
        (('Babbitt'),('Sinclair Lewis'),(1922), (2)),
        (('Money'),('Martin Amis'),(1984), (3)),
        (('Midnights Children'),('Salman Rushdie'),(1981), (1)),
        (('East of Eden'),('John Steinbeck'),(1952), (2)),
        (('Foundation'),('Isaac Asimov'),(1942), (3))]
    
    cur.executemany("insert into Books ('bookName','author','yearPublished','bookType') values(?,?,?,?)", (book_list))
    
    con.commit()

def genCustomersData():
    customers_list = [
         (('Jacob Gor'),('Bat Yam'),(42)),
         (('Sam Franklin'),('London'),(23)),
         (('Natasha Zeiss'),('Antwerpen'),(18)),
         (('Omer Sasson'),('Tel Aviv'),(30)),
         (('Michael Bradley'),('Bat Yam'),(42)),
         (('Avner Ivanov'),('Kiev'),(20)),
         (('Giorgi Kinkladze'),('Tbilisi'),(17))]
    
    cur.executemany("insert into Customers ('customerName', 'customerCity', 'customerAge') values (?,?,?)", (customers_list)) 
    
    con.commit()
        
        
