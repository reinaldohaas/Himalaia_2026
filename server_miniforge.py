import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "C:/Users/haas/github/Himalaia_2026"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run_server():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"================================================================")
        print(f"  SERVIDOR MINIFORGE PYTHON INICIADO COM SUCESSO NA PORTA {PORT}!")
        print(f"  Ambiente: C:\\Users\\haas\\miniforge3\\python.exe")
        print(f"  Visualizador 4D: http://localhost:{PORT}/viewer_4d.html")
        print(f"  Infográfico:    http://localhost:{PORT}/index.html")
        print(f"================================================================")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
