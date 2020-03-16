use library;

set foreign_key_checks=0;  # Remove foreign key checks
ALTER TABLE tbl_book MODIFY bookId INTEGER NOT NULL AUTO_INCREMENT;
ALTER TABLE tbl_publisher MODIFY publisherId INTEGER NOT NULL AUTO_INCREMENT;
ALTER TABLE tbl_genre MODIFY genre_id INTEGER NOT NULL AUTO_INCREMENT;
ALTER TABLE tbl_author MODIFY authorId INTEGER NOT NULL AUTO_INCREMENT;
ALTER TABLE tbl_library_branch MODIFY branchId INTEGER NOT NULL AUTO_INCREMENT;
ALTER TABLE tbl_borrower MODIFY cardNo INTEGER NOT NULL AUTO_INCREMENT;
# Adds foreign key checks back
set foreign_key_checks=1;

# INSERT PUBLISHERS
INSERT INTO tbl_publisher (publisherID, publisherName, publisherAddress, publisherPhone) VALUES (1, 'Book Guys', '123 Fake St, Indiana', '555-333-2222');
INSERT INTO tbl_publisher (publisherID, publisherName, publisherAddress, publisherPhone) VALUES (2, 'Book Makers', '321 Some St, Iowa', '999-777-8888');
INSERT INTO tbl_publisher (publisherID, publisherName, publisherAddress, publisherPhone) VALUES (3, 'We Make Books', '444 Totally Real St, Florida', '101-010-1010');

# INSERT BORROWERS
INSERT INTO tbl_borrower (name, address) VALUES ('Tom Jerry', '987 Some Place, Kansas');
INSERT INTO tbl_borrower (name, address) VALUES ('Jerry Lee Lewis', 'New York, New York');
INSERT INTO tbl_borrower (name, address) VALUES ('Mickey Mouse', '1928 Disneyland, California');

# INSERT LIBRARY BRANCHES
INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('University Library', 'Boston, MA');
INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('State Liberty', 'New York, NY');
INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('Federal Library', 'Washington, DC');
INSERT INTO tbl_library_branch (branchName, branchAddress) VALUES ('County Library', 'McLean, VA');

# INSERT AUTHORS
INSERT INTO tbl_author (authorName) VALUES ('Stephen King');
INSERT INTO tbl_author (authorName) VALUES ('Sidney Sheldon');
INSERT INTO tbl_author (authorName) VALUES ('Mark Penn');
INSERT INTO tbl_author (authorName) VALUES ('Sun Tzu');
INSERT INTO tbl_author (authorName) VALUES ('Joseph Schmo');

# INSERT BOOKS
INSERT INTO tbl_book (title, pubId) VALUES ('Lost Tribe', 1);
INSERT INTO tbl_book (title, pubId) VALUES ('The Haunting', 2);
INSERT INTO tbl_book (title, pubId) VALUES ('Microtrends', 3);
INSERT INTO tbl_book (title, pubId) VALUES ('Intro to Biology', 1);
INSERT INTO tbl_book (title, pubId) VALUES ('The Art of War', 2);
INSERT INTO tbl_book (title, pubId) VALUES ('Macrotrends', 3);

# INSERT BOOK-AUTHORS
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (1, 2);
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (2, 1);
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (3, 3);
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (4, 5);
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (5, 4);
INSERT INTO tbl_book_authors (bookId, authorId) VALUES (6, 3);

# INSERT BOOK-COPIES
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (1, 1, 10);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (2, 1, 15);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (3, 1, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (4, 1, 10);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (5, 1, 17);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (6, 1, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (1, 2, 0);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (2, 2, 1);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (3, 2, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (4, 2, 10);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (5, 2, 2);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (6, 2, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (1, 3, 7);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (2, 3, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (3, 3, 4);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (4, 3, 10);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (5, 3, 0);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (6, 3, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (1, 4, 6);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (2, 4, 1);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (3, 4, 5);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (4, 4, 8);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (5, 4, 9);
INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies) VALUES (6, 4, 5);

# INSERT BOOK-COPIES
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (1, 1, 1, '2020-03-10', '2020-03-17');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (2, 2, 2, '2020-03-12', '2020-03-19');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (3, 3, 3, '2020-03-09', '2020-03-16');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (6, 1, 1, '2020-03-15', '2020-03-22');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (4, 2, 2, '2020-03-15', '2020-03-22');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (3, 1, 1, '2020-03-14', '2020-03-21');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (2, 1, 1, '2020-03-12', '2020-03-19');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (6, 4, 2, '2020-03-11', '2020-03-18');
INSERT INTO tbl_book_loans (bookId, branchId, cardNo, dateOut, dueDate) VALUES (4, 1, 1, '2020-03-10', '2020-03-17');