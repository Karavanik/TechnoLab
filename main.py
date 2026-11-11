from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import os
import webbrowser

# pliki zawsze z folderu, w którym leży main.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = parse_qs(self.rfile.read(length).decode())

        if data["email"][0] == "serwis@gmail.com" and data["haslo"][0] == "1234":
            strona = "/serwis.html"
        else:
            strona = "/index.html"

        self.send_response(303)
        self.send_header("Location", strona)
        self.end_headers()


# automatycznie otwiera stronę główną w przeglądarce
webbrowser.open("http://localhost:8080/index.html")
HTTPServer(("localhost", 8080), Handler).serve_forever()