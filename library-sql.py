# In terminal:
# virtualenv ENVIRONMENTNAMEHERE
# pip install mysql-connector-python
# source ENVIRONMENTNAMEHERE/Scripts/activate

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="library"
)

mycursor = mydb.cursor()

def alter(state,msg):
    result = mycursor.execute(state,multi=True)
    result.send(None)
    print(msg,result)

# MODIFY PRIMARY KEYS TO AUTO INCREMENT
try:
    alter("set foreign_key_checks=0;","done") # Remove foreign key checks
    alter("ALTER TABLE tbl_book MODIFY bookId INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("ALTER TABLE tbl_publisher MODIFY publisherId INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("ALTER TABLE tbl_genre MODIFY genre_id INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("ALTER TABLE tbl_author MODIFY authorId INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("ALTER TABLE tbl_library_branch MODIFY branchId INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("ALTER TABLE tbl_borrower MODIFY cardNo INTEGER NOT NULL AUTO_INCREMENT","done")
    alter("set foreign_key_checks=1;","done") # Adds foreign key checks back
    mydb.commit()
except Exception as e:
    mydb.rollback() #undo all above changes if any errors
    raise e

try:
    # INSERT LIBRARY BRANCHES
    alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('University Library', 'Boston')","done")
    alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('State Liberty', 'New York')","done")
    alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('Federal Library', 'Washington, DC')","done")
    alter("INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('County Library', 'McLean, VA')","done")

    # INSERT AUTHORS
    alter("INSERT INTO tbl_author (authorName) VALUES ('Stephen King')","done")
    alter("INSERT INTO tbl_author (authorName) VALUES ('Sidney Sheldon')","done")
    alter("INSERT INTO tbl_author (authorName) VALUES ('Mark Penn')","done")

    # INSERT BOOKS
    alter("INSERT INTO tbl_book (title) VALUES ('Lost Tribe')","done")
    alter("INSERT INTO tbl_book (title) VALUES ('The Haunting')","done")
    alter("INSERT INTO tbl_book (title) VALUES ('Microtrends')","done")

    # INSERT BOOK-AUTHORS
    alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (1, 2)","done")
    alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (2, 1)","done")
    alter("INSERT INTO tbl_book_authors (bookId, authorId) VALUES (3, 3)","done")
    mydb.commit()
except Exception as e:
    mydb.rollback()
    raise e

# SELECTS ALL THEN STORE RESULTS
mycursor.execute("SELECT * FROM tbl_library_branch")
branches = mycursor.fetchall()

mycursor.execute("SELECT * FROM tbl_author")
authors = mycursor.fetchall()

mycursor.execute("SELECT * FROM tbl_book")
books = mycursor.fetchall()

mycursor.execute("SELECT * FROM tbl_book_authors")
bookAuthors = mycursor.fetchall()

# PRINT RESULTS
for branch in branches:
  print(branch)

for author in authors:
  print(author)

for book in books:
  print(book)

for bookAuthor in bookAuthors:
  print(bookAuthor)

# mycursor.execute("UPDATE tbl_book SET title = 'The Test Title' WHERE bookId = 2")
# mydb.commit()