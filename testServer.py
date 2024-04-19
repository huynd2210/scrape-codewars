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


import requests

def isKataApproved(challenge_id_or_slug):
    # API endpoint URL
    api_url = f"https://www.codewars.com/api/v1/code-challenges/{challenge_id_or_slug}"

    # Send GET request
    response = requests.get(api_url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Check if the challenge is approved
        if 'approvedBy' in data:
            return True
        else:
            return False
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")



if __name__ == "__main__":
    # run()

    # Example usage:
    challenge_id_or_slug = "65f3fad050b1045394b71836"
    approved_by = isKataApproved(challenge_id_or_slug)
    print("Approved By:", approved_by)
