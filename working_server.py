#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/aws_supply_chain_demo.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"AWS Supply Chain Optimizer running at:")
        print(f"http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        
        # Auto-open browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        httpd.serve_forever()