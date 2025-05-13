from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from books_data import get_all_books, get_book_by_id, add_book

class BookRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        if self.path == "/books":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_all_books()).encode())
        elif len(path_parts) == 2 and path_parts[0] == "books":
            try:
                book_id = int(path_parts[1])
                book = get_book_by_id(book_id)
                if book:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(book).encode())
                else:
                    self.send_error(404, "Book not found")
            except ValueError:
                self.send_error(400, "Invalid ID")
        else:
            self.send_error(404, "Route not found")

    def do_POST(self):
        if self.path == "/books":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                new_book = add_book(data["title"], data["author"])
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(new_book).encode())
            except (KeyError, json.JSONDecodeError):
                self.send_error(400, "Invalid JSON or missing fields")

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, BookRequestHandler)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
