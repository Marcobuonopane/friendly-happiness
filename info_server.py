#!/usr/bin/env python3
"""
Info Server for AUTENTICO - Pre-download information page
"""

import http.server
import socketserver
import os
import sys

class InfoHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for AUTENTICO info page"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/home/user/webapp", **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/info':
            self.path = '/autentico_info.html'
        elif self.path == '/readme':
            self.path = '/AUTENTICO_README.md'
        
        return super().do_GET()
    
    def log_message(self, format, *args):
        sys.stdout.write(f"📋 INFO [{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    
    print(f"📋 Starting AUTENTICO Info Server on port {port}...")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), InfoHandler) as httpd:
            print(f"✅ Info server running on http://0.0.0.0:{port}")
            print("📋 Available pages:")
            print("   • / or /info - App information page")
            print("   • /readme - Technical documentation")
            print("🛑 Press Ctrl+C to stop")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Info server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")