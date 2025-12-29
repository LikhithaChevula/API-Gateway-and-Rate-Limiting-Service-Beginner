from http.server import BaseHTTPRequestHandler, HTTPServer
from rate_limiter import RateLimiter

rate_limiter = RateLimiter(limit=3, window=10)

class GatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        user_ip = self.client_address[0]

        if not rate_limiter.allow_request(user_ip):
            self.send_response(429)
            self.end_headers()
            self.wfile.write(b"Too Many Requests")
            return

        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Welcome to API Gateway")
        elif self.path == "/hello":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello from Service")
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server = HTTPServer(("localhost", 8080), GatewayHandler)
    print("API Gateway running at http://localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()
