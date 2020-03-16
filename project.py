# We can put our names up here
# Started on 3/11/20
# Runs the program
import librarian as lib
import borrower as bor
import admin as ad
import check
from librarysql import *


def main():
    print("\nWelcome to the GCIT Library Management System.")
    inp = 0
    # Main menu loop
    while inp != 4:
        print("\nWhich category of a user are you?:\n\n1) Librarian\n2) Administrator\n3) Borrower\n4) To Quit")
        inp = input("\nPlease enter a number between 1 and 4: ")
        # Check for valid input, then proceed
        if check.validInput(inp, 1, 4):
            inp = int(inp)
            if inp == 1:
                lib.runLibrarian()
            elif inp == 2:
                ad.runAdministrator()
            elif inp == 3:
                bor.runBorrower()
            # If inp = 4
            else:
                print("\nGoodbye!")


main()
