# pip install mysql-connector-python

import mysql.connector


def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="library"
    )
 
def getTableData(tableName):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        result = cursor.fetchall()
        connection.commit()
        return [list(item) for item in result]
    except Exception as e:
        raise e
    finally:
        connection.close()
        cursor.close()
        
 
def getIds(tableName):
    if tableName == 'tbl_genre':
        idName = 'genre_id'
    elif tableName == 'tbl_publisher':
        idName = 'publisherId'
    elif tableName == 'tbl_book':
        idName = 'bookId'
    elif tableName == 'tbl_author':
        idName = 'authorId'
    elif tableName == 'tbl_library_branch':
        idName = 'branchId'
    elif tableName == 'tbl_borrower':
        idName = 'cardNo'
    connection = getConnection()
    try:
        cursor = connection.cursor()
        sql = f"SELECT {idName} FROM {tableName} ORDER BY {idName}"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        return [item[0] for item in result]
    except Exception as e:
        raise e
    finally:
        connection.close()
        cursor.close()
        

def checkout(bookId, branchId, cardNo):
    addBookLoan(bookId, branchId, cardNo)
    removeBookCopy(bookId, branchId)


def addBookCopy(bookId, branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "UPDATE tbl_book_copies SET noOfCopies = noOfCopies + 1 WHERE bookId = %s AND branchId = %s;"
        data = (bookId, branchId)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def removeBookLoan(bookId, branchId, cardNo):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "DELETE FROM tbl_book_loans WHERE bookId = %s AND branchId = %s AND cardNo = %s;"
        data = (bookId, branchId, cardNo)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def processReturn(bookId, branchId, cardNo):
    addBookCopy(bookId, branchId)
    removeBookLoan(bookId, branchId, cardNo)


def addBookLoan(bookId, branchId, cardNo):
    connection = getConnection()
    try: 
        cursor = connection.cursor()
        stmt = "INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (%s, %s, %s, CURDATE(), DATE(CURDATE() + 7));"
        data = (bookId, branchId, cardNo)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def removeBookCopy(bookId, branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "UPDATE tbl_book_copies SET noOfCopies = noOfCopies - 1 WHERE bookId = %s AND branchId = %s"
        data = (bookId, branchId)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def checkedOut(bookId, branchId, cardNo):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "SELECT * FROM tbl_book_loans WHERE bookId = %s AND branchId = %s AND cardNo = %s;"
        data = (bookId, branchId, cardNo)
        cursor.execute(stmt, data)
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
    finally:
        connection.close()
        cursor.close()
        


def getAuthorName(authorId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT authorName FROM tbl_author WHERE authorId = {authorId}")
        result = cursor.fetchall()
        connection.commit()
        return result[0][0]
    finally:
        connection.close()
        cursor.close()
        


def getAuthorID(bookId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT authorId FROM tbl_book_authors WHERE bookId = {bookId}")
        result = cursor.fetchall()
        connection.commit()
        return result[0][0]
    finally:
        connection.close()
        cursor.close()


def getAvailBooks(branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM tbl_book_copies WHERE branchId = {branchId} AND noOfCopies > 0")
        result = cursor.fetchall()
        connection.commit()
        return result
    finally:
        connection.close()
        cursor.close()
        


def getBookTitle(bookId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT title FROM tbl_book WHERE bookId = {bookId}")
        result = cursor.fetchall()
        connection.commit()
        return result[0][0]
    finally:
        connection.close()
        cursor.close()
        


def getBorrowedBooks(branchId, cardNo):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT bookId, dueDate FROM tbl_book_loans WHERE branchId = {branchId} AND cardNo = {cardNo}")
        result = cursor.fetchall()
        connection.commit()
        return result
    finally:
        connection.close()
        cursor.close()


def getBranchName(branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT branchName FROM tbl_library_branch WHERE branchId = {branchId}")
        result = cursor.fetchall()
        connection.commit()
        return result[0][0]
    finally:
        connection.close()
        cursor.close()


def getAllBranches():
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM tbl_library_branch")
        result = cursor.fetchall()
        connection.commit()
        return result
    finally:
        connection.close()
        cursor.close()
        


def getDueDate(bookId, branchId, cardNo):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT dueDate FROM tbl_book_loans WHERE bookId = {bookId} AND branchId = {branchId} AND cardNo = {cardNo}")
        result = cursor.fetchall()
        connection.commit()
        return result[0][0]
    finally:
        connection.close()
        cursor.close()
        


def getNumCopy(bookId, branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT noOfCopies FROM tbl_book_copies WHERE bookId = {bookId} AND branchId = {branchId}")
        result = cursor.fetchall()
        connection.commit()
        copies = result[0][0]
        if copies > 0:
            return copies
        else:
            return 0
    finally:
        connection.close()
        cursor.close()
        

def updateBookCop(bookId, numOfCop, branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "UPDATE tbl_book_copies SET noOfCopies = %s WHERE bookId = %s AND branchId = %s"
        data = (numOfCop, bookId, branchId)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def updateBranchName(branchId, newBranchName):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        #Removed single quotes from %s's, see if problematic
        stmt = "UPDATE tbl_library_branch SET branchName = %s WHERE branchId = %s"
        data = (newBranchName, branchId)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def updateBranchLocation(branchId, newBranchAddress):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        stmt = "UPDATE tbl_library_branch SET branchAddress = %s WHERE branchId = %s;"
        data = (newBranchAddress, branchId)
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def getAvailBooks2(branchId):
    connection = getConnection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM tbl_book_copies WHERE branchId = {branchId}")
        result = cursor.fetchall()
        connection.commit()
        return result
    finally:
        connection.close()
        cursor.close()
