class Book_Info:
    def __init__(self, title, author, publication_year, ISBN_Number):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.ISBN_Number = ISBN_Number

class Library:
    def __init__(self):
        self.books = []
    def add_book(self):
        Book_Name = input("Enter the name of the book you want to add: ")
        Book_Author = input("Enter the author of the book: ")
        Book_Publication_Year = input("Enter the publication year of the book: ")
        Book_ISBN_Number = input("Enter the ISBN number of the book: ")
        new_book = Book_Info(Book_Name, Book_Author, Book_Publication_Year, Book_ISBN_Number)
        self.books.append(new_book)
        print(f"Book '{new_book.title}' by {new_book.author} added to the library.")
        print("--------Book Added Successfully--------")
        print(f"Total books in the library: {len(self.books)}")

    def display_books(self):
        if len(self.books) == 0:
            print("No books in the library.")
        else:
            for book in self.books:
                print(f"Title: {book.title}\n Author: {book.author}\n Publication Year: {book.publication_year} \n ISBN Number: {book.ISBN_Number}")
                print("*"*50)
    def update_book(self):
        
        if len(self.books) == 0:
            print("No books in the library to update.")
            return
        else:
            for book in self.books:
                ISBN_Number_To_Update = input("Enter the ISBN Number of the book you want to update: ")
                if ISBN_Number_To_Update == book.ISBN_Number:
                    while True:
                        print("="*50)
                        print("1. Update Title")
                        print("2. Update Author")
                        print("3. Update Publication Year")
                        print("4. Update ISBN Number")
                        print("="*50)
                        update_choice = int(input("Enter your choice (1/2/3/4/5): "))
                        print("="*50)
                        if update_choice == 1:
                            new_title = input("Enter the new title: ")
                            book.title = new_title
                            print(f"Title updated to '{book.title}'")
                        elif update_choice == 2:
                            new_author = input("Enter the new author: ")
                            book.author = new_author
                            print(f"Author updated to '{book.author}'")
                        elif update_choice == 3:
                            new_publication_year = input("Enter the new publication year: ")
                            book.publication_year = new_publication_year
                            print(f"Publication Year updated to '{book.publication_year}'")
                        elif update_choice == 4:
                            new_ISBN_Number = input("Enter the new ISBN number: ")
                            book.ISBN_Number = new_ISBN_Number
                            print(f"ISBN Number updated to '{book.ISBN_Number}'")
                            print("Invalid choice. Please try again.")
                        print("--------Book Updated Successfully--------")
                        print(f"Updated Book Details: \n Title: {book.title} \n Author: {book.author} \n Publication Year: {book.publication_year} \n ISBN Number: {book.ISBN_Number}")
                        print("*"*50)
                        print("1.Want To Update Attribute Of Same Book")
                        print("2.Want To Update Attribute Of Another Book")
                        print("0.Exit Update Menu")
                        update_another_choice = int(input("Enter your choice (0/1/2): "))
                        if update_another_choice == 1:
                            continue        
                        elif update_another_choice == 2:
                            break
                        elif update_another_choice == 0:
                            return 0
                            #break
                                #pass
    def delete_book(self):
        if len(self.books) == 0:
            print("No books in the library to delete.")
            return
        else:
            Book_Name_To_Delete = input("Enter the name of the book you want to delete: ")
            for book in self.books:
                if Book_Name_To_Delete == book.title:
                    self.books.remove(book)
                    print(f"Book '{book.title}' by {book.author} deleted from the library.")
                    print(f"Total books in the library: {len(self.books)}")
                    print("--------Book Deleted Successfully--------")
                    return
lms = Library()
while True:
    print("="*50)
    print(" "*10,"Library Management System")
    print("="*50)
    print("0. Exit")
    print("1. Add Book")
    print("2. Display Books")
    print("3.Update Books")
    print("4.Delete Books")
    print("="*50)
    choice = int(input("Enter your choice (0/1/2/3/4): "))
    print("="*50)
    if choice == 0:
        print("Exiting the program.")
        break
    elif choice == 1:
        lms.add_book()
    elif choice == 2:
        lms.display_books()
    elif choice == 3:
        lms.update_book()
    elif choice == 4:
        lms.delete_book()
    else:
        print("Invalid choice. Please try again.")