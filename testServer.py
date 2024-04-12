from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set the response headers to allow CORS
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = json.loads(post_data.decode('utf-8'))

        print("Received data:", parsed_data)
        self.wfile.write(b"Data received and processed successfully.")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8099):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
