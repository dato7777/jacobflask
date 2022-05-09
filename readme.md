# LIBRARY MANAGEMENT WITH FLASK -

# THIS APPLICATION SHOULD BE ABLE TO EXECUTE SEVERAL COMMANDS AND IS COMBINED WITH PYTHON AS BACKEND, FLASK WITH HTML AS GUI AND SQLITE3 AS DATABASE

# TASKS:
1) I HAVE TO CREATE 3 TABLES AS SQL DATABASES: EACH TABLE MANAGED BY A CLASS OBJECT:
# CLASS BOOKS (book ID, book Name, book Author, Year published, Type(1,2,3))
    def addBook()
#  ***NOTE : The book type sets the maximum loan time for the book:  1 – up to 10 days  2 – up to 5 days  3 – up to 2 days***

# CLASS CUSTOMERS  (Customer ID, Customer name, customer city, customer age)
    def addCustomer()

# CLASS LOANS (Customer ID, book ID, Loan date, Return date)
    def addLoans()
# NOTE: In my library, one customer can borrow as many books as he can-if that book exists in the list of course

2) BUILD UNIT TESTS - GENERATE INITIAL DATABASE AS A START POINT - FOR EASY APPLIANCE AND COMFORTABLE TESTING
   - *DONE* I have created the python file (in the tools), generateData.py -which will generate initial data for 2 tables, as for 3rd table-Loans-it should be for user's reference to add loans. I am adding 4th table which is helpful for saving loaned books- To reenter the data after the book is returned.
   -*DONE* I need to create html page file, where all the information from the books table will appear
   -*DONE* I need to create html page file, where all the information from the customers table will appear
   -*SOLVED* I receive double results in the initial tables for books and customers
   -*SOLVED* I receive double results multuplying themselves in the loans table, after some days- i just used 'distinct'-solved all.

# VISUAL EXPERIENCE
1) My plan is to create comfortable environment for a client, I want all tables be visible while he chooses action.
Despite Eyal showed us iFrame function and it seems to be useful in my case, however, i think it will change the structure of my site a bit.
I will just use comma next to render template function and that will add tables for visual choice of the client.
only one thing: I have to copy and paste same table without navbar and other features.
   The problem is that lists can be long. But still to find any customer or book there is a specified button in the home menu.
   This is useful because I execute tasks according to Book ID or Customer ID, without inputting names.
2) I could add also find book by author as well, but considering it is easy to do, just takes time, I will ignore it.
# DECISION TO CREATE ADDITIONAL TABLES.
I would call them more virtual tables, which will be helpful in checking options.
My program goes with IDs a lot. I think it is ideal-because when client borrows a book- it makes sense he receives the loan ID or some kind of a check with order number-which is loan ID for me. 
When he returns a book-I will just enter the ID and I will avoid many mistakes this way.-----after some hours I realize loan ID is not enough, empty cells for RETURNDATE is also needed to check every option before returning the book.

# MISSION: BUILD A CLIENT WEB APPLICATION WITH THE BELOW MENTIONED LIBRARY MANAGEMENT TASKS:
 Add a new customer  Add a new book  Loan a book  Return a book  Display all books  Display all customers  Display all loans  Display late loans  Find book by name  Find customer by name  Remove book  Remover customer

I hope I made something interesting for you in terms of functions and their use, if not-in use of logic.
Thanks 
