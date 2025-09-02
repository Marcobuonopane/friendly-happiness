#!/usr/bin/env python3
"""
AUTENTICO v2.2 - Server di Anteprima Integrato
Serve sia l'anteprima che l'applicazione principale con routing intelligente
"""

import http.server
import socketserver
import os
import urllib.parse
import json
from pathlib import Path

class AutenticoPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/home/user/webapp", **kwargs)
    
    def do_GET(self):
        # Parse dell'URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Routing intelligente
        if path == '/' or path == '/preview' or path == '/preview.html':
            # Serve l'anteprima
            self.serve_file('/home/user/webapp/preview.html')
        elif path == '/app' or path == '/app.html':
            # Serve l'applicazione principale
            self.serve_file('/home/user/webapp/src/index.html')
        elif path.startswith('/src/'):
            # Serve file dalla directory src
            file_path = '/home/user/webapp' + path
            self.serve_file(file_path)
        elif path.startswith('/assets/'):
            # Serve asset
            file_path = '/home/user/webapp' + path
            self.serve_file(file_path)
        elif path.startswith('/scripts/'):
            # Serve script
            file_path = '/home/user/webapp' + path
            self.serve_file(file_path)
        elif path == '/api/status':
            # API endpoint per status
            self.serve_api_status()
        elif path == '/api/info':
            # API endpoint per info app
            self.serve_api_info()
        else:
            # Default: prova a servire il file richiesto
            try:
                super().do_GET()
            except Exception as e:
                # Se fallisce, serve l'anteprima come fallback
                print(f"Errore servendo {path}: {e}")
                self.serve_file('/home/user/webapp/preview.html')
    
    def serve_file(self, file_path):
        """Serve un file specifico"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Determina il content type
                if file_path.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript; charset=utf-8'
                elif file_path.endswith('.css'):
                    content_type = 'text/css; charset=utf-8'
                elif file_path.endswith('.json'):
                    content_type = 'application/json; charset=utf-8'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif file_path.endswith('.ico'):
                    content_type = 'image/x-icon'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-length', len(content))
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, f'File non trovato: {file_path}')
        except Exception as e:
            print(f"Errore servendo file {file_path}: {e}")
            self.send_error(500, f'Errore interno: {str(e)}')
    
    def serve_api_status(self):
        """Serve lo status dell'applicazione"""
        status_data = {
            "status": "online",
            "version": "2.2.0",
            "app_name": "AUTENTICO",
            "features": [
                "AES-256 Encryption",
                "Biometric Authentication",
                "Digital Certificates",
                "PWA Support",
                "Multi-language"
            ],
            "endpoints": {
                "/": "Homepage/Anteprima",
                "/preview": "Anteprima Documentazione", 
                "/app": "Applicazione Principale",
                "/src/index.html": "App Direct Access",
                "/api/status": "API Status",
                "/api/info": "App Info"
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status_data, indent=2).encode('utf-8'))
    
    def serve_api_info(self):
        """Serve informazioni dettagliate sull'app"""
        info_data = {
            "app": "AUTENTICO v2.2",
            "description": "Sistema di Certificazione Digitale Avanzato",
            "author": "Marco Buonopane",
            "designer": "Massimiliano Cardinali",
            "technology_stack": {
                "frontend": ["HTML5", "CSS3", "JavaScript ES6+"],
                "security": ["AES-256", "SHA-256", "WebAuthn"],
                "apis": ["Web Crypto API", "Geolocation API", "Service Workers"],
                "mobile": ["PWA", "Capacitor", "Android/iOS"]
            },
            "features": {
                "security": {
                    "encryption": "AES-256-GCM",
                    "hashing": "SHA-256", 
                    "authentication": "WebAuthn Biometric",
                    "storage": "Encrypted LocalStorage"
                },
                "certificates": {
                    "digital_signing": "Cryptographic Hash",
                    "gps_location": "Precise Geolocation",
                    "timestamps": "Millisecond Precision",
                    "export": "PDF Generation"
                },
                "vault": {
                    "file_encryption": "AES-256",
                    "upload": "Multiple Files",
                    "download": "Secure Decryption",
                    "management": "Version Control"
                }
            },
            "deployment": {
                "platforms": ["Web PWA", "Android", "iOS", "Desktop"],
                "automation": "Fastlane + GitHub Actions",
                "monitoring": "Play Store API",
                "distribution": "Multi-track Release"
            },
            "stats": {
                "lines_of_code": "2847+",
                "features_count": "25+",
                "languages_supported": 13,
                "security_level": "Military Grade"
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(info_data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override per logging personalizzato"""
        timestamp = self.log_date_time_string()
        print(f"[{timestamp}] {format % args}")

def run_preview_server(port=3000):
    """Avvia il server di anteprima"""
    print(f"""
    ╔══════════════════════════════════════════╗
    ║         AUTENTICO v2.2 PREVIEW          ║
    ║      Server di Anteprima Integrato      ║
    ╚══════════════════════════════════════════╝
    
    🌐 Server attivo su: http://localhost:{port}
    
    📋 Endpoints disponibili:
    ├── /                    → Anteprima e Documentazione
    ├── /preview            → Anteprima Completa  
    ├── /app                → Applicazione AUTENTICO
    ├── /src/index.html     → App Diretta
    ├── /api/status         → Status API
    └── /api/info           → Informazioni App
    
    🚀 Funzionalità:
    ├── ✅ Routing intelligente
    ├── ✅ Serving file statici
    ├── ✅ API endpoints
    ├── ✅ CORS enabled
    └── ✅ Error handling
    
    📱 Testa l'app:
    ├── Demo Live integrata
    ├── Funzionalità complete
    ├── Crittografia reale
    └── Autenticazione biometrica
    
    Press Ctrl+C per fermare il server
    """)
    
    try:
        with socketserver.TCPServer(("", port), AutenticoPreviewHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server fermato dall'utente")
    except Exception as e:
        print(f"❌ Errore server: {e}")

if __name__ == "__main__":
    import sys
    
    # Porta dal parametro o default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    
    # Verifica directory di lavoro
    os.chdir("/home/user/webapp")
    
    run_preview_server(port)