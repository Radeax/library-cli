import check
from librarysql import *

def runAdministrator():
	print("\nYour input was 2, You are an Administrator")
	inp = 0
	while inp != 6:
		print("\nAdministrator Menu:\n")
		print("What would you like to do?\n\n1) Adjust Books and Authors\n2) Adjust Publishers")
		print("3) Adjust Library Branches\n4) Adjust Borrowers\n5) Override Due Date for a Book Loan\n6) Quit to main menu\n")
		inp = input("Please enter a number between 1 and 6: ")
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
		print("Override due date, gonna be it's own function")
		#Just send to a function
	else:
		inp = 0
		while inp != 4:
			print("\nMenu for Adjusting:")
			for tbl in tableNames[tableId]: print(tbl)
			print("\nPlease select your type of adjustment.\n\n1) Add\n2) Update\n3) Delete\n4) Quit to previous menu\n")
			inp = input("Please enter a number between 1 and 4: ")
			if check.validInput(inp, 1, 4):
				inp = int(inp)
				#Updating singular tables can share a function
				if tableId != 1:
					if inp ==  1:
						add(tableNames[tableId][0])
					elif inp ==  2:
						update(tableNames[tableId][0])
					if inp ==  3:
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
					if inp ==  3:
						deleteBookAuthor()
						print("\nMoving to previous menu...")

#Special case: if updating books and author, must do consistency checks

def add(tableName):
	print("Adding to", tableName)
	if tableName == 'tbl_publisher':
		print("Please limit input to 45 characters.")
		nameInput = input("What would you like to name the publisher(type 'quit' to quit):")
		if nameInput == 'quit':
			return
		print("Please limit input to 45 characters.")
		addrInput = input("What is the address of the publisher(type 'quit' to quit):")
		if addrInput == 'quit':
			return
		print("Please limit input to valid phone number.")
		phoneInput = input("What is the phone number of the publisher(type 'quit' to quit):")
		if phoneInput == 'quit':
			return
		try:
			mycursor.execute(f"Insert into tbl_publisher values (NULL,'{nameInput}','{addrInput}','{phoneInput}');")
			mydb.commit()
		except Exception as e:
			mydb.rollback()
			raise e
		test = getTableData('tbl_publisher')
		print(test)
	#Ask user for inputs one at a time
	#Insert it into the table

def update(tableName):
	inp = -1
	numRows = -1
	while inp != numRows + 1:
		table = getTableData(tableName)
		tIds = getIds(tableName)
		numRows = len(table)
		print(f"Please select a row in {tableName} to update:")
		for i in range(0,numRows):
			print(f"{i+1}) {table[i]}")
		print(f"{numRows+1}) To quit to previous menu")
		inp = input(f"Please enter a number between 1 and {numRows+1}: ")
		if check.validInput(inp, 1, numRows + 1):
			#Grab specific row based on selection
			inp = int(inp)
			if inp != numRows + 1:
				row = table[inp-1]
				print("You selected:", row)
				#Gonna have to do specific update based on table
				if tableName == 'tbl_publisher':
					print("Here is the current name:", row[1])
					nameInput = input("What would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
					if nameInput in ('N/A', 'n/a', 'NA', 'na'):
						nameInput = row[1]
					print("Here is the current address:", row[2])
					addrInput = input("What would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
					if addrInput in ('N/A', 'n/a', 'NA', 'na'):
						addrInput = row[2]
					print("Here is the phone number:", row[3])
					phoneInput = input("What would you like to change it to?(Limit to 45 characters), Type 'N/A' if you do not wish to change:\n")
					if phoneInput in ('N/A', 'n/a', 'NA', 'na'):
						phoneInput = row[3]
					#Reflect inputs in the database
					pubId = tIds[inp-1]
					try:
						mycursor.execute(f"UPDATE tbl_publisher SET publisherName = '{nameInput}', publisherAddress = '{addrInput}', publisherPhone = '{phoneInput}' WHERE publisherId = {pubId};")
						mydb.commit()
					except Exception as e:
						mydb.rollback()
						raise e
					test = getTableData('tbl_publisher')
					print(test)
			else:
				print("Moving to previous page...")				

		#List entire table
		#Take selection of row to edit
		#Go through items and update them, N/A if nothing

def delete(tableName):
	inp = -1
	numRows = -1
	while inp != numRows + 1:
		table = getTableData(tableName)
		tIds = getIds(tableName)
		numRows = len(table)
		print(f"Please select a row in {tableName} to delete:")
		for i in range(0,numRows):
			print(f"{i+1}) {table[i]}")
		print(f"{numRows+1}) To quit to previous menu")
		inp = input(f"Please enter a number between 1 and {numRows+1}: ")
		if check.validInput(inp, 1, numRows + 1):
			#Grab specific row based on selection
			inp = int(inp)
			if inp != numRows + 1:
				row = table[inp-1]
				print("You selected:", row)
				#Gonna have to do specific delete based on table
				if tableName == 'tbl_publisher':
					#Delete the chosen row from the database
					pubId = tIds[inp-1]
					try:
						mycursor.execute(f"DELETE FROM tbl_publisher WHERE publisherId = {pubId};")
						mydb.commit()
					except Exception as e:
						mydb.rollback()
						raise e
					test = getTableData('tbl_publisher')
					print(test)
		else:
			print("Moving to previous page...")	
	#List entire table
	#Take selection of row to delete
	#Delete the row from the table(s)

def addBookAuthor():
	print("This will take more logic than the other tables to ADD")

def updateBookAuthor():
	print("This will take more logic than the other tables to UPDATE")

def deleteBookAuthor():
	print("This will take more logic than the other tables to DELETE")

def overrideDueDate():
	print("Please select loan that you would like to override due date of:\n")
	#List tbl_book_loans
	#Update dueDate based on bookId, branchId, and cardNo
	#Maybe list names of books branches and loans if we have time
