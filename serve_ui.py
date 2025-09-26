#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

PORT = 8001

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/aws_supply_chain_demo.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"AWS Supply Chain Optimizer UI running at:")
        print(f"http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        
        webbrowser.open(f'http://localhost:{PORT}')
        httpd.serve_forever()