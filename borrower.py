import check
# import mysql.connector
from librarysql import *

initialData()  # Only run on a library database with no data
borrower = []
borrowerIds = getIds("tbl_borrower")
borrowers = getTableData("tbl_borrower")
branches = getTableData("tbl_library_branch")
branches = getTableData("tbl_library_branch")
books = getTableData("tbl_book")
authors = getTableData("tbl_author")
book_authors = getTableData("tbl_book_authors")

# Takes card number


def runBorrower():
    cardNum = -1
    print("\nYour input was 3, You are a Borrower\n")
    print(borrowers)
    print(borrowerIds)
    while cardNum not in borrowerIds:
        cardNum = input("Enter your card number:\n")
        if check.validCardNum(cardNum):
            cardNum = int(cardNum)
            print("\nCard number:", cardNum)
            if cardNum in borrowerIds:
                # Find row where cardNo is cardNum
                i = borrowerIds.index(cardNum)
                borrower = borrowers[i]
                print(f"\nWelcome, {borrower[1]}!")
                bookOption(cardNum)
            else:
                print("\nCard number not found. Please try again.\n")

# Borr 1, Check out book or return book


def bookOption(cardNum):
    inp = 0
    while inp != 3:
        print("\nWhat would you like to do?")
        print("\n1) Check out a book\n2) Return a book\n3) Quit to main menu\n")
        inp = input("Please enter a number between 1 and 3: ")
        if check.validInput(inp, 1, 3):
            inp = int(inp)
            print("\nYou selected", inp)
            # Check out
            if inp == 1:
                selectBranch(cardNum, True)
            # Return book
            elif inp == 2:
                selectBranch(cardNum, False)
            elif inp == 3:
                print("\nMoving to main menu...")

# Used in both option 1 and 2


def selectBranch(cardNum, checkout):
    # numBranches + 1 will be our quit option
    numBranches = len(branches)
    branchID = 0

    # If checking out a book
    if checkout:
        print("\nPick the branch you want to check out from:\n")
    # If returning a book
    else:
        print("\nPick the branch you want to return book to:\n")

    i = 1
    for branch in branches:
        branchName = branch[1]
        branchLoc = branch[2]
        print(f"{i}) {branchName}, {branchLoc}")
        i += 1

    print(f"{numBranches + 1}) Quit to previous page\n")

    # Take input from user and take appropriate action
    branchID = input(f"Please enter a number between 1 and {numBranches+1}: ")

    if check.validInput(branchID, 1, numBranches + 1):
        branchID = int(branchID)
        if branchID == (numBranches + 1):
            # Quit to Borr1
            print("\nMoving to previous page...")
        elif checkout:
            # Move to book menu
            selectLibBook(branchID, cardNum)
        else:
            selectBorBook(branchID, cardNum)

# Option 1 p2, Select a book to check out then update the database


def selectLibBook(branchId, cardNum):
    branchName = branches[branchId-1][1]
    branchLoc = branches[branchId-1][2]

    bookInp = 0
    numBooks = -2

    while bookInp != numBooks + 1:
        # GET BOOK DATA
        # bookCopies = getTableData("tbl_book_copies")
        bookCopies = getAvailBooks(branchId)
        numBooks = len(bookCopies)

        print(f"\nHere are the books at {branchName} in {branchLoc}.")

        print("\nPlease select a book to check out:\n")
        listNo = 0
        i = 1
        for bookCopy in bookCopies:
            if bookCopy[1] == branchId:
                bookID = bookCopy[0]
                title = books[bookID-1][1]
                author = getAuthorName(getAuthorID(bookID))
                copiesLeft = getNumCopy(bookID, branchId)
                listNo = listNo + 1
                print(f"{listNo}) {title} by {author} | Available: {copiesLeft}")
            i += 1

        print("{0}) Quit to borrower menu\n".format(numBooks + 1))

        # Take input from user and take appropriate action
        bookChoice = input(
            f"Please enter a number between 1 and {numBooks + 1}: ")
        if check.validInput(bookChoice, 1, numBooks + 1):
            bookChoice = int(bookChoice)
            # If quit not selected
            if bookChoice != (numBooks + 1):
                print(numBooks)
                myBook = bookCopies[bookChoice-1]
                myBookID = myBook[0]
                print(f"\nYou picked {getBookTitle(myBookID)}")
                if checkedOut(myBookID, branchId, cardNum):
                    print(
                        f"\nYou already have a copy of {getBookTitle(myBookID)} checked out.")
                else:
                    print(
                        f"\nYou are checking out 1 copy of {getBookTitle(myBookID)}")
                    checkout(myBookID, branchId, cardNum)
                # This is merely cosmetic, will get actual value from DB
                print(f"\nCopies remaining: {getNumCopy(myBookID, branchId)}")
            else:
                print("\nMoving to previous page...")
                break

# Option 2, Return a book


def selectBorBook(branchId, cardNum):
    # **THIS WILL NEED A SQL QUERY TO POPULATE**
    # Will be based on library branch id
    # loans = {123: [[1, "The Lost Tribe", "3-10-20", "4-1-20"]], 234: [[1, "The Lost Tribe", "3-15-20", "4-6-20"],
    #                                                                   [2, "The Haunting", "3-5-20", "3-27-20"]], 345: []}
    loans = getBorrowedBooks(branchId, cardNum)
    print(getBorrowedBooks(branchId, cardNum))

    numLoans = len(loans)
    print("NumLoans =", numLoans)

    if numLoans == 0:
        print("\nYou do not have any outstanding book loans.\n")
    else:
        print("\nHere are the books owned by borrower #{0}.".format(cardNum))
        print("\nPlease select a book to return:\n")
        for i in range(0, numLoans):
            # Allows for change in number of books
            bookID = loans[i][0]
            title = getBookTitle(bookID)
            authorID = getAuthorID(bookID)
            author = getAuthorName(authorID)
            dueDate = getDueDate(bookID, branchId, cardNum)
            print(f"{i+1}) {title} by {author} (Due on {dueDate}")
            # print("{0}) {1} (Due on {2})".format(
            #     i + 1, books[i][1], books[i][3]))
        print("{0}) Quit to previous page\n".format(numLoans + 1))

        bookInp = 0
        # Take input from user and take appropriate action
        bookInp = input(
            "Please enter a number between 1 and {0}: ".format(numLoans + 1))
        if check.validInput(bookInp, 1, numLoans + 1):
            bookInp = int(bookInp)
            # If quit not selected
            if bookInp != (numLoans + 1):
                myBook = loans[bookInp - 1]
                print("\nYou picked {0} with id: {1}".format(
                    myBook[1], myBook[0]))
                print(f"\nYou are returning 1 copy of {0} to {1}.".format(
                    myBook[1], getBranchName(branchId)))
                myBookID = myBook[0]
                processReturn(myBookID, branchId, cardNum)

    print("\nMoving to previous page...")
