#Check for invalid input
def validInput(inp, beg, end):
	#Check if integer
	try:
		int(inp)
	except ValueError:
		print("\n-------------------------\nInvalid input. Try Again\n-------------------------\n")
		print("\nWrong data type, please stick to integers.\n")
		return False
	else:
		#Check if in range
		if int(inp) < beg:
			print("\n-------------------------\nInvalid input. Try Again\n-------------------------\n")
			print("\nYour input was too low.\n")
			return False
		elif int(inp) > end:
			print("\n-------------------------\nInvalid input. Try Again\n-------------------------\n")
			print("\nYour input was too high\n")
			return False
		else:
			return True