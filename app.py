import json, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _set_body(self, dict_content):
        self.wfile.write(bytes(json.dumps(dict_content), encoding='UTF-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        temperature = subprocess.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\\.[0-9]*'")
        self._set_body({'temperature': float(temperature)})


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8010):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port} 🚀")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
