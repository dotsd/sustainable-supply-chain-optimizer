#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import socket

PORT = int(os.getenv("UI_PORT", "8004"))

def find_free_port(preferred: int) -> int:
    try:
        with socketserver.TCPServer(("", preferred), None):
            return preferred
    except Exception:
        s = socket.socket()
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/aws_supply_chain_demo.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    PORT = find_free_port(PORT)
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"AWS Supply Chain Optimizer UI running at:")
        print(f"http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        
        webbrowser.open(f'http://localhost:{PORT}')
        httpd.serve_forever()