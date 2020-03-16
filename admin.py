import check
import datetime
from librarysql import *

def runAdministrator():
    print("\nYour input was 2, You are an Administrator")
    inp = 0
    while inp != 6:
        print("\nAdministrator Menu:")
        print("\nWhat would you like to do?\n\n1) Adjust Books and Authors\n2) Adjust Publishers")
        print("3) Adjust Library Branches\n4) Adjust Borrowers\n5) Override Due Date for a Book Loan\n6) Quit to main menu")
        inp = input("\nPlease enter a number between 1 and 6: ")
        if check.validInput(inp, 1, 6):
            inp = int(inp)
            if inp !=  6:
                selectAction(inp)
            else:
                print("\nMoving to main menu...")

def selectAction(tableId):
    #1 Books & authors
    #2 Publishers
    #3 Library Branches
    #4 Borrowers
    #5 Override Due Date in Book Loan
    tableNames = {1:['tbl_book', 'tbl_book_authors', 'tbl_author'], 2:['tbl_publisher'], 3:['tbl_library_branch'],
                    4:['tbl_borrower'], 5:['tbl_book_loans']}
    if tableId == 5:
        overrideDueDate()
        #Just send to a function
    else:
        inp = 0
        while inp != 4:
            print("\nMenu for Adjusting:")
            for tbl in tableNames[tableId]: print(tbl)
            print("\nPlease select your type of adjustment.\n\n1) Add\n2) Update\n3) Delete\n4) Quit to previous menu")
            inp = input("\nPlease enter a number between 1 and 4: ")
            if check.validInput(inp, 1, 4):
                inp = int(inp)
                #Updating singular tables can share a function
                if tableId != 1:
                    if inp ==  1:
                        add(tableNames[tableId][0])
                    elif inp ==  2:
                        update(tableNames[tableId][0])
                    elif inp ==  3:
                        delete(tableNames[tableId][0])
                    else:
                        print("\nMoving to previous menu...")
                #Updating books and authors requires consistency checks
                #They are in multiple tables
                else:
                    if inp ==  1:
                        addBookAuthor()
                    elif inp ==  2:
                        updateBookAuthor()
                    elif inp ==  3:
                        deleteBookAuthor()
                    else:
                        print("\nMoving to previous menu...")

#Special case: if updating books and author, must do consistency checks

def add(tableName):
    print("Adding to", tableName)
    #Based on table name, ask for specific fields to fill out
    if tableName == 'tbl_publisher':
        print("\nPlease limit input to 45 characters.")
        nameInput = input("What would you like to name the publisher(type 'quit' to quit)?:\n")
        if nameInput == 'quit':
            return
        print("\nPlease limit input to 45 characters.")
        addrInput = input("What is the address of the publisher(type 'quit' to quit)?:\n")
        if addrInput == 'quit':
            return
        print("\nPlease limit input to valid phone number.")
        phoneInput = input("What is the phone number of the publisher(type 'quit' to quit)?:\n")
        if phoneInput == 'quit':
            return
        #This gets executed by cursor
        stmt = "Insert into tbl_publisher values (NULL,%s,%s,%s);"
        data = (nameInput, addrInput, phoneInput)
    elif tableName == 'tbl_library_branch':
        print("\nPlease limit input to 45 characters.")
        nameInput = input("What would you like to name the library branch(type 'quit' to quit)?:\n")
        if nameInput == 'quit':
            return
        print("\nPlease limit input to 45 characters.")
        addrInput = input("What is the address of the library branch(type 'quit' to quit)?:\n")
        if addrInput == 'quit':
            return
        stmt = "Insert into tbl_library_branch values (NULL,%s,%s);"
        data = (nameInput, addrInput)

    elif tableName == 'tbl_borrower':
        print("\nPlease limit input to 45 characters.")
        nameInput = input("What would you like to name the borrower(type 'quit' to quit)?:\n")
        if nameInput == 'quit':
            return
        print("\nPlease limit input to 45 characters.")
        addrInput = input("What is the address of the borrower(type 'quit' to quit)?:\n")
        if addrInput == 'quit':
            return
        print("\nPlease limit input to valid phone number.")
        phoneInput = input("What is the phone number of the borrower(type 'quit' to quit)?:\n")
        if phoneInput == 'quit':
            return
        stmt = "Insert into tbl_borrower values (NULL,%s,%s,%s);"
        data = (nameInput, addrInput, phoneInput)

    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(stmt, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
        cursor.close()


def update(tableName):
    inp = -1
    numRows = -1
    #List rows in table
    while inp != numRows + 1:
        #Grab table data, primary keys, and count the tuples for the entire table
        #Should refresh after every update
        table = getTableData(tableName)
        tIds = getIds(tableName)
        numRows = len(table)
        #Have user select row tuple to update
        print(f"\nPlease select a row in {tableName} to update:\n")
        for i in range(0,numRows):
            print(f"{i+1}) {table[i]}")
        print(f"{numRows+1}) To quit to previous menu")
        inp = input(f"\nPlease enter a number between 1 and {numRows+1}: ")
        if check.validInput(inp, 1, numRows + 1):
            #Grab specific row based on selection
            inp = int(inp)
            if inp != numRows + 1:
                #Based on selection, grab data tuple, and it's primary key
                row = table[inp-1]
                pKey = tIds[inp-1]
                #Gonna have to do specific update based on table
                #But all tables using this function have name and address
                print("\nHere is the current name:", row[1])
                nameInput = input("\nWhat would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
                if nameInput in ('N/A', 'n/a', 'NA', 'na'):
                    #Since all tables her have data in the same order (id, name, addr), we leverage that to simplify these statements
                    #We could potentially use a conditional to tailor what index the data came from if that wasn't the case
                    nameInput = row[1]
                print("\nHere is the current address:", row[2])
                addrInput = input("\nWhat would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
                if addrInput in ('N/A', 'n/a', 'NA', 'na'):
                    addrInput = row[2]
     
                #Publisher and borrower need a phone number, not the library branch
                if tableName == 'tbl_publisher' or tableName == 'tbl_borrower':
                    print("\nHere is the phone number:", row[3])
                    phoneInput = input("\nWhat would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
                    if phoneInput in ('N/A', 'n/a', 'NA', 'na'):
                        phoneInput = row[3]
      
                #Tailor update statement to match the table we're updating
                if tableName == 'tbl_publisher':
                    stmt = "UPDATE tbl_publisher SET publisherName = %s, publisherAddress = %s, publisherPhone = %s WHERE publisherId = %s;"
                    data = (nameInput, addrInput, phoneInput, pKey)
                elif tableName == 'tbl_library_branch':
                    stmt = "UPDATE tbl_library_branch SET branchName = %s, branchAddress = %s WHERE branchId = %s;"
                    data = (nameInput, addrInput, pKey)
                elif tableName == 'tbl_borrower':
                    stmt = "UPDATE tbl_borrower SET name = %s, address = %s, phone = %s WHERE cardNo = %s;"
                    data = (nameInput, addrInput, phoneInput, pKey)
                
                #Send SQL statements to the database
                try:
                    connection = getConnection()
                    cursor = connection.cursor()
                    cursor.execute(stmt, data)
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
                    cursor.close()
            #If quit is chosen
            else:
                print("\nMoving to previous page...")               

        #List entire table
        #Take selection of row to edit
        #Go through items and update them, N/A if nothing

def delete(tableName):
    inp = -1
    numRows = -1
    #List rows in table
    while inp != numRows + 1:
        table = getTableData(tableName)
        tIds = getIds(tableName)
        numRows = len(table)
        print(f"\nPlease select a row in {tableName} to delete:\n")
        for i in range(0,numRows):
            print(f"{i+1}) {table[i]}")
        print(f"{numRows+1}) To quit to previous menu")
        inp = input(f"\nPlease enter a number between 1 and {numRows+1}: ")
        if check.validInput(inp, 1, numRows + 1):
            #Grab specific row based on selection
            inp = int(inp)
            if inp != numRows + 1:
                row = table[inp-1]
                #Let the user make sure of their decision
                print(f"\nAre you sure you want to delete:\n{row}")
                backout = input("\nType 'y' if you want to proceed: ")
                if backout in ('y', 'Y', 'yes', 'Yes', 'YES'):
                    print(f"\nDeleting {row}...")
                    pKey = tIds[inp-1]
                    #Gonna have to do specific delete based on table
                    if tableName == 'tbl_publisher':
                        #Delete the chosen row from the database
                        stmt = "DELETE FROM tbl_publisher WHERE publisherId = %s;"
                        data = (pKey,)
                    elif tableName == 'tbl_library_branch':
                        #Delete the chosen row from the database
                        stmt = "DELETE FROM tbl_library_branch WHERE branchId = %s;"
                        data = (pKey,)
                    elif tableName == 'tbl_borrower':
                        #Delete the chosen row from the database
                        stmt = "DELETE FROM tbl_borrower WHERE cardNo = %s;"
                        data = (pKey,)
                    #Send SQL statement to the database
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()
                        cursor.execute(stmt, data)
                        connection.commit()
                    except Exception as e:
                        connection.rollback()
                        raise e
                    finally:
                        connection.close()
                        cursor.close()
        else:
            print("\nMoving to previous page...")

def addBookAuthor():
    #Have user choose to add just a book, or add a new book and auth
    print("\nWould you like to add:\n\n1) Just a book, with existing author\n2) A book and an author\n3) To quit to previous")
    choice = input("\nPlease input an input between 1 and 3: ")
    #If add type choice isn't to quit
    if check.validInput(choice, 1, 3):
        choice = int(choice)
        #If user didn't select quit
        if choice != 3:
            #get book title to input into db
            print("\nPlease limit to 45 characters.")
            #If title is 'quit' then go to previous page
            #tileInp going into 
            titleInp = input("Please enter the title of the new book (type 'quit' to cancel):\n")
            #If user types quit
            if titleInp in ('q', 'Q', 'quit', 'Quit', 'QUIT'):
                print("\nMoving to previous page...")
                return
            #Give choice of publisher
            publishers = getTableData('tbl_publisher')
            pubIds = getIds('tbl_publisher')
            numPubs = len(publishers)           
            #List publishers in tbl_publisher, and have user choose one
            for i in range(0, numPubs):
                print(f"{i+1}) {publishers[i]}")
            print(f"{numPubs+1}) Quit to previous page")
            pubInp = input(f"\nPlease enter a number between 1 and {numPubs+1}: ")
            if check.validInput(pubInp, 1, numPubs+1):
                pubInp = int(pubInp)
                #If not quitting, remeber publisher Id of selection
                if pubInp != numPubs + 1:
                    #pubID is going into the database
                    #Grab publisher Id based on user's selection
                    pubId = pubIds[pubInp-1]
                    #Add title and pubLisherID to tbl_book
                    sql = "Insert into tbl_book values (NULL, %s, %s);"
                    data = (titleInp, pubId)
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()
                        #Had to insert here so there is an existing Id for the book
                        cursor.execute(sql, data)
                        connection.commit()
                        print("\nBook added to database.")
                    except Exception as e:
                        connection.rollback()
                        raise e
                    finally:
                        connection.close()
                        cursor.close()
                #If quitting
                else:
                    print("\nMoving to previous page...")
                    return
                #Want to assign an author that is already in the database
                if choice == 1:
                    #Select an exiting author
                    #This will go in tbl_book_authors, with the book_id
                    authors = getTableData('tbl_author')
                    authIds = getIds('tbl_author')
                    numAuths = len(authors)
                    #Listing authors
                    for i in range(0, numAuths):
                        print(f"{i+1}) {authors[i]}")
                    print(f"{numAuths+1}) Quit to previous page")
                    authInp = input(f"\nPlease enter a number between 1 and {numAuths+1}: ")
                    if check.validInput(authInp, 1, numAuths+1):
                        authInp = int(authInp)
                        #If not quitting, remeber publisher Id of selection
                        if authInp != numAuths + 1:
                            #authorId is going to be based on user's selection
                            authId = authIds[authInp-1]
                        #If quitting
                        else:
                            print("\nMoving to previous page...")
                            return
                #If choice = 2
                else:
                    #Ask user for a new author
                    print("\nPlease limit to 45 characters.")
                    #If nameInp is 'quit' then go to previous page
                    nameInp = input("Please enter the name of the new author (type 'quit' to cancel):\n")
                    #If user types quit
                    if nameInp in ('q', 'Q', 'quit', 'Quit', 'QUIT'):
                        print("\nMoving to previous page...")
                        return
                    #Add title and pubLisherID to tbl_book
                    sql = "Insert into tbl_author values (NULL, %s);"
                    data = (nameInp,)
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()
                        #Had to insert here so there is an existing Id for the book
                        cursor.execute(sql, data)
                        connection.commit()
                        print("\nAuthor added to database.")
                    except Exception as e:
                        connection.rollback()
                        raise e
                    finally:
                        connection.close()
                        cursor.close()
                    #For tbl_book_authors, get author id of author we just added
                    authIds = getIds('tbl_author')
                    print(f"authIds(from getIds):{authIds}")
                    authId = authIds[-1]
                #Now we need the book Id, need this for both instances
                #This is the book id of our newly added book
                bookIds = getIds('tbl_book')
                bookId = bookIds[-1]
                #Add bookId and authorId together in tbl_book_authors
                sql = "Insert into tbl_book_authors values (%s, %s);"
                data = (bookId, authId)
                try:
                    connection = getConnection()
                    cursor = connection.cursor()
                    #Had to insert here so there is an existing Id for the book
                    cursor.execute(sql, data)
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
                    cursor.close()
            #If input was invalid
            print("\nMoving to previous page ...")
        #If quit is selected
        else:
            print("\nMoving to previous page ...")
    
 
def updateBookAuthor():
    #Have user choose to add just a book, or add a new book and auth
    print("\nWould you like to update:\n\n1) Books\n2) Authors\n3) To quit to previous")
    choice = input("\nPlease input an input between 1 and 3: ")
    #If add type choice isn't to quit
    if check.validInput(choice, 1, 3):
        choice = int(choice)
        if choice != 3:
            inp = -1
            numRows = -1
            #List rows in table
            while inp != numRows + 1:
                #Grab table data, primary keys, and count the tuples for the entire table
                #Should refresh after every update
                if choice == 1:
                    tableName = 'tbl_book'
                else:
                    tableName = 'tbl_author'
                table = getTableData(tableName)
                tIds = getIds(tableName)
                numRows = len(table)
                #Have user select row tuple to update
                print(f"\nPlease select a row in {tableName} to update:\n")
                for i in range(0,numRows):
                    print(f"{i+1}) {table[i]}")
                print(f"{numRows+1}) To quit to previous menu")
                inp = input(f"\nPlease enter a number between 1 and {numRows+1}: ")
                if check.validInput(inp, 1, numRows + 1):
                    #Grab specific row based on selection
                    inp = int(inp)
                    #If not quit
                    if inp != numRows + 1:
                        #Based on selection, grab data tuple, and it's primary key
                        row = table[inp-1]
                        pKey = tIds[inp-1]
                        #Gonna have to do specific update based on table
                        #But all tables using this function have name and address
                        print("\nHere is the current name:", row[1])
                        nameInput = input("\nWhat would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
                        if nameInput in ('N/A', 'n/a', 'NA', 'na'):
                            nameInput = row[1]
                        #Tailor update statement to match the table we're updating
                        if tableName == 'tbl_book':
                            #Give choice of publisher
                            publishers = getTableData('tbl_publisher')
                            pubIds = getIds('tbl_publisher')
                            numPubs = len(publishers)           
                            #List publishers in tbl_publisher, and have user choose one
                            for i in range(0, numPubs):
                                print(f"{i+1}) {publishers[i]}")
                            print(f"{numPubs+1}) Keep the same publisher")
                            pubInp = input(f"\nPlease enter a number between 1 and {numPubs+1}: ")
                            if check.validInput(pubInp, 1, numPubs+1):
                                pubInp = int(pubInp)
                                #If changing the publisher
                                if pubInp != numPubs + 1:
                                    pubId = pubIds[pubInp-1]
                                else:
                                    #Use the publisher Id of the book we selected
                                    pubId = row[2]
                            stmt = "UPDATE tbl_book SET title = %s, pubId = %s WHERE bookId = %s;"
                            data = (nameInput, pubId, pKey)
                        elif tableName == 'tbl_author':
                            stmt = "UPDATE tbl_author SET authorName = %s WHERE authorId = %s;"
                            data = (nameInput, pKey)
                        #Send SQL statements to the database
                        try:
                            connection = getConnection()
                            cursor = connection.cursor()
                            cursor.execute(stmt, data)
                            connection.commit()
                        except Exception as e:
                            connection.rollback()
                            raise e
                        finally:
                            connection.close()
                            cursor.close()
                    else:
                        print("\nMoving to previous page ...")

def deleteBookAuthor():
    inp = -1
    numBooks = -1
    #List rows in table
    while inp != numBooks + 1:
        books = getTableData('tbl_book')
        bIds = getIds('tbl_book')
        numBooks = len(books)
        print(f"\nPlease select a book to delete:\n")
        for i in range(0, numBooks):
            print(f"{i+1}) {books[i]}")
        print(f"{numBooks+1}) To quit to previous menu")
        inp = input(f"\nPlease enter a number between 1 and {numBooks+1}: ")
        if check.validInput(inp, 1, numBooks + 1):
            #Grab specific row based on selection
            inp = int(inp)
            if inp != numBooks + 1:
                book = books[inp-1]
                #Let the user make sure of their decision
                print(f"\nAre you sure you want to delete:\n{book}")
                backout = input("\nType 'y' if you want to proceed: ")
                if backout in ('y', 'Y', 'yes', 'Yes', 'YES'):
                    print(f"\nDeleting {book}...")
                    pKey = bIds[inp-1]
     
                    #Delete book from tbl_book and tbl_book_authors
                    stmt = "DELETE FROM tbl_book_authors WHERE bookId = %s;"
                    data = (pKey,)
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()
                        cursor.execute(stmt, data)
                        connection.commit()
                    except Exception as e:
                        connection.rollback()
                        raise e
                    finally:
                        connection.close()
                        cursor.close()
      
                    stmt = "DELETE FROM tbl_book WHERE bookId = %s;"
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()
                        cursor.execute(stmt, data)
                        connection.commit()
                    except Exception as e:
                        connection.rollback()
                        raise e
                    finally:
                        connection.close()
                        cursor.close()
                    #Send SQL statements to the database
                    authorIds = getIds('tbl_author')
                    #Find all author ids in tbl_book_author
                    connection = getConnection()
                    try:
                        cursor = connection.cursor()
                        sql = "SELECT authorId FROM tbl_book_authors;"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        connection.commit()
                        bAuthorIds =  [item[0] for item in result]
                    finally:
                        connection.close()
                        cursor.close()
     
                    badId = -1
                    #If author Id is in tbl_author but not in tbl_book_authors, then delete that author
                    #In other words, delete the author with no books
                    for aId in authorIds:
                        if aId not in bAuthorIds:
                            badId = aId
                            stmt = "DELETE FROM tbl_author WHERE authorId = %s;"
                            data = (badId,)
                            try:
                                connection = getConnection()
                                cursor = connection.cursor()
                                cursor.execute(stmt, data)
                                connection.commit()
                            except Exception as e:
                                connection.rollback()
                                raise e
                            finally:
                                connection.close()
                                cursor.close()
                    
def overrideDueDate():
    inp = -1
    numBors = -1 
    #Unless the user wants to quit
    while inp != numBors + 1:
        #Get borrower data from database
        borrowers = getTableData('tbl_borrower')
        numBors = len(borrowers)
        cardNums = getIds('tbl_borrower')
        print(f"\nPlease select a borrower to override due date of:\n")
        #Display borrowers
        for i in range(0, numBors):
            print(f"{i+1}) {borrowers[i]}")
        print(f"{numBors+1}) To quit to previous menu")
        inp = input(f"\nPlease enter a number between 1 and {numBors+1}: ")
        if check.validInput(inp, 1, numBors + 1):
            #Grab specific borrower based on selection
            inp = int(inp)
            if inp != numBors + 1:
                borrower = borrowers[inp-1]
                cardNum = cardNums[inp-1]
                #Find borrower's loans in tbl_book_loans
                loanCount = 0
                connection = getConnection()
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM tbl_book_loans WHERE cardNo = %s", (cardNum,))
                    borLoans = cursor.fetchall()
                    loanCount = len(borLoans)
                    connection.commit()
                except Exception as e:
                    raise e
                finally:
                    connection.close()
                    cursor.close()   
 
                #If there aren't any loans, then leave page
                if loanCount == 0:
                    print("\nThis borrower has no outstanding loans.")
                    print("\nMoving to previous page ...")
                    return
                #Otherwise, show the user their loans
                else:
                    print(f"\nOverriding due dates for {borrower[1]}.")
                    loanInp = -1
                    while loanInp != loanCount + 1:
                        print(f"\nPlease select a loan to override due date of:\n")
                        #Will refresh the due dates after they are changed
                        connection = getConnection()
                        try:
                            cursor = connection.cursor()
                            cursor.execute("SELECT * FROM tbl_book_loans WHERE cardNo = %s", (cardNum,))
                            borLoans = cursor.fetchall()
                            #This will show the loans with the book title and branch name
                            stmt = "SELECT bor.name, lb.branchName, b.title, bl.dateOut, bl.dueDate FROM tbl_book AS b, tbl_book_loans AS bl, tbl_borrower AS bor, tbl_library_branch AS lb WHERE b.bookId = bl.bookId AND bor.cardNo = bl.cardNo AND lb.branchId = lb.branchId AND bor.cardNo = %s;"
                            cursor.execute(stmt, (cardNum,))
                            borLoanNames = cursor.fetchall()
                        except Exception as e:
                            raise e
                        finally:
                            connection.close()
                            cursor.close()
                        #Print show user what loans the borrower has
                        for i in range(0, loanCount):
                            dateOut = borLoanNames[i][3].strftime("%m-%d-%y")
                            dueDate = borLoanNames[i][4].strftime("%m-%d-%y")
                            print(f"{i+1}) Branch: {borLoanNames[i][1]}, Book: {borLoanNames[i][2]}, Date Out: {dateOut}, Due Date: {dueDate}")
                        print(f"{loanCount+1}) To quit to previous menu")
                        loanInp = input(f"\nPlease enter a number between 1 and {loanCount+1}: ")
                        if check.validInput(loanInp, 1, loanCount + 1):
                            #Grab specific row based on selection
                            loanInp = int(loanInp)
                            if loanInp != loanCount + 1:
                                loan = borLoans[loanInp-1]
                                #Show user current due date
                                #**Maybe clean up how the date is displayed
                                print(f"\nThis borrower has a due date of: {loan[4]}")
                                #User inputs date or quits
                                newDate = input("Please input new date (yyyy-mm-dd), enter 'quit' if no change:\n")
                                
                                if newDate in ('quit', 'QUIT', 'Quit', 'Q', 'q'):
                                    print("\nMoving to previous menu ...")
                                else:
                                    #**Could use a decent date format validation
                                    stmt = "UPDATE tbl_book_loans SET dueDate = %s WHERE bookId = %s AND branchId = %s AND cardNo = %s;"
                                    data = (newDate, loan[0], loan[1], loan[2])
                                    try:
                                        connection = getConnection()
                                        cursor = connection.cursor()
                                        cursor.execute(stmt, data)
                                        connection.commit()
                                    except Exception as e:
                                        connection.rollback()
                                        raise e
                                    finally:
                                        connection.close()
                                        cursor.close()
                            else:
                                print("\nMoving to previous page ...")
        else:
            print("Moving to previous page ...")
