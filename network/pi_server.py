import http.server
import socketserver
import json
import time
import threading

COORDINATES_BUFFER = []

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/coordinates':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response_data = json.dumps(COORDINATES_BUFFER)
            self.wfile.write(response_data.encode("utf-8"))
            COORDINATES_BUFFER.clear()
        else:
            self.send_error(404, "Not Found")

def run_server(host="localhost", port=4242):
    with socketserver.TCPServer((host, port), MyRequestHandler) as httpd:
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()

def run_server_threaded(host="localhost", port=4242):
    server_thread = threading.Thread(target=run_server, args=(host, port), daemon=True)
    server_thread.start()


if __name__ == '__main__':
    run_server_threaded(host="0.0.0.0")
    while True:
        COORDINATES_BUFFER.append((time.time(), time.time(), time.time()))
        time.sleep(1)
