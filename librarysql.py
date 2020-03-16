# pip install mysql-connector-python

import mysql.connector


def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="library"
    )


mydb = getConnection()
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


def updateBookCop(bookId, numOfCop, branchId):
    mycursor.execute(
        f"UPDATE tbl_book_copies SET noOfCopies = {numOfCop} WHERE bookId = {bookId} AND branchId = {branchId}")
    mydb.commit()


def updateBranchName(branchId, newBranchName):
    mycursor.execute(
        f"UPDATE tbl_library_branch SET branchName = '{newBranchName}' WHERE branchId = '{branchId}'")
    mydb.commit()


def updateBranchLocation(branchId, newBranchAddress):
    mycursor.execute(
        f"UPDATE tbl_library_branch SET branchAddress = '{newBranchAddress}' WHERE branchId = '{branchId}'")
    mydb.commit()


def getAvailBooks2(branchId):
    mycursor.execute(
        f"SELECT * FROM tbl_book_copies WHERE branchId = {branchId}")
    return mycursor.fetchall()


def getIds(tableName):
    if "genre" in tableName:
        mycursor.execute(f"SELECT genre_id FROM {tableName} ORDER BY genre_id")
    elif "publisher" in tableName:
        mycursor.execute(f"SELECT publisherId FROM {tableName} ORDER BY publisherId")
    elif "book" in tableName:
        mycursor.execute(f"SELECT bookId FROM {tableName} ORDER BY bookId")
    elif "author" in tableName:
        mycursor.execute(f"SELECT authorId FROM {tableName} ORDER BY authorId")
    elif "branch" in tableName:
        mycursor.execute(f"SELECT branchId FROM {tableName} ORDER BY branchId")
    elif "borrower" in tableName:
        mycursor.execute(f"SELECT cardNo FROM {tableName} ORDER BY cardNo")

    return [item[0] for item in mycursor.fetchall()]
