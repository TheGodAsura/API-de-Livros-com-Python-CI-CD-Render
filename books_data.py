books = [
    { "id": 1, "title": "1984", "author": "George Orwell" },
    { "id": 2, "title": "Brave New World", "author": "Aldous Huxley" }
]

def get_all_books():
    return books

def get_book_by_id(book_id):
    return next((book for book in books if book["id"] == book_id), None)

def add_book(title, author):
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = { "id": new_id, "title": title, "author": author }
    books.append(new_book)
    return new_book
