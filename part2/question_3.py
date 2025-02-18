class Book:
    def __init__(self, title: str, author: str, pages: int):
        """Initialize the Book with title, author, and number of pages."""
        self.title = title
        self.author = author
        self.pages = pages

    def get_book_info(self) -> str:
        """Return a formatted string containing the title and author."""
        return f"Title: {self.title}, Author: {self.author}"

    def is_long(self) -> bool:
        """Return True if the book has more than 300 pages."""
        return self.pages > 300

# Example usage:
book1 = Book("Harry Potter", "J.K. Rowling", 500)
book2 = Book("Python Programming", "John Doe", 150)

print(book1.get_book_info())  # Output: Title: Harry Potter, Author: J.K. Rowling
print(book2.get_book_info())  # Output: Title: Python Programming, Author: John Doe

print(book1.is_long())  # Output: True
print(book2.is_long())  # Output: False