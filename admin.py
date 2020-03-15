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
		stmt = f"Insert into tbl_publisher values (NULL,'{nameInput}','{addrInput}','{phoneInput}');"
	elif tableName == 'tbl_library_branch':
		print("\nPlease limit input to 45 characters.")
		nameInput = input("What would you like to name the library branch(type 'quit' to quit)?:\n")
		if nameInput == 'quit':
			return
		print("\nPlease limit input to 45 characters.")
		addrInput = input("What is the address of the library branch(type 'quit' to quit)?:\n")
		if addrInput == 'quit':
			return
		stmt = f"Insert into tbl_library_branch values (NULL,'{nameInput}','{addrInput}');"

	elif tableName == 'tbl_borrower':	
		#Either can auto increment card number or enter it manually
		#If manual, will need to do some value checking		
		#print("Please limit input to 45 characters.")
		#cardInput = input("What should the card number be(type 'quit' to quit)?:\n")
		#if cardInput == 'quit':
		#	return
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
		stmt = f"Insert into tbl_borrower values (NULL,'{nameInput}','{addrInput}','{phoneInput}');"

	try:
		mycursor.execute(stmt)
		mydb.commit()
	except Exception as e:
		mydb.rollback()
		raise e


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
					stmt = f"UPDATE tbl_publisher SET publisherName = '{nameInput}', publisherAddress = '{addrInput}', publisherPhone = '{phoneInput}' WHERE publisherId = {pKey};"
				elif tableName == 'tbl_library_branch':
					stmt = f"UPDATE tbl_library_branch SET branchName = '{nameInput}', branchAddress = '{addrInput}' WHERE branchId = {pKey};"
				elif tableName == 'tbl_borrower':
					stmt = f"UPDATE tbl_borrower SET name = '{nameInput}', address = '{addrInput}', phone = '{phoneInput}' WHERE cardNo = {pKey};"
				
				#Send SQL statements to the database
				try:
					mycursor.execute(stmt)
					mydb.commit()
				except Exception as e:
					mydb.rollback()
					raise e
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
						stmt = f"DELETE FROM tbl_publisher WHERE publisherId = {pKey};"
					elif tableName == 'tbl_library_branch':
						#Delete the chosen row from the database
						stmt = f"DELETE FROM tbl_library_branch WHERE branchId = {pKey};"
					elif tableName == 'tbl_borrower':
						#Delete the chosen row from the database
						stmt = f"DELETE FROM tbl_borrower WHERE cardNo = {pKey};"
					#Send SQL statement to the database
					try:
						mycursor.execute(stmt)
						mydb.commit()
					except Exception as e:
						mydb.rollback()
						raise e
		else:
			print("\nMoving to previous page...")	
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
	inp = -1
	numBors = -1 
	while inp != numBors + 1:
		#Get borrower data from database
		borrowers = getTableData('tbl_borrower')
		numBors = len(borrowers)
		cardNums = getIds('tbl_borrower')
		print(f"\nPlease select a borrower to override due date of:\n")
		for i in range(0,numBors):
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
				try:
					mycursor.execute(f"SELECT * FROM tbl_book_loans WHERE cardNo = {cardNum}")
					borLoans = mycursor.fetchall()
					loanCount = len(borLoans)
				except Exception as e:
					raise e
 
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
						try:
							mycursor.execute(f"SELECT * FROM tbl_book_loans WHERE cardNo = {cardNum}")
							borLoans = mycursor.fetchall()
						except Exception as e:
							raise e
						#Print options to user
						for i in range(0, loanCount):
							print(f"{i+1}) {borLoans[i]}")
						print(f"{loanCount+1}) To quit to previous menu")
						loanInp = input(f"\nPlease enter a number between 1 and {loanCount+1}: ")
						if check.validInput(loanInp, 1, loanCount + 1):
							#Grab specific row based on selection
							loanInp = int(loanInp)
							if loanInp != loanCount + 1:
								print(f"borLoans:{borLoans}")
								loan = borLoans[loanInp-1]
								#Show user current due date
								#**Maybe clean up how the date is displayed
								print(f"\nThis borrower has a due date of: {loan[4]}")
								#User inputs date or quits
								newDate = input("Please input new date (yyyy-mm-dd), enter 'quit' if no change:\n")
								print(f"\nnewDate:{newDate}\n")
								print(f"\nloan:{loan}\n")
								
								if newDate in ('quit', 'QUIT', 'Quit', 'Q', 'q'):
									print("\nMoving to previous menu ...")
								else:
									#**Could use a decent date format validation
									try:
										mycursor.execute(f"UPDATE tbl_book_loans SET dueDate = '{newDate}' WHERE bookId = {loan[0]} AND branchId = {loan[1]} AND cardNo = {loan[2]};")
										mydb.commit()
									except Exception as e:
										mydb.rollback()
										raise e
							else:
								print("\nMoving to previous page ...")
		else:
			print("Moving to previous page ...")
