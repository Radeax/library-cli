# We can put our names up here
# Started on 3/11/20
# Runs the program
import librarian as lib
import borrower as bor
import check


def main():
    inp = 0
    print("\nWelcome to the GCIT Library Management System.")

    # Main menu loop
    while inp != 4:
        print("\nWhich category of a user are you?\n\n1) Librarian\n2) Administrator\n3) Borrower\n4) To Quit\n")
        inp = input("Please enter a number between 1 and 4: ")
        # Check for valid input, then proceed
        if check.validInput(inp, 1, 4):
            inp = int(inp)
            if inp == 1:
                lib.runLibrarian()
            elif inp == 2:
                runAdministrator()
            elif inp == 3:
                bor.runBorrower()
            # If inp = 4
            else:
                print("\nGoodbye!")


def runAdministrator():
    print("\nYour input was 2, You are an Administrator")


main()
