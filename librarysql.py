# pip install mysql-connector-python

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="library"
)

mycursor = mydb.cursor()


def alter(state, msg):
    result = mycursor.execute(state, multi=True)
    result.send(None)
    print(msg, result)


def checkout(bookId, branchId, cardNo):
    addBookLoan(bookId, branchId, cardNo)
    removeBookCopy(bookId, branchId)


def addBookCopy(bookId, branchId):
    mycursor.execute(
        f"UPDATE tbl_book_copies SET noOfCopies = noOfCopies + 1 WHERE bookId = {bookId} AND branchId = {branchId}")
    mydb.commit()


def removeBookLoan(bookId, branchId, cardNo):
    mycursor.execute(
        f"DELETE FROM tbl_book_loans WHERE bookId = {bookId} AND branchId = {branchId} AND cardNo = {cardNo}")
    mydb.commit()


def processReturn(bookId, branchId, cardNo):
    addBookCopy(bookId, branchId)
    removeBookLoan(bookId, branchId, cardNo)


def addBookLoan(bookId, branchId, cardNo):
    mycursor.execute(
        f"INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES ({bookId}, {branchId}, {cardNo}, CURDATE(), DATE(CURDATE() + 7))")
    mydb.commit()


def removeBookCopy(bookId, branchId):
    mycursor.execute(
        f"UPDATE tbl_book_copies SET noOfCopies = noOfCopies - 1 WHERE bookId = {bookId} AND branchId = {branchId}")
    mydb.commit()


def checkedOut(bookId, branchId, cardNo):
    mycursor.execute(
        f"SELECT * FROM tbl_book_loans WHERE bookId = {bookId} AND branchId = {branchId} AND cardNo = {cardNo}")
    if len(mycursor.fetchall()) > 0:
        return True
    else:
        return False


def getTableData(tableName):
    mycursor.execute(f"SELECT * FROM {tableName}")
    return [list(item) for item in mycursor.fetchall()]


def getAuthorName(authorId):
    mycursor.execute(
        f"SELECT authorName FROM tbl_author WHERE authorId = {authorId}")
    return mycursor.fetchall()[0][0]


def getAuthorID(bookId):
    mycursor.execute(
        f"SELECT authorId FROM tbl_book_authors WHERE bookId = {bookId}")
    return mycursor.fetchall()[0][0]


def getAvailBooks(branchId):
    mycursor.execute(
        f"SELECT * FROM tbl_book_copies WHERE branchId = {branchId} AND noOfCopies > 0")
    return mycursor.fetchall()


def getBookTitle(bookId):
    mycursor.execute(
        f"SELECT title FROM tbl_book WHERE bookId = {bookId}")
    return mycursor.fetchall()[0][0]


def getBorrowedBooks(branchId, cardNo):
    mycursor.execute(
        f"SELECT bookId, dueDate FROM tbl_book_loans WHERE branchId = {branchId} AND cardNo = {cardNo}")
    return mycursor.fetchall()


def getBranchName(branchId):
    mycursor.execute(
        f"SELECT branchName FROM tbl_library_branch WHERE branchId = {branchId}")
    return mycursor.fetchall()[0][0]


def getAllBranches():
    mycursor.execute(
        f"SELECT * FROM tbl_library_branch")
    return mycursor.fetchall()


def getDueDate(bookId, branchId, cardNo):
    mycursor.execute(
        f"SELECT dueDate FROM tbl_book_loans WHERE bookId = {bookId} AND branchId = {branchId} AND cardNo = {cardNo}")
    return mycursor.fetchall()[0][0]


def getNumCopy(bookId, branchId):
    mycursor.execute(
        f"SELECT noOfCopies FROM tbl_book_copies WHERE bookId = {bookId} AND branchId = {branchId}")
    copies = mycursor.fetchall()[0][0]
    if copies > 0:
        return copies
    else:
        return 0


def getIds(tableName):
    if "genre" in tableName:
        mycursor.execute(f"SELECT genre_id FROM {tableName}")
    elif "publisher" in tableName:
        mycursor.execute(f"SELECT publisherId FROM {tableName}")
    elif "book" in tableName:
        mycursor.execute(f"bookId FROM {tableName}")
    elif "author" in tableName:
        mycursor.execute(f"SELECT tbl_author FROM {tableName}")
    elif "branch" in tableName:
        mycursor.execute(f"SELECT branchId FROM {tableName}")
    elif "borrower" in tableName:
        mycursor.execute(f"SELECT cardNo FROM {tableName}")

    return [item[0] for item in mycursor.fetchall()]


def initialData():
    # MODIFY PRIMARY KEYS TO AUTO INCREMENT
    try:
        alter("set foreign_key_checks=0;", "done")  # Remove foreign key checks
        alter("ALTER TABLE tbl_book MODIFY bookId INTEGER NOT NULL AUTO_INCREMENT", "done")
        alter("ALTER TABLE tbl_publisher MODIFY publisherId INTEGER NOT NULL AUTO_INCREMENT", "done")
        alter(
            "ALTER TABLE tbl_genre MODIFY genre_id INTEGER NOT NULL AUTO_INCREMENT", "done")
        alter(
            "ALTER TABLE tbl_author MODIFY authorId INTEGER NOT NULL AUTO_INCREMENT", "done")
        alter("ALTER TABLE tbl_library_branch MODIFY branchId INTEGER NOT NULL AUTO_INCREMENT", "done")
        alter(
            "ALTER TABLE tbl_borrower MODIFY cardNo INTEGER NOT NULL AUTO_INCREMENT", "done")
        # Adds foreign key checks back
        alter("set foreign_key_checks=1;", "done")
        mydb.commit()
    except Exception as e:
        mydb.rollback()  # undo all above changes if any errors
        raise e

    try:
        # INSERT BORROWERS
        alter("INSERT INTO tbl_borrower (name, address) VALUES ('Tom', '288 Bar')", "done")
        alter("INSERT INTO tbl_borrower (name, address) VALUES ('Jerry', 'New York City')", "done")
        alter("INSERT INTO tbl_borrower (name, address) VALUES ('Mickey', '1928')", "done")

        # INSERT LIBRARY BRANCHES
        alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('University Library', 'Boston')", "done")
        alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('State Liberty', 'New York')", "done")
        alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('Federal Library', 'Washington, DC')", "done")
        alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('County Library', 'McLean, VA')", "done")

        # INSERT AUTHORS
        alter("INSERT INTO tbl_author (authorName) VALUES ('Stephen King')", "done")
        alter("INSERT INTO tbl_author (authorName) VALUES ('Sidney Sheldon')", "done")
        alter("INSERT INTO tbl_author (authorName) VALUES ('Mark Penn')", "done")

        # INSERT BOOKS
        alter("INSERT INTO tbl_book (title) VALUES ('Lost Tribe')", "done")
        alter("INSERT INTO tbl_book (title) VALUES ('The Haunting')", "done")
        alter("INSERT INTO tbl_book (title) VALUES ('Microtrends')", "done")

        # INSERT BOOK-AUTHORS
        alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (1, 2)", "done")
        alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (2, 1)", "done")
        alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (3, 3)", "done")

        # INSERT BOOK-COPIES
        alter("INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (1, 1, 1)", "done")
        alter("INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (2, 1, 2)", "done")
        alter("INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (3, 1, 1)", "done")
        mydb.commit()
    except Exception as e:
        mydb.rollback()
        raise e

# # SELECTS ALL THEN STORE RESULTS
# mycursor.execute("SELECT * FROM tbl_library_branch")
# branches = mycursor.fetchall()

# mycursor.execute("SELECT * FROM tbl_author")
# authors = mycursor.fetchall()

# mycursor.execute("SELECT * FROM tbl_book")
# books = mycursor.fetchall()

# mycursor.execute("SELECT * FROM tbl_book_authors")
# bookAuthors = mycursor.fetchall()

# # PRINT RESULTS
# for branch in branches:
#   print(branch)

# for author in authors:
#   print(author)

# for book in books:
#   print(book)

# for bookAuthor in bookAuthors:
#   print(bookAuthor)

# alter("INSERT INTO tbl_borrower (name, address) VALUES ('Bob Tom', '321')","done")
# mydb.commit()
# mycursor.execute("SELECT cardNo FROM tbl_borrower")
# # borrowers = mycursor.fetchall()
# borrowers = [item[0] for item in mycursor.fetchall()]
# for borrower in borrowers:
#   print(borrower)
# print(borrowers)

# cardNum = input("Enter your card number:\n")
# cardNum = int(cardNum)
# print("\nCard number:", cardNum)

# if cardNum in borrowers:
# 	print("\nWelcome {0}!".format(borrowers[cardNum-1]))
# else:
# 	print("\nCard number not found. Please try again.\n")

# # mycursor.execute("UPDATE tbl_book SET title = 'The Test Title' WHERE bookId = 2")
# # mydb.commit()
