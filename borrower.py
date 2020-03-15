import check
# import mysql.connector
from datetime import datetime
from librarysql import *

# initialData()  # Only run on a library database with no data
borrower = []
borrowerIds = getIds("tbl_borrower")
borrowers = getTableData("tbl_borrower")
branches = getAllBranches()


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


def bookOption(cardNum):
    inp = 0
    while inp != 3:
        # Display User Options
        print("\nWhat would you like to do?")
        print("\n1) Check out a book\n2) Return a book\n3) Quit to main menu\n")
        inp = input("Please enter a number between 1 and 3: ")

        # Take User Input
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


def selectLibBook(branchId, cardNum):
    branchName = branches[branchId-1][1]
    branchLoc = branches[branchId-1][2]

    bookInp = 0
    numBooks = -2

    while bookInp != numBooks + 1:
        bookCopies = getAvailBooks(branchId)
        numBooks = len(bookCopies)

        print(f"\nHere are the books at {branchName} in {branchLoc}.")

        print("\nPlease select a book to check out:\n")
        listNo = 0
        i = 1
        for bookCopy in bookCopies:
            if bookCopy[1] == branchId:
                bookID = bookCopy[0]
                title = getBookTitle(bookID)
                author = getAuthorName(getAuthorID(bookID))
                copiesLeft = getNumCopy(bookID, branchId)
                listNo = listNo + 1
                print(f"{listNo}) {title} by {author} | Available: {copiesLeft}")
            i += 1

        print(f"{numBooks + 1}) Quit to borrower menu\n")

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
                print(f"\nCopies remaining: {getNumCopy(myBookID, branchId)}")
            else:
                print("\nMoving to previous page...")
                break

# Option 2, Return a book


def selectBorBook(branchId, cardNum):
    loans = getBorrowedBooks(branchId, cardNum)
    print(getBorrowedBooks(branchId, cardNum))

    numLoans = len(loans)
    print("NumLoans =", numLoans)
    bookInp = 0

    if numLoans == 0:
        print("\nYou do not have any outstanding book loans.\n")
    else:
        while numLoans != 0:
            loans = getBorrowedBooks(branchId, cardNum)
            numLoans = len(loans)
            print(f"\nHere are the books owned by borrower #{cardNum}.")
            print("\nPlease select a book to return:\n")
            for i in range(0, numLoans):
                # Allows for change in number of books
                bookID = loans[i][0]
                title = getBookTitle(bookID)
                authorID = getAuthorID(bookID)
                author = getAuthorName(authorID)
                dueDate = getDueDate(
                    bookID, branchId, cardNum).strftime("%a, %m/%d/%Y")
                print(f"{i+1}) {title} by {author} | Due Date: {dueDate})")
            print(f"{numLoans + 1}) Quit to previous page\n")

            # bookInp = 0
            # Take input from user and take appropriate action
            bookInp = input(
                f"Please enter a number between 1 and {numLoans + 1}: ")
            if check.validInput(bookInp, 1, numLoans + 1):
                bookInp = int(bookInp)
                # If quit not selected
                if bookInp != (numLoans + 1):
                    myBook = loans[bookInp - 1]
                    print(f"\nYou picked {myBook[1]} with id: {myBook[0]}")
                    print(
                        f"\nYou are returning 1 copy of {myBook[1]} to {getBranchName(branchId)}.")
                    myBookID = myBook[0]
                    processReturn(myBookID, branchId, cardNum)
                else:
                    break

    print("\nMoving to previous page...")
