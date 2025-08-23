#!/usr/bin/env python3
"""
AUTENTICO v2.2 - Server di Distribuzione Istantanea
Server HTTP per servire l'app PWA di Marco Buonopane
"""

import http.server
import socketserver
import os
import mimetypes
import json
from urllib.parse import urlparse
import sys

class AutenticoHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/home/user/webapp", **kwargs)
    
    def do_GET(self):
        # Gestione delle route personalizzate
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route principale - serve la pagina di download
        if path == '/' or path == '/download':
            self.path = '/INSTANT_APP_DEPLOY.html'
        
        # Route per l'app principale
        elif path == '/app' or path == '/autentico':
            self.path = '/src/index.html'
        
        # Route per la soluzione magica
        elif path == '/magic' or path == '/bypass':
            self.path = '/MAGIC_BYPASS_SOLUTION.html'
        
        # Route per il manifest PWA
        elif path == '/manifest.json':
            self.serve_manifest()
            return
        
        # Route per il service worker
        elif path == '/sw.js':
            self.path = '/sw.js'
        
        # Serve file statici normalmente
        try:
            super().do_GET()
        except Exception as e:
            self.send_error(500, f"Errore server: {str(e)}")
    
    def serve_manifest(self):
        """Serve il manifest.json con headers corretti"""
        try:
            with open('/home/user/webapp/manifest.json', 'r') as f:
                manifest_data = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(manifest_data.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Errore nel servire manifest: {str(e)}")
    
    def end_headers(self):
        # Aggiungi headers per PWA e sicurezza
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Headers per PWA
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-cache')
        elif self.path.endswith(('.js', '.css', '.png', '.jpg', '.ico')):
            self.send_header('Cache-Control', 'max-age=31536000')
        
        super().end_headers()
    
    def log_message(self, format, *args):
        """Log personalizzato"""
        message = format % args
        sys.stdout.write(f"[AUTENTICO v2.2] {self.log_date_time_string()} - {message}\n")
        sys.stdout.flush()

def main():
    PORT = 8001
    
    print("🚀 AUTENTICO v2.2 - Server di Distribuzione Istantanea")
    print(f"📡 Avvio server sulla porta {PORT}...")
    print(f"📁 Directory di lavoro: /home/user/webapp")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), AutenticoHandler) as httpd:
            print(f"✅ Server attivo su http://0.0.0.0:{PORT}")
            print(f"🌐 Pagina principale: http://0.0.0.0:{PORT}/")
            print(f"📱 App AUTENTICO: http://0.0.0.0:{PORT}/app")
            print(f"🎯 Soluzione Magica: http://0.0.0.0:{PORT}/magic")
            print("🔄 Premi Ctrl+C per fermare il server")
            
            sys.stdout.flush()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n⏹️  Server fermato dall'utente")
    except Exception as e:
        print(f"❌ Errore server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()