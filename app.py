from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# بيانات أفلام تجريبية
movies = [
    {"id": 1, "title": "Inception", "rating": 8.8, "genre": ["Action", "Sci-Fi"], "year": 2010},
    {"id": 2, "title": "Interstellar", "rating": 8.6, "genre": ["Adventure", "Drama"], "year": 2014},
    {"id": 3, "title": "The Dark Knight", "rating": 9.0, "genre": ["Action", "Crime"], "year": 2008}
]

class MovieAPI(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/movies":
            self._send_json({"movies": movies})
        elif path == "/api/details":
            params = parse_qs(parsed.query)
            movie_id = int(params.get("id", [0])[0])
            movie = next((m for m in movies if m["id"] == movie_id), None)
            if movie:
                self._send_json(movie)
            else:
                self._send_json({"error": "Movie not found"}, 404)
        else:
            self._send_json({
                "message": "🎬 Welcome to Movies API",
                "routes": ["/api/movies", "/api/details?id=1"]
            })

def run(server_class=HTTPServer, handler_class=MovieAPI):
    port = 8000
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 Movies API running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
