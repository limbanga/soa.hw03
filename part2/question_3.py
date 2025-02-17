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