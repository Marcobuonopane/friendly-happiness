#!/usr/bin/env python3
"""
🔐 AUTENTICO - Dedicated Server
Sistema di Certificazione Digitale Sicura
Created by: Marco Buonopane (Creator/Owner) & Massimiliano Cardinali (Design Collaborator)
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class AutenticoHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for AUTENTICO app"""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve from the src folder
        super().__init__(*args, directory="/home/user/webapp/src", **kwargs)
    
    def do_GET(self):
        """Handle GET requests with proper routing"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        
        # Add CORS headers for development
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Serve the AUTENTICO index.html file
        try:
            with open('/home/user/webapp/src/index.html', 'rb') as f:
                content = f.read()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "AUTENTICO app not found")
    
    def log_message(self, format, *args):
        """Enhanced logging with timestamp"""
        sys.stdout.write(f"🔐 AUTENTICO [{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

def start_autentico_server(port=5000):
    """Start the dedicated AUTENTICO server"""
    print("🌟 AUTENTICO - Digital Certification System")
    print("=" * 50)
    print("Creator/Owner: Marco Buonopane")
    print("Design Collaborator: Massimiliano Cardinali")
    print("=" * 50)
    print(f"🚀 Starting AUTENTICO server on port {port}...")
    
    # Verify AUTENTICO app exists
    if not os.path.exists('/home/user/webapp/src/index.html'):
        print("❌ ERROR: AUTENTICO app (src/index.html) not found!")
        return False
    
    try:
        # Create server
        with socketserver.TCPServer(("0.0.0.0", port), AutenticoHandler) as httpd:
            print(f"✅ AUTENTICO server running on http://0.0.0.0:{port}")
            print("🔐 Features available:")
            print("   • AES-256 Encryption")
            print("   • Biometric Authentication")
            print("   • GPS Tracking")
            print("   • Digital Certification")
            print("   • Elegant Parchment Theme")
            print("   • Red Wax Seal Design")
            print()
            print("📱 Access your AUTENTICO app and start certifying!")
            print("🛑 Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 AUTENTICO server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting AUTENTICO server: {e}")
        return False

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    start_autentico_server(port)