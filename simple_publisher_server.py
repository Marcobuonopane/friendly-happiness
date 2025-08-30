#!/usr/bin/env python3
"""
🚀 SIMPLE REAL PUBLISHER - Direct Launch
======================================================================
Simple Flask server for real store publishing
======================================================================
"""

from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main control interface"""
    return send_file('real_publisher_control.html')

@app.route('/api/status')
def status():
    """Get system status"""
    autentico_exists = os.path.exists('com.marcobuonopane.autentico-2.2.0.aab')
    flash_exists = os.path.exists('com.marcobuonopane.flashuniversal-3.0.0.aab')
    
    return jsonify({
        'status': 'ready',
        'autentico_aab': autentico_exists,
        'flash_aab': flash_exists,
        'message': 'Real Store Publisher ready for human + AI collaboration!'
    })

@app.route('/download/<filename>')
def download_aab(filename):
    """Download AAB files"""
    if filename.endswith('.aab') and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("🚀 REAL STORE PUBLISHER - SIMPLE LAUNCH")
    print("=" * 50)
    print("📱 Apps: AUTENTICO + FLASH UNIVERSAL")
    print("🎯 Mission: Real publishing to ALL stores (except Apple)")
    print("🤖 AI + 👤 Human collaboration system")
    print("=" * 50)
    
    # Check AAB files
    autentico_aab = 'com.marcobuonopane.autentico-2.2.0.aab'
    flash_aab = 'com.marcobuonopane.flashuniversal-3.0.0.aab'
    
    if os.path.exists(autentico_aab):
        size = os.path.getsize(autentico_aab)
        print(f"✅ AUTENTICO AAB: {size:,} bytes")
    else:
        print(f"❌ {autentico_aab}: Not found")
        
    if os.path.exists(flash_aab):
        size = os.path.getsize(flash_aab)
        print(f"✅ FLASH UNIVERSAL AAB: {size:,} bytes")
    else:
        print(f"❌ {flash_aab}: Not found")
    
    print()
    print("🌐 Starting web interface...")
    print("💡 Open the URL below to start real publishing!")
    
    app.run(host='0.0.0.0', port=6000, debug=False)