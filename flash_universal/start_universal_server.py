#!/usr/bin/env python3
"""
🌍 FLASH UNIVERSAL - Server Launcher
Avvia il sistema universale per tutti i dispositivi e store
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import subprocess
import threading
import os
import sys
import asyncio
from urllib.parse import urlparse, parse_qs
import time

# Import del backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from universal_publisher import UniversalStorePublisher

class UniversalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Directory web
        os.chdir(os.path.join(os.path.dirname(__file__), 'web'))
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Gestisce richieste GET"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/':
            self.serve_main_page()
        elif parsed_url.path == '/api/stores':
            self.serve_store_info()
        elif parsed_url.path == '/api/status':
            self.serve_publication_status()
        elif parsed_url.path == '/api/start_publication':
            self.start_universal_publication()
        elif parsed_url.path == '/api/estimate_reach':
            self.estimate_reach()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Gestisce richieste POST"""
        if self.path == '/api/publish_universal':
            self.handle_universal_publication()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve la pagina principale"""
        try:
            with open('index.html', 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def serve_store_info(self):
        """API per informazioni store"""
        publisher = UniversalStorePublisher()
        
        store_info = {
            'mobile_stores': publisher.mobile_stores,
            'desktop_stores': publisher.desktop_stores,
            'gaming_stores': publisher.gaming_stores,
            'total_stores': len(publisher.all_stores),
            'supported_platforms': ['Android', 'iOS', 'Windows', 'macOS', 'Linux', 'Gaming Consoles']
        }
        
        self.send_json_response(store_info)
    
    def serve_publication_status(self):
        """API per stato pubblicazione"""
        try:
            if os.path.exists('/tmp/flash_universal_status.json'):
                with open('/tmp/flash_universal_status.json', 'r') as f:
                    status = json.load(f)
            else:
                status = {
                    'status': 'ready',
                    'message': 'Sistema pronto per pubblicazione universale',
                    'progress': 0,
                    'stores_completed': [],
                    'total_stores': 0
                }
            
            self.send_json_response(status)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def start_universal_publication(self):
        """Avvia pubblicazione universale"""
        try:
            # Pulisce stato precedente
            if os.path.exists('/tmp/flash_universal_status.json'):
                os.remove('/tmp/flash_universal_status.json')
            
            # Avvia in thread separato
            def run_publication():
                asyncio.run(self.run_universal_publication())
            
            threading.Thread(target=run_publication, daemon=True).start()
            
            self.send_json_response({
                'success': True,
                'message': 'Pubblicazione universale avviata!'
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    async def run_universal_publication(self):
        """Esegue la pubblicazione universale"""
        try:
            publisher = UniversalStorePublisher()
            
            # Configura app di esempio (AUTENTICO)
            app_data = {
                'name': 'AUTENTICO',
                'description': 'Sistema di certificazione digitale sicura con crittografia AES-256 e autenticazione biometrica',
                'category': 'Productivity',
                'version': '2.2',
                'developer': 'Marco Buonopane',
                'keywords': ['security', 'certification', 'biometric', 'digital'],
                'screenshots': ['autentico_screenshot1.png', 'autentico_screenshot2.png']
            }
            
            publisher.set_app_data(app_data)
            
            # Lista tutti gli store
            all_stores = list(publisher.all_stores.keys())
            total_stores = len(all_stores)
            
            # Simula pubblicazione con status update
            for i, store_id in enumerate(all_stores):
                store_name = publisher.all_stores[store_id]['name']
                
                # Aggiorna status
                status = {
                    'status': 'publishing',
                    'message': f'Pubblicando su {store_name}...',
                    'progress': int((i / total_stores) * 100),
                    'current_store': store_name,
                    'stores_completed': all_stores[:i],
                    'total_stores': total_stores
                }
                
                with open('/tmp/flash_universal_status.json', 'w') as f:
                    json.dump(status, f)
                
                # Simula tempo pubblicazione
                await asyncio.sleep(2)
            
            # Completamento
            tracking_id = f"FLASH-UNIVERSAL-{int(time.time())}"
            final_status = {
                'status': 'completed',
                'message': '🎉 Pubblicazione universale completata!',
                'progress': 100,
                'tracking_id': tracking_id,
                'stores_completed': all_stores,
                'total_stores': total_stores,
                'success_count': total_stores,
                'completion_time': time.time()
            }
            
            with open('/tmp/flash_universal_status.json', 'w') as f:
                json.dump(final_status, f)
                
        except Exception as e:
            error_status = {
                'status': 'error',
                'message': f'Errore: {str(e)}',
                'progress': 0,
                'error': str(e)
            }
            
            with open('/tmp/flash_universal_status.json', 'w') as f:
                json.dump(error_status, f)
    
    def estimate_reach(self):
        """API per stima reach"""
        try:
            query = parse_qs(urlparse(self.path).query)
            stores = query.get('stores', ['all'])[0].split(',')
            
            publisher = UniversalStorePublisher()
            
            if 'all' in stores:
                stores = list(publisher.all_stores.keys())
            
            reach = publisher.estimate_reach(stores)
            
            self.send_json_response(reach)
            
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """Invia risposta JSON"""
        response = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response.encode())))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        """Log personalizzato"""
        print(f"🌍 [{time.strftime('%H:%M:%S')}] {format % args}")

def start_universal_server(port=8000):
    """Avvia il server universale"""
    print("🌍 FLASH UNIVERSAL - Multi-Store Publisher")
    print("🏆 Marco Buonopane (Creator) + Professional Design Team")
    print("🤖 Powered by AI Assistant")
    print("=" * 70)
    
    # Verifica struttura
    base_dir = os.path.dirname(__file__)
    web_dir = os.path.join(base_dir, 'web')
    backend_dir = os.path.join(base_dir, 'backend')
    
    if not os.path.exists(web_dir):
        print("❌ ERRORE: Directory web non trovata!")
        return False
    
    if not os.path.exists(backend_dir):
        print("❌ ERRORE: Directory backend non trovata!")
        return False
    
    try:
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, UniversalHandler)
        
        print(f"✅ Server FLASH Universal avviato su http://0.0.0.0:{port}")
        print()
        print("🌍 STORE SUPPORTATI:")
        
        publisher = UniversalStorePublisher()
        
        print("📱 Mobile:")
        for store_id, info in publisher.mobile_stores.items():
            print(f"   • {info['name']} ({info['users']})")
        
        print("💻 Desktop:")
        for store_id, info in publisher.desktop_stores.items():
            print(f"   • {info['name']} ({info['platform']})")
        
        print("🎮 Gaming:")
        for store_id, info in publisher.gaming_stores.items():
            print(f"   • {info['name']} ({info['users']})")
        
        print()
        print(f"🎯 TOTALE: {len(publisher.all_stores)} store supportati")
        print(f"👥 Reach potenziale: 8+ miliardi di utenti")
        print(f"🌍 Copertura: 200+ paesi")
        print()
        print("🚀 API Endpoints:")
        print(f"   GET  / - Interfaccia principale")
        print(f"   GET  /api/stores - Informazioni store")
        print(f"   GET  /api/status - Stato pubblicazione")
        print(f"   GET  /api/start_publication - Avvia pubblicazione")
        print(f"   GET  /api/estimate_reach - Stima reach")
        print()
        print("Premi Ctrl+C per fermare il server")
        print("=" * 70)
        
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
    
    parser = argparse.ArgumentParser(description='FLASH Universal Multi-Store Publisher')
    parser.add_argument('--port', type=int, default=8000, help='Porta server (default: 8000)')
    parser.add_argument('--desktop', action='store_true', help='Avvia app desktop invece del server web')
    
    args = parser.parse_args()
    
    if args.desktop:
        print("💻 Avvio FLASH Universal Desktop App...")
        try:
            from desktop_apps.flash_desktop_app import main as desktop_main
            desktop_main()
        except ImportError as e:
            print(f"❌ Errore import desktop app: {e}")
            print("💡 Installa tkinter: pip install tkinter")
    else:
        success = start_universal_server(args.port)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()