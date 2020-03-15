import check
from librarysql import * 
#initialData()






def runLibrarian():

	#This input will be for the Librarian menu
	print("\nYour input was 1, You are a Librarian\n")
	inp = 0	
	#In Lib1, let them select a branch, or leave
	while inp != 2:
		print("\nLibrarian Menu:\n")
		print("1) Enter branch you manage\n2) Quit to main menu\n")
		inp = input("Please enter a number, either 1 or 2: ")
		if check.validInput(inp, 1, 2):
			inp = int(inp)
			if inp == 1:
				selectBranch()
			#Quit Lib1 to Main Menu
			else:
				print("\nMoving to main menu...")

#Lib2, Select branch you manage
def selectBranch():

	libraries = getTableData("tbl_library_branch")

	#numBranches + 1 will be our quit option
	numBranches = len(libraries)
	#This input will be for the library selection
	libInp = 0
	#Lib 2, Select library branch
	while libInp != (numBranches + 1):
		print("\nWhich branch do you manage?\n")
		#Print out options
		#for bId, location in libraries.items():
		for i in range(0,len(libraries)):
			#Allows for change in number of libraries
			print("{0}) {1}, {2}".format(libraries[i][0], libraries[i][1], libraries[i][2]))
		print("{0}) Quit to previous page\n".format(numBranches + 1))

		#Take input from user and take appropriate action
		libInp = input("Please enter a number between 1 and {0}: ".format(numBranches + 1))
		if check.validInput(libInp, 1, numBranches + 1):
			libInp = int(libInp)
			if libInp == (numBranches + 1):
				#Quit Lib2 to Lib1
				print("\nMoving to previous page...")
			else:
				#print (libraries)
				#Move to Lib 3
				branchIds=getIds("tbl_library_branch")
				adjustLibrary(branchIds[libInp-1], libraries[libInp-1][1], libraries[libInp-1][2],libraries)

#Lib3, 1) Update Branch Name/Location, 2) Update Numbers of Book Copies
def adjustLibrary(branchId, branchName, branchLocation, libraries):
	#Same thing as above
	inp = 0
	#In Lib3, for picking library actions
	while inp != 3:
		libraries=getTableData("tbl_library_branch")
		print("\nLibrary functions of library #{:d}".format(branchId))
		print("\nAt location: {0}, {1}".format(branchName, branchLocation))
		#List Lib3 options
		print("\n1) Update the details of the library\n2) Add copies of book to the branch\n3) Quit to previous\n")
		inp = input("Please enter a number between 1 and 3: ")
		if check.validInput(inp, 1, 3):
			inp = int(inp)
			#Option 1, Update Library Branch
			if inp == 1:
				changeBranchInfo(branchId, branchName, branchLocation, libraries)
				libraries=getTableData("tbl_library_branch")
				branchName=libraries[branchId-1][1]
				branchLocation=libraries[branchId-1][2]
			#Option 2, Update Book count
			elif inp == 2:
				updateBookCount(branchId, branchName, branchLocation, libraries)
			else:
				print("\nMoving to previous page...")

#Option 1, Change name and location of the branch
def changeBranchInfo(branchId, branchName, branchLocation, libraries):
	print("\nUpdate details of:", branchName)
	print("Branch ID:", branchId)
	print("Branch Location:", branchLocation)
	#Really all we need the funtion arguments for.
	print("\nYou have chosen to update the Branch with Branch Id:{0} and Branch Name:{1}.".format(branchId, branchName))
	print("Enter 'quit' at any prompt to cancel operation.\n")

	#This will tell us what to update the name to
	nameInput = input("Please enter new branch name or enter N/A for no change:\n")
	print("\nYou wrote:{0}\n".format(nameInput))
	if nameInput == "quit":
		return
	#libraries[branchId][1]=nameInput
	updateBranchName(branchId,nameInput)
	#This will tell us what to update the address to
	locInput = input("Please enter new branch address or enter N/A for no change:\n")
	print("\nYou wrote:{0}\n".format(locInput))
	if locInput == "quit":
		return

	#libraries[branchId][2]=locInput#updates instance of table
	updateBranchLocation(branchId,locInput)
	
#Option 2, Update number of books there are
def updateBookCount(branchId, branchName, branchLocation,table):
	MAX_BOOKS = 10000
	availableBooks= getAvailBooks(branchId)
	listOfCopies= getTableData("tbl_book_copies")
	#listOfcopies= method(bookcpies)

	print("\nChange number of copies of books at:", branchName)
	print("Branch ID:", branchId)
	print("Branch Location:", branchLocation)
	
	
	bookInp = 0
	numBooks = len(availableBooks)
	print("\nPick the Book you want to add copies of, to your branch:\n")
	
	for i in range(0,len(availableBooks)):
		
		print("{0}) {1} {2}".format(availableBooks[i][0], getBookTitle(availableBooks[i][0]), availableBooks[i][2]))
		#print("{0}) {1} by {2}".format(i, listOfCopies[i][1], listOfCopies[i][2]))
	print("{0}) Quit to previous page\n".format(numBooks + 1))

	#Take input from user and take appropriate action
	bookInp = input("Please enter a number between 1 and {0}: ".format(numBooks + 1))
	if check.validInput(bookInp, 1, numBooks + 1):
		bookInp = int(bookInp)
		if bookInp != (numBooks + 1):
			print("\nYou picked {0} {1}".format(availableBooks[bookInp-1][0],getBookTitle(availableBooks[bookInp-1][0])))
			print("\nExisting number of copies: {0}".format(availableBooks[bookInp-1][2]))
			#Enter new amount of copies
			newBookCount = input("Enter new number of copies: ")
			if  check.validInput(newBookCount, 0, MAX_BOOKS):
				newBookCount = int(newBookCount)

				#***Needs to send newBookCount to the database***
				print("\nYou entered {0}, this will be updated in DB".format(newBookCount))
				'''
						ADD SQL CODE HERE
				'''
				#listOfCopies[bookInp][2]=newBookCount
				updateBookCop(bookInp,newBookCount,branchId)
		print("\nMoving to previous page...")