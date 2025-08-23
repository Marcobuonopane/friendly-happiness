#!/bin/bash

# 🚀 AUTENTICO - Sistema One-Click per Play Store
# Script di avvio sistema automatico
# Marco Buonopane (Creatore) + Massimiliano Cardinali (Design)

echo "🚀 AUTENTICO - Sistema One-Click Play Store"
echo "🏆 Marco Buonopane (Creatore) + Massimiliano Cardinali (Design)"
echo "🤖 Powered by AI Assistant"
echo "=================================="

# Controlla se supervisor è installato
if ! command -v supervisord &> /dev/null; then
    echo "📦 Installazione supervisor..."
    pip install supervisor
fi

# Vai nella directory corretta
cd /home/user/webapp/one_click_automation

# Ferma eventuali processi precedenti
echo "🛑 Fermando servizi precedenti..."
supervisorctl -c config/supervisor_oneclick.conf shutdown 2>/dev/null || true
pkill -f "web_server.py" 2>/dev/null || true

# Pulisce log vecchi
echo "🧹 Pulizia log..."
rm -f logs/*.log logs/*.pid logs/*.sock

# Avvia supervisor
echo "🚀 Avvio sistema automatico..."
supervisord -c config/supervisor_oneclick.conf

# Attende avvio servizi
sleep 3

# Controlla stato
echo "📊 Stato servizi:"
supervisorctl -c config/supervisor_oneclick.conf status

echo ""
echo "✅ SISTEMA ONE-CLICK ATTIVO!"
echo ""
echo "🌐 Accedi a uno di questi URL:"
echo "   📱 http://localhost:8000  (Porta principale)"
echo "   🖥️  http://localhost:3000  (Porta alternativa)"
echo ""
echo "🎯 COSA FARE:"
echo "1. Apri uno degli URL nel browser"
echo "2. Clicca il pulsante 'PUBBLICA CON UN CLICK!'"
echo "3. Attendi 30 secondi per la magia ✨"
echo "4. AUTENTICO sarà pubblicato automaticamente!"
echo ""
echo "🛑 Per fermare il sistema:"
echo "   supervisorctl -c config/supervisor_oneclick.conf shutdown"
echo ""
echo "=================================="