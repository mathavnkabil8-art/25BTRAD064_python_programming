class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True
 
    def issue_book(self):
        if self.is_available:
            self.is_available = False
            print(f'"{self.title}" has been issued.')
        else:
            print(f'"{self.title}" is currently unavailable.')
 
    def return_book(self):
        if not self.is_available:
            self.is_available = True
            print(f'"{self.title}" has been returned.')
        else:
            print(f'"{self.title}" was not issued.')
 
    def display_status(self):
        status = "Available" if self.is_available else "Issued"
        print(f"Title: {self.title} | Author: {self.author} | Status: {status}")
 
 
class ReferenceBook(Book):
    def display_status(self):
        super().display_status()
        print("Note: Reference books should be used in the library.")
 
 
def main():
    book1 = Book("Python Programming", "John Smith")
    book2 = ReferenceBook("Computer Fundamentals", "A. Kumar")
 
    book1.display_status()
    book1.issue_book()
    book1.display_status()
    book1.issue_book()
    book1.return_book()
    book1.display_status()
    book2.display_status()
 
 
if __name__ == "__main__":
    main()
