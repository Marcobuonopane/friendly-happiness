#!/usr/bin/env python3
"""
🌐 AUTENTICO - Server Web per Pubblicazione One-Click
Interfaccia web semplice per pubblicare AUTENTICO con un click
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import subprocess
import threading
import os
import sys
from urllib.parse import urlparse, parse_qs
import time

class AutomationHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Imposta la directory di lavoro sui file web
        os.chdir('/home/user/webapp/one_click_automation/web')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Gestisce richieste GET"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/':
            # Serve la pagina principale
            self.serve_main_page()
        elif parsed_url.path == '/status':
            # API per stato pubblicazione
            self.serve_status()
        elif parsed_url.path == '/start_publication':
            # Avvia pubblicazione automatica
            self.start_publication()
        else:
            # Serve file statici
            super().do_GET()
    
    def serve_main_page(self):
        """Serve la pagina HTML principale"""
        try:
            with open('index.html', 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "Pagina non trovata")
    
    def serve_status(self):
        """API per controllare lo stato della pubblicazione"""
        try:
            # Legge stato da file temporaneo
            if os.path.exists('/tmp/autentico_status.json'):
                with open('/tmp/autentico_status.json', 'r') as f:
                    status = json.load(f)
            else:
                status = {
                    'current_step': 0,
                    'progress': 0,
                    'message': 'Sistema pronto',
                    'success': False,
                    'tracking_id': None
                }
            
            response = json.dumps(status, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(response.encode())))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode())
            
        except Exception as e:
            error_response = json.dumps({
                'error': str(e),
                'message': 'Errore lettura stato'
            }, ensure_ascii=False)
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_response.encode())
    
    def start_publication(self):
        """Avvia il processo di pubblicazione automatica"""
        try:
            # Pulisce lo stato precedente
            if os.path.exists('/tmp/autentico_status.json'):
                os.remove('/tmp/autentico_status.json')
            
            # Avvia script di automazione in background
            script_path = '/home/user/webapp/one_click_automation/scripts/play_store_automation.py'
            
            def run_automation():
                try:
                    subprocess.run([
                        sys.executable, script_path, '--auto'
                    ], cwd='/home/user/webapp')
                except Exception as e:
                    # Salva errore nello stato
                    error_status = {
                        'current_step': 0,
                        'progress': 0,
                        'message': f'Errore: {str(e)}',
                        'success': False,
                        'tracking_id': None
                    }
                    with open('/tmp/autentico_status.json', 'w') as f:
                        json.dump(error_status, f)
            
            # Esegue in thread separato per non bloccare il server
            threading.Thread(target=run_automation, daemon=True).start()
            
            response = json.dumps({
                'success': True,
                'message': 'Pubblicazione automatica avviata!'
            }, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode())
            
        except Exception as e:
            error_response = json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_response.encode())
    
    def log_message(self, format, *args):
        """Log personalizzato per il server"""
        print(f"🌐 [{time.strftime('%H:%M:%S')}] {format % args}")

def start_server(port=8000):
    """Avvia il server web"""
    print("🚀 AUTENTICO - Server Pubblicazione One-Click")
    print("🏆 Marco Buonopane (Creatore) + Massimiliano Cardinali (Design)")
    print("🤖 Powered by AI Assistant")
    print("=" * 60)
    
    # Verifica che i file necessari esistano
    web_dir = '/home/user/webapp/one_click_automation/web'
    if not os.path.exists(os.path.join(web_dir, 'index.html')):
        print("❌ ERRORE: File index.html non trovato!")
        return False
    
    script_dir = '/home/user/webapp/one_click_automation/scripts'
    if not os.path.exists(os.path.join(script_dir, 'play_store_automation.py')):
        print("❌ ERRORE: Script automazione non trovato!")
        return False
    
    try:
        # Crea server HTTP
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, AutomationHandler)
        
        print(f"✅ Server avviato su http://0.0.0.0:{port}")
        print(f"📱 Accedi da browser per pubblicare AUTENTICO con un click!")
        print(f"🔗 URL locale: http://localhost:{port}")
        print()
        print("🎯 Funzioni disponibili:")
        print("   / - Interfaccia principale con pulsante magico")
        print("   /status - API stato pubblicazione")
        print("   /start_publication - Avvia pubblicazione automatica")
        print()
        print("Premi Ctrl+C per fermare il server")
        print("=" * 60)
        
        # Avvia server
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server fermato dall'utente")
        return True
    except Exception as e:
        print(f"❌ ERRORE server: {e}")
        return False

def main():
    """Funzione principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Server web per pubblicazione automatica AUTENTICO')
    parser.add_argument('--port', type=int, default=8000, help='Porta del server (default: 8000)')
    
    args = parser.parse_args()
    
    success = start_server(args.port)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()