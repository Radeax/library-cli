import check

#Takes card number
def runBorrower():
	print "\nYour input was 3, You are a Borrower\n"
	cardNum = -1
	#borrowers = {123: "John Smith", 234: "Jack Ryan", 345: "Phil Collins"}
	#
	#
	mycursor.execute("SELECT cardNo FROM tbl_borrower")
	borrowers = mycursor.fetchall()
	#
	#
	#
	while cardNum not in borrowers:
		cardNum = raw_input("Enter your card number:\n")
		if validCardNum(cardNum):
			cardNum = int(cardNum)
			print "\nCard number:", cardNum
			if cardNum in borrowers:
				print "\nWelcome {0}!".format(borrowers[cardNum])
				bookOption(cardNum)
			else:
				print "\nCard number not found. Please try again.\n"

#Borr 1, Check out book or return book
def bookOption(cardNum):
	inp = 0
	while inp != 3:
		print "\nWhat would you like to do?"
		print "\n1) Check out a book\n2) Return a book\n3) Quit to main menu\n"
		inp = raw_input("Please enter a number between 1 and 3: ")
		if check.validInput(inp, 1, 3):
			inp = int(inp)
			print "\nYou selected", inp
			#Check out
			if inp == 1:
				selectBranch(cardNum, True)
			#Return book
			elif inp == 2:
				selectBranch(cardNum, False)
			elif inp == 3:
				print "\nMoving to main menu..."

#Option1, Check out book
def selectBranch(cardNum, checkout):
	#IMPORTANT NOTE
	#**Probably need function to grab libraries from database, this will change**
	#libraries = {1: ["University Library", "Boston"], 2: ["State Library", "New York"], 
	#			3: ["Federal Library", "Washington DC"], 4: ["County Library", "McLean VA"],
	#			5: ["Test Library", "Maryland"]}

	mycursor.execute("SELECT branchName, branchAddress FROM tbl_library_branch")
	libraries = mycursor.fetchall()

	#numBranches + 1 will be our quit option
	numBranches = len(libraries)
	#This input will be for the library selection
	libInp = 0
	#If checking out a book
	if checkout:
		print "\nPick the branch you want to check out from:\n"
	#If returning a book
	else:
		print "\nPick the branch you want to return book to:\n"
	#Print out options
	for bId, location in libraries.items():
		#Allows for change in number of libraries
		print "{0}) {1}, {2}".format(bId, location[0], location[1])
	print "{0}) Quit to previous page\n".format(numBranches + 1)

	#Take input from user and take appropriate action
	libInp = raw_input("Please enter a number between 1 and {0}: ".format(numBranches + 1))
	if check.validInput(libInp, 1, numBranches + 1):
		libInp = int(libInp)
		if libInp == (numBranches + 1):
			#Quit to Borr1
			print "\nMoving to previous page..."
		elif checkout:
			#Move to book menu
			selectLibBook(libInp, libraries[libInp][0], libraries[libInp][1], cardNum)
		else:
			selectBorBook(libInp, libraries[libInp][0], libraries[libInp][1], cardNum)

#Option 1, Select a book to check out then update the database
def selectLibBook(branchId, branchName, branchLocation, cardNum):	
	bookInp = 0
	numBooks = -2
	while bookInp != numBooks + 1:
		#**THIS WILL NEED A SQL QUERY TO POPULATE**
		#Will be based on library branch id
		books = {1: ["The Lost Tribe", "Sidney Sheldon", 5], 2: ["The Haunting", "Stephen King", 3],
				3: ["Microtrends", "Sidney Sheldon", 10], 4: ["Test Book", "John Jackson", 0]}
		numBooks = len(books)

		print "\nHere are the books at {0} in {1}.".format(branchName, branchLocation)
		print "\nPlease select a book to check out:\n"
		for bId, bInfo in books.items():
			#Allows for change in number of books
			print "{0}) {1} copies of {2} by {3}".format(bId, books[bId][2], bInfo[0], bInfo[1])
		print "{0}) Quit to previous page\n".format(numBooks + 1)

		#Take input from user and take appropriate action
		bookInp = raw_input("Please enter a number between 1 and {0}: ".format(numBooks + 1))
		if check.validInput(bookInp, 1, numBooks + 1):
			bookInp = int(bookInp)
			#If quit not selected
			if bookInp != (numBooks + 1):
				myBook = books[bookInp]
				print "\nYou picked {0}".format(myBook[0])
				#CHECK FOR 0 COPIES
				if myBook[2] == 0:
					print "\nSorry we have no more copies of", myBook[0]
				else:
					print "\nYou are checking out 1 copy of", myBook[0]
					#***Needs to subtract 1 from no_book_copies in the database***
					#Include in book loans the date out (curdate), and due date (add a week)
					'''
						ADD SQL CODE HERE
					'''

					#This is merely cosmetic, will get actual value from DB
					print "\nNew number of copies: {0}".format(myBook[2] - 1)
			else:
				print "\nMoving to previous page..."

#Option 2, Borrow a book
def selectBorBook(branchId, branchName, branchLocation, cardNum):
	#**THIS WILL NEED A SQL QUERY TO POPULATE**
	#Will be based on library branch id
	loans = {123:[[1, "The Lost Tribe", "3-10-20", "4-1-20"]], 234:[[1, "The Lost Tribe", "3-15-20", "4-6-20"],
	 [2, "The Haunting", "3-5-20", "3-27-20"]], 345:[]} 

	numLoans = len(loans[cardNum])
	print "NumLoans =", numLoans

	if numLoans == 0:
		print "\nYou do not have any outstanding book loans.\n"
	else:
		books = loans[cardNum]

		print "\nHere are the books owned by borrower #{0}.".format(cardNum)
		print "\nPlease select a book to return:\n"
		for i in range(0, numLoans):
			#Allows for change in number of books
			print "{0}) {1} (Due on {2})".format(i + 1, books[i][1], books[i][3])
		print "{0}) Quit to previous page\n".format(numLoans + 1)

		bookInp = 0
		#Take input from user and take appropriate action
		bookInp = raw_input("Please enter a number between 1 and {0}: ".format(numLoans + 1))
		if check.validInput(bookInp, 1, numLoans + 1):
			bookInp = int(bookInp)
			#If quit not selected
			if bookInp != (numLoans + 1):
				myBook = books[bookInp - 1]
				print "\nYou picked {0} with id: {1}".format(myBook[1], myBook[0])
				print "\nYou are returning 1 copy of {0} to {1}.".format(myBook[1], branchName)
				#***Needs to add 1 from no_book_copies in the database***
				#Also needs to remove the book from book loans
				'''
					ADD SQL CODE HERE
				'''
			
	print "\nMoving to previous page..."

def validCardNum(inp):
	try:
		int(inp)
	except ValueError:
		print "\n-------------------------\nInvalid input. Try Again\n-------------------------\n"
		print "\nWrong data type, please use an integer.\n"
		return False
	else:
		#Check if in range
		if int(inp) < 0:
			print "\n-------------------------\nInvalid input. Try Again\n-------------------------\n"
			print "\nYour input should be a positive number.\n"
			return False
		else:
			return True